"""
Hash calculation utilities for CodeGuard.

This module provides utilities for normalizing code content and calculating
cryptographic hashes to detect unauthorized changes to guarded regions.
"""

import hashlib
import re
from typing import List, Tuple


class HashCalculator:
    """
    Utility class for calculating cryptographic hashes of code regions.

    This class handles normalization of code content to avoid false positives
    due to whitespace changes, line ending differences, and other non-semantic
    modifications.
    """

    # Constants
    TAB_WIDTH = 4  # Standard tab width for conversion to spaces

    def __init__(
        self,
        normalize_whitespace: bool = True,
        normalize_line_endings: bool = True,
        ignore_blank_lines: bool = True,
        ignore_indentation: bool = False,
        ignore_comments: bool = False,
    ):
        """
        Initialize the hash calculator.

        Args:
            normalize_whitespace: Whether to normalize whitespace (default: True)
            normalize_line_endings: Whether to normalize line endings (default: True)
            ignore_blank_lines: Whether to ignore blank lines (default: True)
            ignore_indentation: Whether to ignore indentation changes (default: False)
            ignore_comments: Whether to ignore comments (default: False)
        """
        self.normalize_whitespace = normalize_whitespace
        self.normalize_line_endings = normalize_line_endings
        self.ignore_blank_lines = ignore_blank_lines
        self.ignore_indentation = ignore_indentation
        self.ignore_comments = ignore_comments

    def normalize_content(self, content: str) -> str:
        """
        Normalize code content to prevent false positives.

        Args:
            content: Code content to normalize

        Returns:
            Normalized content
        """
        if not content:
            return ""

        normalized = content

        if self.normalize_line_endings:
            # Convert all line endings to '\n'
            normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")

        # Split into lines for per-line processing
        lines = normalized.split("\n")
        processed_lines = []

        for line in lines:
            # Skip blank lines if configured to do so
            if self.ignore_blank_lines and not line.strip():
                continue

            # Process each line
            if self.normalize_whitespace:
                # Normalize tabs to spaces
                processed_line = line.replace("\t", " " * self.TAB_WIDTH)

                # Remove trailing whitespace
                processed_line = processed_line.rstrip()

                # Remove indentation if configured to do so
                if self.ignore_indentation:
                    processed_line = processed_line.lstrip()
            else:
                processed_line = line

            processed_lines.append(processed_line)

        # Rejoin lines
        normalized = "\n".join(processed_lines)

        if self.normalize_whitespace:
            # Remove consecutive blank lines
            normalized = re.sub(r"\n{3,}", "\n\n", normalized)

        return normalized

    def calculate_hash(self, content: str) -> str:
        """
        Calculate cryptographic hash for code content.

        Args:
            content: Code content to hash

        Returns:
            Hexadecimal string representation of the hash
        """
        # Normalize content first
        normalized_content = self.normalize_content(content)

        # Calculate SHA-256 hash
        return hashlib.sha256(normalized_content.encode("utf-8")).hexdigest()

    def calculate_region_hash(self, content: str, start_line: int, end_line: int) -> str:
        """
        Calculate hash for a specific region in the code.

        Args:
            content: Full code content
            start_line: Region start line (1-based)
            end_line: Region end line (1-based)

        Returns:
            Hexadecimal string representation of the hash
        """
        lines = content.split("\n")

        # Adjust for 0-based indexing
        start_idx = max(0, start_line - 1)
        end_idx = min(len(lines), end_line)

        # Extract region content
        region_content = "\n".join(lines[start_idx:end_idx])

        # Calculate hash for the region
        return self.calculate_hash(region_content)

    def compare_content(self, original: str, modified: str) -> Tuple[bool, str, str]:
        """
        Compare original and modified content and generate hashes.

        Args:
            original: Original content
            modified: Modified content

        Returns:
            Tuple of (is_changed, original_hash, modified_hash)
        """
        # Normalize both contents
        normalized_original = self.normalize_content(original)
        normalized_modified = self.normalize_content(modified)

        # Calculate hashes
        original_hash = hashlib.sha256(normalized_original.encode("utf-8")).hexdigest()
        modified_hash = hashlib.sha256(normalized_modified.encode("utf-8")).hexdigest()

        # Determine if content has changed
        is_changed = original_hash != modified_hash

        return is_changed, original_hash, modified_hash

    def get_diff_lines(self, original: str, modified: str) -> List[Tuple[str, str]]:
        """
        Get a simple line-by-line diff between original and modified content.

        This is a basic implementation that doesn't handle complex diffs like
        additions or deletions that change line numbers. It's intended to provide
        context for simple changes.

        Args:
            original: Original content
            modified: Modified content

        Returns:
            List of (original_line, modified_line) tuples for changed lines
        """
        # Normalize both contents
        normalized_original = self.normalize_content(original)
        normalized_modified = self.normalize_content(modified)

        # Split into lines
        original_lines = normalized_original.split("\n")
        modified_lines = normalized_modified.split("\n")

        # Find changed lines
        diffs = []
        for i in range(min(len(original_lines), len(modified_lines))):
            if original_lines[i] != modified_lines[i]:
                diffs.append((original_lines[i], modified_lines[i]))

        # Handle different line counts
        if len(original_lines) < len(modified_lines):
            # Lines were added
            for i in range(len(original_lines), len(modified_lines)):
                diffs.append(("", modified_lines[i]))
        elif len(original_lines) > len(modified_lines):
            # Lines were removed
            for i in range(len(modified_lines), len(original_lines)):
                diffs.append((original_lines[i], ""))

        return diffs
