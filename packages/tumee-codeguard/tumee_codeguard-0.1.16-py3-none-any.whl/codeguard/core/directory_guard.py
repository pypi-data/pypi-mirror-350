"""
Directory-level guard system for CodeGuard.

This module provides functionality for managing directory-level guard annotations
through .ai-attributes files.
"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

from pathspec import PathSpec

from ..parsers.guard_parser import GuardParser, GuardPermission, GuardWho


class PatternRule:
    """
    A rule defined by a pattern and associated guard annotation.

    This class represents a single rule from an .ai-attributes file,
    consisting of a file pattern and a guard annotation.
    """

    def __init__(
        self,
        pattern: str,
        who: GuardWho,
        permission: GuardPermission,
        identifiers: Optional[List[str]] = None,
        description: Optional[str] = None,
        source_file: Optional[Path] = None,
        source_line: Optional[int] = None,
        context_metadata: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize a pattern rule.

        Args:
            pattern: File pattern to match
            who: Who the rule applies to (AI, HUMAN, ALL)
            permission: Permission level (r, w, n, context)
            identifiers: Optional list of specific identifiers (e.g., ["claude-4", "gpt-4"])
            description: Optional description of the rule
            source_file: Path to the source .ai-attributes file
            source_line: Line number in the source file
            context_metadata: Optional metadata for context files
        """
        self.pattern = pattern
        self.who = who
        self.permission = permission
        self.identifiers = identifiers
        self.description = description
        self.source_file = source_file
        self.source_line = source_line
        self.context_metadata = context_metadata

        # Create PathSpec for this single pattern
        self._pathspec = PathSpec.from_lines("gitwildmatch", [pattern])

    def applies_to_identifier(self, identifier: str) -> bool:
        """Check if this rule applies to a specific identifier."""
        if not self.identifiers:
            return True  # No specific identifiers means applies to all
        return "*" in self.identifiers or identifier in self.identifiers

    def matches(self, path: Union[str, Path], base_dir: Optional[Union[str, Path]] = None) -> bool:
        """
        Check if the given path matches this rule's pattern.

        Args:
            path: Path to check (can be relative or absolute)
            base_dir: Optional base directory for relative patterns

        Returns:
            True if the path matches, False otherwise
        """
        path_str = str(path)

        # Make path relative to base_dir if provided
        if base_dir:
            path_obj = Path(path_str)
            base_obj = Path(base_dir)
            try:
                path_str = str(path_obj.relative_to(base_obj))
            except ValueError:
                # Path is not relative to base_dir
                return False

        # Normalize path separators for consistent matching
        path_str = path_str.replace("\\", "/")

        # Handle . as current directory
        if path_str == ".":
            return False

        # Use pathspec for matching
        return self._pathspec.match_file(path_str)

    def get_specificity_score(self) -> int:
        """
        Calculate the specificity score of this rule's pattern.

        Higher scores indicate more specific patterns, used for precedence.

        Returns:
            Specificity score
        """
        pattern = self.pattern
        score = 0

        # Negation patterns are very specific
        if pattern.startswith("!"):
            score += 200
            pattern = pattern[1:]  # Remove ! for further analysis

        # Exact filename match is most specific
        if "/" not in pattern and "*" not in pattern and "?" not in pattern and "[" not in pattern:
            return 1000 + score

        # Path depth increases specificity
        segments = pattern.replace("\\", "/").split("/")
        score += len(segments) * 10

        # Patterns without wildcards are more specific
        if "**" not in pattern:
            score += 50
        if "*" not in pattern and "?" not in pattern:
            score += 30

        # Character classes add specificity
        if "[" in pattern:
            score += 15

        # Patterns with file extensions are more specific
        if "." in segments[-1] and not segments[-1].startswith("*"):
            score += 15

        # Absolute paths are more specific
        if pattern.startswith("/"):
            score += 25

        # Brace expansion adds some specificity
        if "{" in pattern:
            score += 10

        return score

    def __repr__(self) -> str:
        """String representation of the rule."""
        return (
            f"PatternRule(pattern='{self.pattern}', who={self.who}, permission={self.permission})"
        )

    def to_dict(self) -> Dict:
        """
        Convert rule to dictionary.

        Returns:
            Dictionary representation
        """
        result = {
            "pattern": self.pattern,
            "who": str(self.who),
            "permission": str(self.permission),
        }

        if self.identifiers:
            result["identifiers"] = self.identifiers

        if self.description:
            result["description"] = self.description

        if self.source_file:
            result["source_file"] = str(self.source_file)

        if self.source_line is not None:
            result["source_line"] = self.source_line

        if self.context_metadata:
            result["context_metadata"] = self.context_metadata

        return result


