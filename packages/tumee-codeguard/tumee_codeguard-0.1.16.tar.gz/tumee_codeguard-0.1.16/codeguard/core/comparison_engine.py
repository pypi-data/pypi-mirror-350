"""
Comparison Engine for CodeGuard.

This module is responsible for comparing guarded regions between original
and modified versions of code, and identifying violations.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from ..parsers.guard_parser import GuardedRegion, GuardWho
from ..utils.hash_calculator import HashCalculator


# Define GuardViolation type to avoid circular imports
class GuardViolation:
    """
    Represents a detected violation of a guard rule.

    This class encapsulates information about a code modification that
    violates a guard annotation, including the location, type of violation,
    content changes, and severity level.

    Attributes:
        file: Path to the file containing the violation
        line: Line number where the violation starts
        guard_type: Type of guard that was violated (e.g., "AI-RO", "ALL-FX")
        original_hash: Content hash of the original guarded region
        modified_hash: Content hash of the modified guarded region
        message: Human-readable description of the violation
        original_content: Original content of the guarded region
        modified_content: Modified content of the guarded region
        severity: Violation severity ("critical", "warning", or "info")
        diff_summary: Optional summary of the changes made
        violated_by: Optional identifier of who violated the guard
        guard_source: Optional source of the guard rule (file path, line)
    """

    def __init__(
        self,
        file: str,
        line: int,
        guard_type: str,
        original_hash: str,
        modified_hash: str,
        message: str,
        original_content: str,
        modified_content: str,
        severity: str = "critical",
        diff_summary: Optional[str] = None,
        violated_by: Optional[str] = None,
        guard_source: Optional[str] = None,
    ) -> None:
        """
        Initialize a GuardViolation instance.

        Args:
            file: Path to the file containing the violation
            line: Line number where the violation starts
            guard_type: Type of guard that was violated
            original_hash: Content hash of the original region
            modified_hash: Content hash of the modified region
            message: Description of the violation
            original_content: Original content
            modified_content: Modified content
            severity: Violation severity level
            diff_summary: Optional change summary
            violated_by: Optional violator identifier
            guard_source: Optional guard rule source
        """
        self.file = file
        self.line = line
        self.guard_type = guard_type
        self.original_hash = original_hash
        self.modified_hash = modified_hash
        self.message = message
        self.original_content = original_content
        self.modified_content = modified_content
        self.severity = severity
        self.diff_summary = diff_summary
        self.violated_by = violated_by
        self.guard_source = guard_source

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert violation to dictionary representation.

        Returns:
            Dictionary containing all violation information suitable
            for JSON serialization or reporting
        """
        result = {
            "file": self.file,
            "line": self.line,
            "guard_type": self.guard_type,
            "original_hash": self.original_hash,
            "modified_hash": self.modified_hash,
            "message": self.message,
            "original_content": self.original_content,
            "modified_content": self.modified_content,
            "severity": self.severity,
        }

        if self.diff_summary:
            result["diff_summary"] = self.diff_summary

        if self.violated_by:
            result["violated_by"] = self.violated_by

        if self.guard_source:
            result["guard_source"] = self.guard_source

        return result


class ViolationSeverity(Enum):
    """
    Severity levels for guard violations.

    This enum defines the severity levels assigned to different types
    of guard violations based on the permission level that was violated.

    Values:
        CRITICAL: Violations of "fixed" (n) permissions - no changes allowed
        WARNING: Violations of "read-only" (r) permissions - read but not modify
        INFO: Changes to "write" (w) permissions - allowed but noteworthy
    """

    CRITICAL = "critical"  # Fixed (FX) regions
    WARNING = "warning"  # Read-only (RO) regions
    INFO = "info"  # Editable (ED) regions with changes


