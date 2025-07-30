"""
Core validation logic for CodeGuard.

This module contains the main validation engine that orchestrates the process
of detecting guard annotations, calculating hashes, and identifying violations.
"""

from pathlib import Path
from typing import Dict, List, Optional, Union

from ..parsers.guard_parser import (
    GuardDirective,
    GuardedRegion,
    GuardParser,
    GuardPermission,
    GuardWho,
)
from ..parsers.language_parser import LanguageParser
from .comparison_engine import ComparisonEngine, GuardViolation
from .directory_guard import DirectoryGuard


class ValidationResult:
    """
    Contains the results of a validation operation.

    This class encapsulates the results of validating code changes,
    including any violations found and summary statistics.

    Attributes:
        files_checked: Number of files that were checked
        violations: List of guard violations found
        directory_guards_used: Whether directory-level guards were applied
        directory_rules_applied: List of directory guard rules that were applied
    """

    def __init__(
        self,
        files_checked: int,
        violations: List[GuardViolation],
        directory_guards_used: bool = False,
        directory_rules_applied: List[Dict] = None,
    ) -> None:
        """
        Initialize a ValidationResult.

        Args:
            files_checked: Number of files that were checked
            violations: List of guard violations found
            directory_guards_used: Whether directory-level guards were applied
            directory_rules_applied: List of directory guard rules that were applied
        """
        self.files_checked = files_checked
        self.violations = violations
        self.directory_guards_used = directory_guards_used
        self.directory_rules_applied = directory_rules_applied or []

    @property
    def violations_found(self) -> int:
        """
        Get the total number of violations found.

        Returns:
            Total count of all violations
        """
        return len(self.violations)

    @property
    def status(self) -> str:
        """
        Get the overall validation status.

        Returns:
            "SUCCESS" if no critical/warning violations, "FAILED" otherwise
        """
        # Only consider critical and warning violations for the status
        critical_violations = [v for v in self.violations if v.severity != "info"]
        return "FAILED" if critical_violations else "SUCCESS"

    @property
    def critical_count(self) -> int:
        """
        Get the number of critical violations.

        Returns:
            Count of violations with severity "critical"
        """
        return len([v for v in self.violations if v.severity == "critical"])

    @property
    def warning_count(self) -> int:
        """
        Get the number of warning violations.

        Returns:
            Count of violations with severity "warning"
        """
        return len([v for v in self.violations if v.severity == "warning"])

    @property
    def info_count(self) -> int:
        """
        Get the number of info violations.

        Returns:
            Count of violations with severity "info"
        """
        return len([v for v in self.violations if v.severity == "info"])

    @property
    def directory_guard_count(self) -> int:
        """
        Get the number of directory-level guards applied.

        Returns:
            Count of directory guard rules that were applied
        """
        return len(self.directory_rules_applied)

    def to_dict(self) -> Dict:
        """
        Convert validation result to dictionary representation.

        Returns:
            Dictionary containing violations and summary statistics
        """
        result = {
            "violations": [v.to_dict() for v in self.violations],
            "summary": {
                "files_checked": self.files_checked,
                "violations_found": self.violations_found,
                "critical_count": self.critical_count,
                "warning_count": self.warning_count,
                "info_count": self.info_count,
                "status": self.status,
            },
        }

        # Add directory guard information if used
        if self.directory_guards_used:
            result["summary"]["directory_guards_used"] = True
            result["summary"]["directory_guard_count"] = self.directory_guard_count

            if self.directory_rules_applied:
                result["directory_rules"] = self.directory_rules_applied

        return result


