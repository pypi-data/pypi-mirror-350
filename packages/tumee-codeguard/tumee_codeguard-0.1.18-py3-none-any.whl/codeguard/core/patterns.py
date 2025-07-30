"""
Custom pattern classes for extensible pattern matching.

This module provides custom pattern classes that extend pathspec's functionality
for CodeGuard-specific use cases.
"""

import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern


class GuardPattern(GitWildMatchPattern):
    """
    Custom pattern class for guard-specific matching logic.

    Extends GitWildMatchPattern to add metadata and custom behavior.
    """

    def __init__(self, pattern: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a guard pattern.

        Args:
            pattern: The pattern string (gitignore-style)
            metadata: Optional metadata associated with the pattern
        """
        super().__init__(pattern)
        self.metadata = metadata or {}
        self.original_pattern = pattern

    def __repr__(self) -> str:
        """String representation."""
        return f"GuardPattern({self.original_pattern!r}, metadata={self.metadata!r})"


class PermissionPattern(GuardPattern):
    """
    Pattern that includes permission metadata.

    This pattern type associates guard permissions with file patterns.
    """

    def __init__(self, pattern: str, permission: str, who: str, description: str = ""):
        """
        Initialize a permission pattern.

        Args:
            pattern: The file pattern
            permission: Permission level (r, w, n)
            who: Who the permission applies to (ai, hu, all)
            description: Optional description
        """
        metadata = {"permission": permission, "who": who, "description": description}
        super().__init__(pattern, metadata)
        self.permission = permission
        self.who = who
        self.description = description

    def __repr__(self) -> str:
        """String representation."""
        return f"PermissionPattern({self.original_pattern!r}, {self.who}:{self.permission})"


class ConditionalPattern(GuardPattern):
    """
    Pattern that only matches under certain conditions.

    This allows for dynamic pattern matching based on runtime conditions.
    """

    def __init__(
        self,
        pattern: str,
        condition: Callable[[str], bool],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a conditional pattern.

        Args:
            pattern: The file pattern
            condition: A callable that takes a filepath and returns True if the condition is met
            metadata: Optional metadata
        """
        super().__init__(pattern, metadata)
        self.condition = condition

    def match(self, path: Union[str, Path]) -> Optional[Any]:
        """
        Match the path against the pattern with condition check.

        Args:
            path: Path to match

        Returns:
            Match result if pattern matches and condition is met, None otherwise
        """
        # First check the condition
        if not self.condition(str(path)):
            return None

        # Then perform normal pattern matching
        return super().match(path)


class SizePattern(ConditionalPattern):
    """
    Pattern that matches files based on size constraints.

    Example patterns:
        "*.log:size>1MB" - Log files larger than 1MB
        "*.tmp:size<100KB" - Temp files smaller than 100KB
    """

    def __init__(self, pattern: str, size_condition: str):
        """
        Initialize a size-based pattern.

        Args:
            pattern: The file pattern
            size_condition: Size condition (e.g., ">1MB", "<100KB", "=0")
        """
        # Parse size condition
        match = re.match(r"([<>=]+)(\d+)([KMG]?B)?", size_condition)
        if not match:
            raise ValueError(f"Invalid size condition: {size_condition}")

        operator, size_str, unit = match.groups()

        # Convert to bytes
        size = int(size_str)
        if unit:
            multipliers = {"KB": 1024, "MB": 1024**2, "GB": 1024**3, "B": 1}
            size *= multipliers.get(unit, 1)

        # Create condition function
        def check_size(filepath: str) -> bool:
            try:
                file_size = Path(filepath).stat().st_size
                if operator == ">":
                    return file_size > size
                elif operator == "<":
                    return file_size < size
                elif operator == "=":
                    return file_size == size
                elif operator == ">=":
                    return file_size >= size
                elif operator == "<=":
                    return file_size <= size
                return False
            except (OSError, IOError):
                return False

        metadata = {"size_condition": size_condition, "size_bytes": size}
        super().__init__(pattern, check_size, metadata)
        self.size_condition = size_condition


class ContentPattern(ConditionalPattern):
    """
    Pattern that matches files based on content.

    Example patterns:
        "*.py:contains:TODO" - Python files containing TODO
        "*.js:regex:function\\s+async" - JS files with async functions
    """

    def __init__(self, pattern: str, content_check: str, check_type: str = "contains"):
        """
        Initialize a content-based pattern.

        Args:
            pattern: The file pattern
            content_check: String or regex to search for
            check_type: Type of check ("contains" or "regex")
        """

        # Create condition function
        def check_content(filepath: str) -> bool:
            try:
                content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
                if check_type == "contains":
                    return content_check in content
                elif check_type == "regex":
                    return bool(re.search(content_check, content))
                return False
            except (OSError, IOError):
                return False

        metadata = {"content_check": content_check, "check_type": check_type}
        super().__init__(pattern, check_content, metadata)
        self.content_check = content_check
        self.check_type = check_type


class ExtensionPattern(GuardPattern):
    """
    Pattern specifically for file extensions with special handling.

    Supports multiple extensions and exclusions.
    Example: "*.{py,js,ts}" or "!*.min.js"
    """

    def __init__(self, extensions: Union[str, List[str]], exclude: bool = False):
        """
        Initialize an extension pattern.

        Args:
            extensions: Single extension or list of extensions
            exclude: Whether this is an exclusion pattern
        """
        if isinstance(extensions, str):
            extensions = [extensions]

        # Build pattern
        if len(extensions) == 1:
            pattern = f"*.{extensions[0]}"
        else:
            pattern = f"*.{{{','.join(extensions)}}}"

        if exclude:
            pattern = f"!{pattern}"

        metadata = {"extensions": extensions, "exclude": exclude}
        super().__init__(pattern, metadata)
        self.extensions = extensions
        self.exclude = exclude


class PatternFactory:
    """Factory for creating appropriate pattern types from strings."""

    @staticmethod
    def create_pattern(pattern_str: str, **kwargs) -> GuardPattern:
        """
        Create a pattern object from a pattern string.

        Args:
            pattern_str: The pattern string, possibly with modifiers
            **kwargs: Additional arguments for pattern creation

        Returns:
            Appropriate GuardPattern subclass instance
        """
        # Check for size patterns
        if ":size" in pattern_str:
            parts = pattern_str.split(":size", 1)
            if len(parts) == 2:
                return SizePattern(parts[0], parts[1])

        # Check for content patterns
        if ":contains:" in pattern_str:
            parts = pattern_str.split(":contains:", 1)
            if len(parts) == 2:
                return ContentPattern(parts[0], parts[1], "contains")

        if ":regex:" in pattern_str:
            parts = pattern_str.split(":regex:", 1)
            if len(parts) == 2:
                return ContentPattern(parts[0], parts[1], "regex")

        # Check for permission patterns (from kwargs)
        if "permission" in kwargs and "who" in kwargs:
            return PermissionPattern(
                pattern_str, kwargs["permission"], kwargs["who"], kwargs.get("description", "")
            )

        # Default to GuardPattern
        return GuardPattern(pattern_str, kwargs)


def compile_patterns(patterns: List[Union[str, GuardPattern]]) -> PathSpec:
    """
    Compile a list of patterns into a PathSpec.

    Args:
        patterns: List of pattern strings or GuardPattern objects

    Returns:
        Compiled PathSpec object
    """
    # Convert all to GuardPattern objects if needed
    guard_patterns = []
    for p in patterns:
        if isinstance(p, str):
            guard_patterns.append(PatternFactory.create_pattern(p))
        else:
            guard_patterns.append(p)

    # Create PathSpec with our custom patterns
    return PathSpec(guard_patterns)