class ComparisonEngine:
    """
    Engine for comparing guarded regions and detecting violations.

    This class is responsible for comparing guarded code regions between
    original and modified versions of a file, detecting any violations of
    guard rules based on the target audience (e.g., AI) and permission
    levels (read-only, write, none).

    The engine uses content hashing to detect changes and supports various
    normalization options to handle differences in formatting that shouldn't
    be considered violations.

    Attributes:
        hash_calculator: Calculator for generating normalized content hashes
        target: Target audience for guard checks (e.g., GuardWho.ai)
    """

    def __init__(
        self,
        normalize_whitespace: bool = True,
        normalize_line_endings: bool = True,
        ignore_blank_lines: bool = True,
        ignore_indentation: bool = False,
        context_lines: int = 3,
    ) -> None:
        """
        Initialize the comparison engine with normalization options.

        Args:
            normalize_whitespace: If True, treat multiple spaces/tabs as single space
            normalize_line_endings: If True, treat CRLF and LF as equivalent
            ignore_blank_lines: If True, ignore empty lines when comparing
            ignore_indentation: If True, ignore leading whitespace differences
            context_lines: Number of context lines to include around changes
        """
        self.hash_calculator = HashCalculator(
            normalize_whitespace=normalize_whitespace,
            normalize_line_endings=normalize_line_endings,
            ignore_blank_lines=ignore_blank_lines,
            ignore_indentation=ignore_indentation,
        )
        self.context_lines = context_lines

    def compare_regions(
        self,
        original_regions: List[GuardedRegion],
        modified_regions: List[GuardedRegion],
        file_path: str,
        original_content: str,
        modified_content: str,
        target: GuardWho = GuardWho.ai,
        identifier: Optional[str] = None,
    ) -> List[GuardViolation]:
        """
        Compare guarded regions between original and modified code to detect violations.

        This method performs the core comparison logic by:
        1. Matching regions between original and modified versions
        2. Checking each region's permissions for the target audience
        3. Detecting changes that violate guard rules
        4. Creating violation records with appropriate severity

        Args:
            original_regions: List of guarded regions from the original code
            modified_regions: List of guarded regions from the modified code
            file_path: Path to the file being validated
            original_content: Complete content of the original file
            modified_content: Complete content of the modified file
            target: Target audience to check permissions for (default: AI)
            identifier: Optional specific identifier within the target group
                       (e.g., "claude-4" for a specific AI model)

        Returns:
            List of GuardViolation objects representing detected violations,
            sorted by line number. Empty list if no violations found.

        Note:
            The comparison uses content hashing with the normalization options
            specified during engine initialization to determine if regions have
            been modified.
        """
        violations = []

        # Map regions by line number for easier comparison
        original_map = {region.start_line: region for region in original_regions}
        modified_map = {region.start_line: region for region in modified_regions}

        # Case 1: Check for modifications to existing regions
        for start_line, original_region in original_map.items():
            modified_region = modified_map.get(start_line)

            # Skip if region is not present in modified code
            if not modified_region:
                # If region is completely removed, check if it was fixed
                if original_region.is_fixed_for(target, identifier):
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line=original_region.start_line,
                            guard_type=self._format_guard_type(target, identifier, "n"),
                            message="Fixed region was removed",
                            original_content='\n'.join(original_region.content.splitlines()[:self.context_lines*2]) + 
                                           ('\n... (region continues)' if len(original_region.content.splitlines()) > self.context_lines*2 else ''),
                            modified_content="",
                            original_hash=self.hash_calculator.calculate_hash(
                                original_region.content
                            ),
                            modified_hash=self.hash_calculator.calculate_hash(""),
                            severity=ViolationSeverity.CRITICAL,
                            identifier=identifier,
                        )
                    )
                # If region is read-only and removed, report violation
                elif not original_region.is_editable_by(target, identifier):
                    violations.append(
                        self._create_violation(
                            file_path=file_path,
                            line=original_region.start_line,
                            guard_type=self._format_guard_type(target, identifier, "r"),
                            message="Read-only region was removed",
                            original_content='\n'.join(original_region.content.splitlines()[:self.context_lines*2]) + 
                                           ('\n... (region continues)' if len(original_region.content.splitlines()) > self.context_lines*2 else ''),
                            modified_content="",
                            original_hash=self.hash_calculator.calculate_hash(
                                original_region.content
                            ),
                            modified_hash=self.hash_calculator.calculate_hash(""),
                            severity=ViolationSeverity.WARNING,
                            identifier=identifier,
                        )
                    )
                continue

            # Check if region content has changed
            is_changed, original_hash, modified_hash = self.hash_calculator.compare_content(
                original_region.content, modified_region.content
            )

            if not is_changed:
                # Content hasn't changed, no violation
                continue

            # Check if region is fixed (unchangeable)
            if original_region.is_fixed_for(target, identifier):
                orig_context, mod_context = self._extract_change_context(
                    original_region.content, modified_region.content
                )
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line=original_region.start_line,
                        guard_type=self._format_guard_type(target, identifier, "n"),
                        message="Fixed region was modified",
                        original_content=orig_context,
                        modified_content=mod_context,
                        original_hash=original_hash,
                        modified_hash=modified_hash,
                        severity=ViolationSeverity.CRITICAL,
                        identifier=identifier,
                    )
                )

            # Check if region is read-only
            elif not original_region.is_editable_by(target, identifier):
                orig_context, mod_context = self._extract_change_context(
                    original_region.content, modified_region.content
                )
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line=original_region.start_line,
                        guard_type=self._format_guard_type(target, identifier, "r"),
                        message="Read-only region was modified",
                        original_content=orig_context,
                        modified_content=mod_context,
                        original_hash=original_hash,
                        modified_hash=modified_hash,
                        severity=ViolationSeverity.WARNING,
                        identifier=identifier,
                    )
                )

            # Track changes to editable regions as well for informational purposes
            elif is_changed:
                orig_context, mod_context = self._extract_change_context(
                    original_region.content, modified_region.content
                )
                violations.append(
                    self._create_violation(
                        file_path=file_path,
                        line=original_region.start_line,
                        guard_type=self._format_guard_type(target, identifier, "w"),
                        message="Editable region was modified",
                        original_content=orig_context,
                        modified_content=mod_context,
                        original_hash=original_hash,
                        modified_hash=modified_hash,
                        severity=ViolationSeverity.INFO,
                        identifier=identifier,
                    )
                )

        # Case 2: Check for new regions added in modified code that overlap with existing guards
        for start_line, modified_region in modified_map.items():
            if start_line not in original_map:
                # New region was added
                # Check if it overlaps with any fixed or read-only region
                for original_region in original_regions:
                    if (
                        modified_region.start_line <= original_region.end_line
                        and modified_region.end_line >= original_region.start_line
                    ):
                        # Regions overlap
                        if original_region.is_fixed_for(target, identifier):
                            violations.append(
                                self._create_violation(
                                    file_path=file_path,
                                    line=modified_region.start_line,
                                    guard_type=self._format_guard_type(target, identifier, "n"),
                                    message="New region overlaps with fixed region",
                                    original_content='\n'.join(original_region.content.splitlines()[:self.context_lines*2]) + 
                                                   ('\n... (region continues)' if len(original_region.content.splitlines()) > self.context_lines*2 else ''),
                                    modified_content='\n'.join(modified_region.content.splitlines()[:self.context_lines*2]) + 
                                                   ('\n... (region continues)' if len(modified_region.content.splitlines()) > self.context_lines*2 else ''),
                                    original_hash=self.hash_calculator.calculate_hash(
                                        original_region.content
                                    ),
                                    modified_hash=self.hash_calculator.calculate_hash(
                                        modified_region.content
                                    ),
                                    severity=ViolationSeverity.CRITICAL,
                                    identifier=identifier,
                                )
                            )
                            break
                        elif not original_region.is_editable_by(target, identifier):
                            violations.append(
                                self._create_violation(
                                    file_path=file_path,
                                    line=modified_region.start_line,
                                    guard_type=self._format_guard_type(target, identifier, "r"),
                                    message="New region overlaps with read-only region",
                                    original_content='\n'.join(original_region.content.splitlines()[:self.context_lines*2]) + 
                                                   ('\n... (region continues)' if len(original_region.content.splitlines()) > self.context_lines*2 else ''),
                                    modified_content='\n'.join(modified_region.content.splitlines()[:self.context_lines*2]) + 
                                                   ('\n... (region continues)' if len(modified_region.content.splitlines()) > self.context_lines*2 else ''),
                                    original_hash=self.hash_calculator.calculate_hash(
                                        original_region.content
                                    ),
                                    modified_hash=self.hash_calculator.calculate_hash(
                                        modified_region.content
                                    ),
                                    severity=ViolationSeverity.WARNING,
                                    identifier=identifier,
                                )
                            )
                            break

        return violations

    def _format_guard_type(self, who: GuardWho, identifier: Optional[str], permission: str) -> str:
        """Format guard type string with identifier if present."""
        who_part = who.value.upper()
        if identifier:
            who_part += f"[{identifier}]"
        perm_part = permission.upper()
        return f"{who_part}-{perm_part}"

    def _create_violation(
        self,
        file_path: str,
        line: int,
        guard_type: str,
        message: str,
        original_content: str,
        modified_content: str,
        original_hash: str,
        modified_hash: str,
        severity: ViolationSeverity,
        identifier: Optional[str] = None,
        guard_source: str = "file-level",
    ) -> GuardViolation:
        """
        Create a guard violation object.

        Args:
            file_path: Path to the file
            line: Line number of the violation
            guard_type: Type of guard (e.g., "AI-R", "AI[claude-4]-N")
            message: Violation message
            original_content: Original content
            modified_content: Modified content
            original_hash: Hash of original content
            modified_hash: Hash of modified content
            severity: Violation severity
            identifier: Specific identifier that violated the guard
            guard_source: Source of the guard rule

        Returns:
            GuardViolation object
        """
        # Get the diff between original and modified content
        diffs = self.hash_calculator.get_diff_lines(original_content, modified_content)

        # Create a formatted diff summary (limit to 10 lines for brevity)
        diff_summary = []
        for i, (orig, mod) in enumerate(diffs[:10]):
            diff_summary.append(f"- Original: {orig}")
            diff_summary.append(f"+ Modified: {mod}")

        if len(diffs) > 10:
            diff_summary.append(f"... and {len(diffs) - 10} more line(s)")

        diff_text = "\n".join(diff_summary)

        return GuardViolation(
            file=file_path,
            line=line,
            guard_type=guard_type,
            original_hash=original_hash,
            modified_hash=modified_hash,
            message=message,
            original_content=original_content,
            modified_content=modified_content,
            severity=severity.value,
            diff_summary=diff_text,
            violated_by=f"{guard_type.split('-')[0].lower()}[{identifier}]"
            if identifier
            else guard_type.split("-")[0].lower(),
            guard_source=guard_source,
        )

    def _extract_change_context(
        self,
        original_content: str,
        modified_content: str,
        context_lines: int = None,
    ) -> tuple[str, str]:
        """
        Extract only the changed lines plus surrounding context.

        Args:
            original_content: Full original content
            modified_content: Full modified content
            context_lines: Number of context lines (uses self.context_lines if None)

        Returns:
            Tuple of (original_context, modified_context) containing only relevant lines
        """
        if context_lines is None:
            context_lines = self.context_lines

        # Get line-by-line diff
        orig_lines = original_content.splitlines()
        mod_lines = modified_content.splitlines()
        
        # If content is already small, return as-is
        if len(orig_lines) <= context_lines * 2 + 1 and len(mod_lines) <= context_lines * 2 + 1:
            return original_content, modified_content
        
        # Find changed line indices
        changed_indices = set()
        
        # Use difflib to find changed lines
        import difflib
        matcher = difflib.SequenceMatcher(None, orig_lines, mod_lines)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                # Add changed line indices with context
                for i in range(max(0, i1 - context_lines), min(len(orig_lines), i2 + context_lines)):
                    changed_indices.add(('orig', i))
                for j in range(max(0, j1 - context_lines), min(len(mod_lines), j2 + context_lines)):
                    changed_indices.add(('mod', j))
        
        # Build context strings
        orig_context_lines = []
        mod_context_lines = []
        last_orig_idx = -1
        last_mod_idx = -1
        
        for content_type, idx in sorted(changed_indices):
            if content_type == 'orig':
                if last_orig_idx >= 0 and idx > last_orig_idx + 1:
                    orig_context_lines.append(f"... ({idx - last_orig_idx - 1} lines omitted) ...")
                orig_context_lines.append(orig_lines[idx])
                last_orig_idx = idx
            else:
                if last_mod_idx >= 0 and idx > last_mod_idx + 1:
                    mod_context_lines.append(f"... ({idx - last_mod_idx - 1} lines omitted) ...")
                mod_context_lines.append(mod_lines[idx])
                last_mod_idx = idx
        
        # Add ellipsis if we're not showing the beginning or end
        orig_indices = [idx for t, idx in changed_indices if t == 'orig']
        mod_indices = [idx for t, idx in changed_indices if t == 'mod']
        
        if orig_indices and min(orig_indices) > 0:
            orig_context_lines.insert(0, f"... ({min(orig_indices)} lines omitted) ...")
        if orig_indices and max(orig_indices) < len(orig_lines) - 1:
            orig_context_lines.append(f"... ({len(orig_lines) - max(orig_indices) - 1} lines omitted) ...")
            
        if mod_indices and min(mod_indices) > 0:
            mod_context_lines.insert(0, f"... ({min(mod_indices)} lines omitted) ...")
        if mod_indices and max(mod_indices) < len(mod_lines) - 1:
            mod_context_lines.append(f"... ({len(mod_lines) - max(mod_indices) - 1} lines omitted) ...")
        
        return '\n'.join(orig_context_lines), '\n'.join(mod_context_lines)