class CodeGuardValidator:
    """
    Main validator class that orchestrates the validation process.

    This class is responsible for detecting guard annotations, calculating
    hashes for guarded regions, and identifying violations when comparing
    original and modified code files.

    The validator supports:
    - Multiple programming languages via tree-sitter
    - Directory-level guard rules (.ai-attributes files)
    - Various normalization options for comparison
    - Different target audiences (currently only "ai" is supported)

    Attributes:
        guard_parser: Parser for guard annotations
        language_parser: Parser for language-specific syntax
        comparison_engine: Engine for comparing code regions
        target: Target audience for guard checks
        directory_guard: Directory-level guard manager
    """

    def __init__(
        self,
        normalize_whitespace: bool = True,
        normalize_line_endings: bool = True,
        ignore_blank_lines: bool = True,
        ignore_indentation: bool = False,
        target: str = "ai",
        repo_path: Optional[Union[str, Path]] = None,
        use_directory_guards: bool = True,
        context_lines: int = 3,
    ) -> None:
        """
        Initialize the validator with specified options.

        Args:
            normalize_whitespace: Whether to normalize whitespace when comparing
            normalize_line_endings: Whether to normalize line endings (CRLF/LF)
            ignore_blank_lines: Whether to ignore blank lines in comparison
            ignore_indentation: Whether to ignore indentation changes
            target: Target audience for guard checks (currently only "ai" supported)
            repo_path: Repository root path for finding directory guard files
            use_directory_guards: Whether to apply directory-level guard rules
            context_lines: Number of context lines to include around changes
        """
        self.guard_parser = GuardParser()
        self.language_parser = LanguageParser()
        self.comparison_engine = ComparisonEngine(
            normalize_whitespace=normalize_whitespace,
            normalize_line_endings=normalize_line_endings,
            ignore_blank_lines=ignore_blank_lines,
            ignore_indentation=ignore_indentation,
            context_lines=context_lines,
        )

        try:
            self.target = GuardWho(target)
        except ValueError:
            # Try legacy names
            try:
                self.target = GuardWho[target]
            except (ValueError, KeyError):
                self.target = GuardWho.ai

        self.repo_path = repo_path
        self.use_directory_guards = use_directory_guards
        self.directory_guard = DirectoryGuard(repo_path) if use_directory_guards else None

    def validate_files(
        self, original_path: Union[str, Path], modified_path: Union[str, Path]
    ) -> ValidationResult:
        """
        Validate changes between two files for guard violations.

        This method compares the original and modified versions of a file,
        checking for violations of guard annotations. It extracts guard
        directives from both files, identifies guarded regions, and checks
        if any modifications violate the guard rules.

        Args:
            original_path: Path to the original/reference file
            modified_path: Path to the modified/changed file

        Returns:
            ValidationResult object containing:
                - Number of files checked
                - List of guard violations found
                - Directory guard information if applicable
                - Summary statistics

        Raises:
            No exceptions are raised; file read errors are returned as violations
        """
        # Read file contents
        try:
            with open(original_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            with open(modified_path, "r", encoding="utf-8") as f:
                modified_content = f.read()
        except Exception as e:
            return ValidationResult(
                files_checked=0,
                violations=[
                    GuardViolation(
                        file=str(original_path),
                        line=0,
                        guard_type="ERROR",
                        original_hash="",
                        modified_hash="",
                        message=f"Error reading files: {str(e)}",
                        original_content="",
                        modified_content="",
                        severity="critical",
                    )
                ],
            )

        # Detect language
        language = self.language_parser.detect_language(original_path)

        # Extract comments and regions from files
        original_comments = self.language_parser.extract_comments(original_content, language)
        original_regions = self.language_parser.extract_regions(original_content, language)

        modified_comments = self.language_parser.extract_comments(modified_content, language)
        modified_regions = self.language_parser.extract_regions(modified_content, language)

        # Extract guarded regions from files
        original_guarded_regions = self.guard_parser.extract_guarded_regions(
            original_content, language, original_comments, original_regions
        )

        modified_guarded_regions = self.guard_parser.extract_guarded_regions(
            modified_content, language, modified_comments, modified_regions
        )

        # Apply directory-level permissions if enabled
        directory_guards_used = False
        directory_rules_applied = []

        if self.use_directory_guards and self.directory_guard:
            modified_path_obj = Path(modified_path)

            # Check if there are any applicable directory rules
            dir_rules = self.directory_guard.get_applicable_rules(modified_path_obj)
            if dir_rules:
                directory_guards_used = True
                # Convert rules to dictionary for reporting
                for rule in dir_rules:
                    directory_rules_applied.append(rule.to_dict())

            # Apply the directory permissions
            self._apply_directory_permissions(modified_path_obj, original_guarded_regions)

        # Compare regions and detect violations
        violations = self.comparison_engine.compare_regions(
            original_guarded_regions,
            modified_guarded_regions,
            str(original_path),
            original_content,
            modified_content,
            self.target,
        )

        return ValidationResult(
            files_checked=1,
            violations=violations,
            directory_guards_used=directory_guards_used,
            directory_rules_applied=directory_rules_applied,
        )

    def _apply_directory_permissions(
        self, file_path: Path, guarded_regions: List[GuardedRegion]
    ) -> None:
        """
        Apply directory-level permissions to guarded regions.

        This method enhances file-level guard annotations with directory-level permissions.
        Directory-level permissions are applied as a base level, and file-level annotations
        can only make them more restrictive, not less.

        Args:
            file_path: Path to the file
            guarded_regions: List of guarded regions to update
        """
        if not self.directory_guard:
            return

        # Get directory-level permissions for the file
        ai_permissions = self.directory_guard.get_effective_permissions(file_path, "ai")
        # hu_permissions no longer needed as we only support 'ai' target

        # Convert to permission enum
        ai_permission = ai_permissions.get("permission", GuardPermission.w)

        # Apply directory permissions as a base level for unguarded lines
        # We'll create a default region for the entire file if no file-level guards exist
        if not guarded_regions:
            # Create a directive with the appropriate permissions
            default_directive = GuardDirective(
                who=GuardWho.ai,
                permission=GuardPermission.w,  # Start with most permissive
                description="Default directory-level guard",
                line_number=1,
            )

            # Set permissions based on directory-level guards
            if ai_permission == GuardPermission.r:
                default_directive.permission = GuardPermission.r
            elif ai_permission == GuardPermission.n:
                default_directive.permission = GuardPermission.n

            # Create the guarded region with this directive
            default_region = GuardedRegion(
                start_line=1,
                end_line=len(file_path.read_text().splitlines()) + 1,
                content=file_path.read_text(),
                directives=[default_directive],
            )

            guarded_regions.append(default_region)
        else:
            # Enhance existing regions with directory-level permissions
            for region in guarded_regions:
                # Check if there are directives for ai
                ai_directives = [d for d in region.directives if d.who == GuardWho.ai]

                # Apply ai permissions
                for directive in ai_directives:
                    # Directory permission can only make file permission more restrictive
                    if (
                        ai_permission == GuardPermission.n
                        and directive.permission != GuardPermission.n
                    ):
                        directive.permission = GuardPermission.n
                    elif (
                        ai_permission == GuardPermission.r
                        and directive.permission == GuardPermission.w
                    ):
                        directive.permission = GuardPermission.r

    def validate_directory(
        self,
        directory: Union[str, Path],
        include_pattern: Optional[str] = None,
        exclude_pattern: Optional[str] = None,
    ) -> ValidationResult:
        """
        Scan a directory for guard annotations and validate consistency.

        This method recursively scans a directory tree for source code files,
        extracts guard annotations from each file, and checks for various
        issues like conflicting guards, overlapping regions, or guard rule
        violations. It does not compare files but validates the guard
        annotations themselves.

        Args:
            directory: Path to the directory to scan
            include_pattern: Optional glob pattern to include specific files
                           (e.g., "*.py" for Python files only)
            exclude_pattern: Optional glob pattern to exclude files
                           (e.g., "test_*.py" to exclude test files)

        Returns:
            ValidationResult object containing:
                - Number of files scanned
                - List of validation issues found
                - Directory guard information if applicable

        Note:
            This method validates guard annotation consistency, not file changes.
            Use validate_files() to check for guard violations between file versions.
        """
        import glob

        directory = Path(directory)

        # Get list of files to check
        if include_pattern:
            files = list(directory.glob(include_pattern))
        else:
            files = []
            for ext in [
                ".py",
                ".js",
                ".jsx",
                ".ts",
                ".tsx",
                ".java",
                ".cs",
                ".cpp",
                ".go",
                ".rs",
                ".rb",
                ".php",
            ]:
                files.extend(directory.glob(f"**/*{ext}"))

        # Apply exclude pattern if provided
        if exclude_pattern:
            exclude_files = set(directory.glob(exclude_pattern))
            files = [f for f in files if f not in exclude_files]

        # Validate each file
        all_violations = []
        files_checked = 0

        for file_path in files:
            # Skip directories
            if file_path.is_dir():
                continue

            # Read file content
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                # Skip files that can't be read
                continue

            # Detect language
            language = self.language_parser.detect_language(file_path)

            # Extract comments and regions
            comments = self.language_parser.extract_comments(content, language)
            regions = self.language_parser.extract_regions(content, language)

            # Extract guarded regions
            guarded_regions = self.guard_parser.extract_guarded_regions(
                content, language, comments, regions
            )

            # Apply directory-level guards if enabled
            has_directory_guards = False
            if self.use_directory_guards and self.directory_guard:
                # Check if this file has directory-level guards
                directory_rules = self.directory_guard.get_applicable_rules(file_path)
                if directory_rules:
                    has_directory_guards = True

                # Apply directory permissions
                self._apply_directory_permissions(file_path, guarded_regions)

            # If no guarded regions (file-level or directory-level), skip the file
            if not guarded_regions and not has_directory_guards:
                continue

            files_checked += 1

            # As we're only checking a single version, we just validate guard consistency
            # We don't have a "modified" version to compare against

            # Check for overlapping fixed/read-only regions
            for i, region1 in enumerate(guarded_regions):
                for j, region2 in enumerate(guarded_regions):
                    if i >= j:
                        continue

                    # Check if regions overlap
                    if (
                        region1.start_line <= region2.end_line
                        and region1.end_line >= region2.start_line
                    ):
                        # Regions overlap, check for conflicts
                        if (
                            region1.is_fixed_for(self.target)
                            and region2.is_editable_by(self.target)
                            or region2.is_fixed_for(self.target)
                            and region1.is_editable_by(self.target)
                        ):
                            all_violations.append(
                                GuardViolation(
                                    file=str(file_path),
                                    line=min(region1.start_line, region2.start_line),
                                    guard_type=f"{self.target.value}-CONFLICT",
                                    original_hash="",
                                    modified_hash="",
                                    message="Conflicting guard directives for overlapping regions",
                                    original_content=region1.content + "\n\n" + region2.content,
                                    modified_content="",
                                    severity="warning",
                                )
                            )

            # If directory-level guards are enabled, check for conflicts with file-level guards
            if self.use_directory_guards and has_directory_guards:
                self._check_directory_file_conflicts(file_path, guarded_regions, all_violations)

        # Collect directory guard information
        directory_guards_used = self.use_directory_guards and self.directory_guard is not None

        directory_rules = {}
        if directory_guards_used:
            # Gather all applied directory rules
            for file_path in files:
                if file_path.is_file():
                    rules = self.directory_guard.get_applicable_rules(file_path)
                    if rules:
                        directory_rules[str(file_path)] = [rule.to_dict() for rule in rules]

        # Convert to list format for the result
        directory_rules_applied = []
        for file_path, rules in directory_rules.items():
            directory_rules_applied.append({"file": file_path, "rules": rules})

        return ValidationResult(
            files_checked=files_checked,
            violations=all_violations,
            directory_guards_used=directory_guards_used,
            directory_rules_applied=directory_rules_applied,
        )

    def _check_directory_file_conflicts(
        self,
        file_path: Path,
        guarded_regions: List[GuardedRegion],
        violations: List[GuardViolation],
    ) -> None:
        """
        Check for conflicts between directory-level and file-level guards.

        Args:
            file_path: Path to the file
            guarded_regions: List of guarded regions
            violations: List to append any violations to
        """
        if not self.directory_guard:
            return

        # Get directory-level permissions
        ai_permissions = self.directory_guard.get_effective_permissions(file_path, "ai")

        # Get directory rules that apply to this file
        dir_rules = self.directory_guard.get_applicable_rules(file_path)
        if not dir_rules:
            return

        # Build a description of the directory rules
        rules_desc = []
        for rule in dir_rules[:3]:  # Only show first 3 rules for brevity
            if rule.source_file:
                source = f"{rule.source_file.name}"
                rules_desc.append(
                    f"{source}: {rule.pattern} @guard:{rule.who.value}:{rule.permission.value}"
                )

        rules_text = "\n".join(rules_desc)
        if len(dir_rules) > 3:
            rules_text += f"\n... and {len(dir_rules) - 3} more rules"

        # Check for conflicts between directory and file permissions
        for region in guarded_regions:
            # Skip regions from directory-level guards
            if any(d.description == "Default directory-level guard" for d in region.directives):
                continue

            # Check each directive in the region
            for directive in region.directives:
                # Check for ai permission conflicts
                if directive.who == GuardWho.ai:
                    ai_perm = ai_permissions.get("permission", GuardPermission.w)

                    # File tries to make more permissive than directory allows
                    if (
                        ai_perm == GuardPermission.n and directive.permission != GuardPermission.n
                    ) or (
                        ai_perm == GuardPermission.r and directive.permission == GuardPermission.w
                    ):
                        violations.append(
                            GuardViolation(
                                file=str(file_path),
                                line=region.start_line,
                                guard_type=f"ai-directive-conflict",
                                original_hash="",
                                modified_hash="",
                                message=f"File-level @guard:{directive.who.value}:{directive.permission.value} conflicts with directory-level @guard:ai:{ai_perm.value}",
                                original_content=f"Directory rules:\n{rules_text}\n\nFile-level guard at line {region.start_line}:\n{region.content}",
                                modified_content="",
                                severity="warning",
                            )
                        )

    def get_effective_permissions(
        self, path: Union[str, Path], verbose: bool = False, recursive: bool = False
    ) -> Dict:
        """
        Get the effective guard permissions for a path.

        This method calculates the effective permissions for a file or directory
        by considering both file-level guard annotations and directory-level
        guard rules from .ai-attributes files. It follows the permission
        hierarchy where directory rules can make file permissions more
        restrictive but not more permissive.

        Args:
            path: File or directory path to check permissions for
            verbose: If True, include detailed information about which rules
                    apply and their sources (file paths, line numbers)
            recursive: If True and path is a directory, recursively check
                      permissions for all files and subdirectories

        Returns:
            Dictionary containing:
                - path: The requested path
                - type: "file" or "directory"
                - permissions: Dict mapping targets (e.g., "ai") to their permissions
                - rules: List of applicable rules (if verbose=True)
                - children: Recursive results for subdirectories (if recursive=True)

        Example:
            >>> validator.get_effective_permissions("src/main.py")
            {
                "path": "src/main.py",
                "type": "file",
                "permissions": {"ai": "read-only"}
            }
        """
        if not self.directory_guard:
            # Initialize directory guard if not already initialized
            self.directory_guard = DirectoryGuard(self.repo_path)

        path_obj = Path(path)

        # Check if path exists
        if not path_obj.exists():
            return {
                "path": str(path_obj),
                "type": "unknown",
                "error": "Path does not exist",
                "status": "error",
            }

        # Get permissions with sources if verbose
        if verbose:
            permissions = self.directory_guard.get_permissions_with_sources(path_obj)
        else:
            # Get basic permissions
            ai_perms = self.directory_guard.get_effective_permissions(path_obj, "ai")
            human_perms = self.directory_guard.get_effective_permissions(path_obj, "human")

            # Format permission strings
            ai_perm_str = f"{ai_perms['who'].value}:{ai_perms['permission'].value}"

            # Format permission code
            perm_code = ai_perm_str

            # Format permissions in readable form
            permissions = {
                "path": str(path_obj),
                "type": "file" if path_obj.is_file() else "directory",
                "permissions": {
                    "ai": self.directory_guard._permission_to_readable(ai_perms["permission"]),
                    "human": self.directory_guard._permission_to_readable(
                        human_perms["permission"]
                    ),
                },
                "code": perm_code,
                "status": "success",
            }

        # Handle recursive directory scanning
        if recursive and path_obj.is_dir():
            # Get all children
            children = list(path_obj.glob("**/*"))

            # Filter out directories if requested
            if not recursive:
                children = [c for c in children if c.is_file()]

            # Process all children
            child_results = []
            consistent = True
            base_permissions = permissions["permissions"]

            for child in children:
                # Skip directories if not recursive
                if not recursive and child.is_dir():
                    continue

                # Get child permissions
                child_perms = self.get_effective_permissions(child)

                # Check consistency
                if (
                    child_perms["permissions"]["ai"] != base_permissions["ai"]
                    or child_perms["permissions"]["human"] != base_permissions["human"]
                ):
                    consistent = False

                # Add to results if verbose
                if verbose:
                    child_results.append(child_perms)

            # Add directory summary
            permissions["children"] = {
                "total": len(children),
                "consistent": consistent,
                "inconsistent_paths": [
                    str(c["path"])
                    for c in child_results
                    if c["permissions"]["ai"] != base_permissions["ai"]
                    or c["permissions"]["human"] != base_permissions["human"]
                ]
                if not consistent
                else [],
            }

            if verbose:
                permissions["child_permissions"] = child_results

        return permissions