class DirectoryGuard:
    """
    Directory-level guard system.

    This class handles parsing and applying directory-level guard annotations
    from .ai-attributes files.
    """

    # Name of the attributes file
    ATTRIBUTES_FILENAME = ".ai-attributes"

    def __init__(self, repo_path: Optional[Union[str, Path]] = None):
        """
        Initialize the directory guard.

        Args:
            repo_path: Repository root path (default: current directory)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self._guard_parser = GuardParser()
        self._rules_cache: Dict[str, List[PatternRule]] = {}
        self._pathspec_cache: Dict[str, PathSpec] = {}
        self._parsed_files: Set[Path] = set()

    def parse_attributes_file(self, file_path: Union[str, Path]) -> List[PatternRule]:
        """
        Parse an .ai-attributes file into pattern rules.

        Args:
            file_path: Path to the .ai-attributes file

        Returns:
            List of parsed pattern rules

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file has invalid syntax
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Attributes file not found: {file_path}")

        rules = []

        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Parse the line
                try:
                    pattern, annotation = self._parse_attributes_line(line)

                    # Extract guard information
                    guard_info = self._guard_parser.parse_guard_annotation(annotation, line_num)

                    if guard_info:
                        # Extract context metadata if this is a context permission
                        context_metadata = None
                        if guard_info.permission == GuardPermission.context:
                            # Parse any metadata in brackets after permission
                            import re

                            metadata_match = re.search(r"\[([^\]]+)\]", annotation.split(":")[-1])
                            if metadata_match:
                                context_metadata = self._parse_context_metadata(
                                    metadata_match.group(1)
                                )

                        rule = PatternRule(
                            pattern=pattern,
                            who=guard_info.who,
                            permission=guard_info.permission,
                            identifiers=guard_info.identifiers
                            or ([guard_info.identifier] if guard_info.identifier else None),
                            description=guard_info.description,
                            source_file=file_path,
                            source_line=line_num,
                            context_metadata=context_metadata,
                        )
                        rules.append(rule)
                except ValueError as e:
                    # Add file and line information to the error
                    raise ValueError(f"Error in {file_path}, line {line_num}: {str(e)}")

        # Mark this file as parsed
        self._parsed_files.add(file_path)

        # Update cache
        dir_path = str(file_path.parent)
        if dir_path in self._rules_cache:
            self._rules_cache[dir_path].extend(rules)
        else:
            self._rules_cache[dir_path] = rules

        return rules

    def _parse_attributes_line(self, line: str) -> Tuple[str, str]:
        """
        Parse a line from an .ai-attributes file.

        Args:
            line: Line to parse

        Returns:
            Tuple of (pattern, guard_annotation)

        Raises:
            ValueError: If the line has invalid syntax
        """
        # Split the line into pattern and attributes
        parts = line.split(None, 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid attribute line format: {line}")

        pattern, annotation = parts

        # Validate the pattern
        if not pattern:
            raise ValueError(f"Empty pattern in attribute line: {line}")

        # Validate the annotation
        if not (annotation.startswith("@guard:") or annotation.startswith("@GUARD:")):
            raise ValueError(f"Invalid guard annotation: {annotation}")

        return pattern, annotation

    def _parse_context_metadata(self, metadata_str: str) -> Dict[str, str]:
        """Parse context metadata like priority=high,for=testing."""
        metadata = {}

        for item in metadata_str.split(","):
            if "=" in item:
                key, value = item.split("=", 1)
                metadata[key.strip()] = value.strip()

        return metadata

    def get_directory_rules(self, directory: Union[str, Path]) -> List[PatternRule]:
        """
        Get all pattern rules from an .ai-attributes file in the given directory.

        Args:
            directory: Directory to check

        Returns:
            List of pattern rules, or empty list if no .ai-attributes file
        """
        directory = Path(directory)

        # Check if we already parsed this directory
        dir_str = str(directory)
        if dir_str in self._rules_cache:
            return self._rules_cache[dir_str]

        # Check if .ai-attributes exists
        attributes_file = directory / self.ATTRIBUTES_FILENAME
        if attributes_file.exists():
            try:
                return self.parse_attributes_file(attributes_file)
            except (FileNotFoundError, ValueError):
                # Return empty list on errors
                return []

        # No file found, cache empty list
        self._rules_cache[dir_str] = []
        return []

    def get_all_parent_directories(self, path: Union[str, Path]) -> List[Path]:
        """
        Get all parent directories of a path, from most specific to least.

        Args:
            path: Path to get parents for

        Returns:
            List of parent directories, starting from the immediate parent
        """
        path = Path(path)

        # If path is a file (exists or looks like a file), start from its directory
        if path.is_file() or (not path.exists() and path.suffix):
            path = path.parent

        # Get all parents up to repo_path
        parents = []
        current = path

        while True:
            parents.append(current)
            # Stop if we've reached the repo root or filesystem root
            if current == self.repo_path or current == current.parent:
                break
            current = current.parent

        return parents

    def get_applicable_rules(self, path: Union[str, Path]) -> List[PatternRule]:
        """
        Get all rules applicable to a path, ordered by precedence.

        This method now supports negation patterns (!) and handles them properly.

        Args:
            path: Path to get rules for

        Returns:
            List of applicable rules in precedence order
        """
        path = Path(path)
        applicable_rules = []
        excluded = False

        # Get all parent directories
        parents = self.get_all_parent_directories(path)

        # Process from repo root down to immediate parent
        for directory in reversed(parents):
            rules = self.get_directory_rules(directory)

            # Process rules to handle negations
            for rule in rules:
                rel_path = path.relative_to(directory) if path != directory else Path(".")

                # Handle negation patterns
                if rule.pattern.startswith("!"):
                    # Negation pattern - remove exclusion if it matches
                    negated_pattern = rule.pattern[1:]
                    negated_spec = PathSpec.from_lines("gitwildmatch", [negated_pattern])
                    if negated_spec.match_file(str(rel_path).replace("\\", "/")):
                        excluded = False
                        applicable_rules.append(rule)
                else:
                    # Normal pattern
                    if rule.matches(rel_path) and not excluded:
                        applicable_rules.append(rule)
                        # Check if this is an exclusion rule
                        if rule.permission == GuardPermission.n:
                            excluded = True

        # Sort by specificity (highest first)
        applicable_rules.sort(key=lambda r: r.get_specificity_score(), reverse=True)

        return applicable_rules

    def get_effective_permissions(
        self, path: Union[str, Path], target: str = "ai", identifier: Optional[str] = None
    ) -> Dict[str, Union[GuardWho, GuardPermission]]:
        """
        Get effective permissions for a path based on directory-level guards.

        Args:
            path: Path to get permissions for
            target: Target audience ('ai' or 'human')
            identifier: Specific identifier (e.g., "claude-4", "security-team")

        Returns:
            Dictionary with who and permission keys
        """
        # Parse target
        if target.lower() == "ai":
            target_who = GuardWho.ai
        elif target.lower() == "human":
            target_who = GuardWho.human
        else:
            # Default to ai for backwards compatibility
            target_who = GuardWho.ai

        # Get applicable rules
        rules = self.get_applicable_rules(path)

        # Start with most permissive default
        permissions = {"who": target_who, "permission": GuardPermission.w}

        # Apply rules in precedence order, considering identifier specificity
        most_specific_rule = None
        for rule in rules:
            if rule.who == target_who:
                # Check if rule applies to the identifier
                if identifier and not rule.applies_to_identifier(identifier):
                    continue

                # More specific rules (with identifiers) take precedence
                if rule.identifiers and identifier in rule.identifiers:
                    # Direct identifier match is most specific
                    most_specific_rule = rule
                    break
                elif not rule.identifiers:
                    # Wildcard rule, use if no specific rule found yet
                    if not most_specific_rule:
                        most_specific_rule = rule

        # Apply the most specific rule found
        if most_specific_rule:
            permissions = {
                "who": most_specific_rule.who,
                "permission": most_specific_rule.permission,
            }

        # Return the permissions
        return permissions

    def get_permissions_with_sources(
        self, path: Union[str, Path], identifier: Optional[str] = None
    ) -> Dict:
        """
        Get permissions for a path with detailed source information.

        Args:
            path: Path to get permissions for
            identifier: Specific identifier (e.g., "claude-4")

        Returns:
            Dictionary with permissions and sources
        """
        path = Path(path)
        rules = self.get_applicable_rules(path)

        # Get effective permissions
        ai_perm = self.get_effective_permissions(path, "ai", identifier)
        human_perm = self.get_effective_permissions(path, "human", identifier)

        # Format permission strings
        ai_perm_str = f"{ai_perm['who'].value}:{ai_perm['permission'].value}"

        # Format permission code
        perm_code = ai_perm_str

        # Format permissions in readable form
        permissions = {
            "ai": self._permission_to_readable(ai_perm["permission"]),
            "human": self._permission_to_readable(human_perm["permission"]),
        }

        # Create sources list
        sources = []
        for rule in rules:
            if rule.source_file:
                # Determine the level
                if rule.source_file.parent == self.repo_path:
                    level = "repository"
                else:
                    level = "directory"

                perm_str = f"@guard:{rule.who.value}"
                if rule.identifiers:
                    perm_str += f"[{','.join(rule.identifiers)}]"
                perm_str += f":{rule.permission.value}"

                source_entry = {
                    "level": level,
                    "file": str(rule.source_file),
                    "pattern": rule.pattern,
                    "permission": perm_str,
                    "applies_to": [f"{rule.who.value}[{id}]" for id in rule.identifiers]
                    if rule.identifiers
                    else [f"{rule.who.value}[*]"],
                }
                sources.append(source_entry)

        return {
            "path": str(path),
            "type": "file" if path.is_file() else "directory",
            "permissions": permissions,
            "code": perm_code,
            "permission_sources": sources,
            "file_level_guards": [],  # To be filled by validator
            "status": "success",
        }

    def _permission_to_readable(self, permission: GuardPermission) -> str:
        """
        Convert a GuardPermission to a human-readable string.

        Args:
            permission: Permission to convert

        Returns:
            Human-readable permission string
        """
        if permission == GuardPermission.r:
            return "read-only"
        elif permission == GuardPermission.w:
            return "write"
        elif permission == GuardPermission.n:
            return "none"
        elif permission == GuardPermission.context:
            return "context"
        else:
            return "unknown"

    def get_directory_pathspec(self, directory: Union[str, Path]) -> Optional[PathSpec]:
        """
        Get compiled PathSpec for all rules in a directory.

        Args:
            directory: Directory to get PathSpec for

        Returns:
            Compiled PathSpec object or None if no rules
        """
        directory = Path(directory)
        dir_str = str(directory)

        if dir_str in self._pathspec_cache:
            return self._pathspec_cache[dir_str]

        rules = self.get_directory_rules(directory)
        if not rules:
            return None

        # Create PathSpec from all patterns
        patterns = [rule.pattern for rule in rules]
        pathspec_obj = PathSpec.from_lines("gitwildmatch", patterns)

        self._pathspec_cache[dir_str] = pathspec_obj
        return pathspec_obj

    def clear_cache(self):
        """Clear the cached rules and pathspecs."""
        self._rules_cache.clear()
        self._pathspec_cache.clear()
        self._parsed_files.clear()

    def create_attributes_file(self, directory: Union[str, Path], rules: List[Dict]) -> Path:
        """
        Create or update an .ai-attributes file.

        Args:
            directory: Directory to create the file in
            rules: List of rule dictionaries with pattern, who, and permission keys

        Returns:
            Path to the created attributes file

        Raises:
            ValueError: If the rules format is invalid
        """
        directory = Path(directory)

        # Make sure the directory exists
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")

        # Validate rules
        for rule in rules:
            if not all(k in rule for k in ("pattern", "who", "permission")):
                raise ValueError(f"Invalid rule format: {rule}")

        # Create the file content
        lines = ["# Directory-level guard attributes"]

        for rule in rules:
            pattern = rule["pattern"]
            who = rule["who"]
            permission = rule["permission"]
            description = rule.get("description", "")

            # Format the line
            line = f"{pattern} @guard:{who}:{permission}"
            if description:
                line += f" {description}"

            lines.append(line)

        # Write the file
        file_path = directory / self.ATTRIBUTES_FILENAME
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        # Clear cache for this directory
        dir_str = str(directory)
        if dir_str in self._rules_cache:
            del self._rules_cache[dir_str]
        if dir_str in self._pathspec_cache:
            del self._pathspec_cache[dir_str]

        return file_path

    def is_context_file(self, path: Union[str, Path]) -> Tuple[bool, Optional[Dict[str, str]]]:
        """
        Check if a file is marked as a context file.

        Args:
            path: Path to the file

        Returns:
            Tuple of (is_context, metadata)
        """
        rules = self.get_applicable_rules(path)

        for rule in rules:
            if rule.permission == GuardPermission.context:
                return True, rule.context_metadata

        return False, None

    def get_context_files(self, directory: Union[str, Path], recursive: bool = True) -> List[Dict]:
        """
        Get all context files in a directory.

        Args:
            directory: Directory to search
            recursive: Whether to search subdirectories

        Returns:
            List of context file information
        """
        directory = Path(directory)
        context_files = []

        # Get all files in directory
        if recursive:
            files = list(directory.rglob("*"))
        else:
            files = [f for f in directory.iterdir() if f.is_file()]

        # Check each file
        for file_path in files:
            if file_path.is_file():
                is_context, metadata = self.is_context_file(file_path)
                if is_context:
                    context_files.append({"path": str(file_path), "metadata": metadata or {}})

        return context_files


def get_effective_permissions(
    path: Union[str, Path],
    repo_path: Optional[Union[str, Path]] = None,
    verbose: bool = False,
    identifier: Optional[str] = None,
) -> Dict:
    """
    Get effective permissions for a path.

    Args:
        path: Path to get permissions for
        repo_path: Repository root path
        verbose: Whether to include detailed source information
        identifier: Specific identifier (e.g., "claude-4")

    Returns:
        Dictionary with permissions information
    """
    guard = DirectoryGuard(repo_path)

    if verbose:
        return guard.get_permissions_with_sources(path)
    else:
        # Get permissions for both AI and human
        ai_perms = guard.get_effective_permissions(path, "ai", identifier)
        human_perms = guard.get_effective_permissions(path, "human", identifier)

        # Check if it's a context file
        is_context, context_metadata = guard.is_context_file(path)

        # Format to readable form
        result = {
            "path": str(path),
            "type": "file" if Path(path).is_file() else "directory",
            "permissions": {
                "ai": guard._permission_to_readable(ai_perms["permission"]),
                "human": guard._permission_to_readable(human_perms["permission"]),
            },
            "is_context": is_context,
            "code": f"{ai_perms['who'].value}:{ai_perms['permission'].value}",
            "status": "success",
        }

        if is_context and context_metadata:
            result["context_metadata"] = context_metadata

        return result
