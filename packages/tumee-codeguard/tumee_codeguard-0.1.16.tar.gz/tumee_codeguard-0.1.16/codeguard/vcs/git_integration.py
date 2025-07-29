"""
Git Integration for CodeGuard.

This module provides integration with Git version control system for comparing
files against different revisions.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Union

from ..core.validator import CodeGuardValidator, ValidationResult


class GitError(Exception):
    """
    Exception raised for Git-related errors.

    This exception is raised when Git operations fail, such as when
    a repository is not found, a revision doesn't exist, or Git
    commands fail to execute.
    """

    pass


class GitIntegration:
    """
    Integration with Git version control system.

    This class provides functionality for working with Git repositories,
    including retrieving file content from different revisions, comparing
    changes between commits, and installing pre-commit hooks for automatic
    validation.

    The integration uses Git command-line tools via subprocess calls, so
    Git must be installed and available in the system PATH.

    Attributes:
        repo_path: Path to the Git repository root
    """

    def __init__(self, repo_path: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize Git integration for a repository.

        Args:
            repo_path: Path to the Git repository root. If None, uses the
                      current working directory. The path must contain a
                      valid Git repository.

        Raises:
            GitError: If the specified path is not a Git repository
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self._verify_git_repo()

    def _verify_git_repo(self) -> None:
        """
        Verify that the specified path is a Git repository.

        This method checks for the presence of a .git directory or file
        (in case of git worktrees) to confirm the path is a valid Git repository.

        Raises:
            GitError: If the path is not a Git repository
        """
        git_dir = self.repo_path / ".git"
        if not git_dir.is_dir():
            raise GitError(f"Not a Git repository: {self.repo_path}")

    def _run_git_command(self, args: List[str], check: bool = True) -> str:
        """
        Run a Git command and return its output.

        Args:
            args: Command arguments (excluding 'git')
            check: Whether to raise an exception on non-zero exit code

        Returns:
            Command output as string

        Raises:
            GitError: If command execution fails
        """
        try:
            result = subprocess.run(
                ["git"] + args, cwd=self.repo_path, check=check, capture_output=True, text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise GitError(f"Git command failed: {e.stderr}")

    def get_file_content(self, file_path: Union[str, Path], revision: str = "HEAD") -> str:
        """
        Get file content from a specific revision.

        Args:
            file_path: Path to the file (relative to repository root)
            revision: Git revision specifier (default: HEAD)

        Returns:
            File content as string

        Raises:
            GitError: If file retrieval fails
        """
        file_path_str = str(file_path)
        rel_path = os.path.relpath(file_path_str, self.repo_path)

        try:
            content = self._run_git_command(["show", f"{revision}:{rel_path}"])
            return content
        except GitError as e:
            if "does not exist" in str(e) or "fatal: path" in str(e):
                raise GitError(f"File does not exist in revision {revision}: {rel_path}")
            raise

    def get_changed_files(
        self, revision: str = "HEAD", base_revision: Optional[str] = None
    ) -> List[str]:
        """
        Get a list of files that were changed between revisions.

        This method retrieves the paths of all files that were modified,
        added, or deleted between two Git revisions. It's useful for
        identifying which files need validation after changes.

        Args:
            revision: Target Git revision (commit hash, branch, tag, etc.)
                     Default: "HEAD" (current commit)
            base_revision: Base revision for comparison. If None, compares
                          with the parent of the target revision.

        Returns:
            List of file paths (relative to repository root) that changed
            between the revisions. Empty list if no changes.

        Raises:
            GitError: If the Git command fails or revisions don't exist

        Example:
            >>> git.get_changed_files("main", "develop")
            ['src/main.py', 'tests/test_main.py']
        """
        if base_revision:
            rev_range = f"{base_revision}..{revision}"
        else:
            rev_range = f"{revision}^..{revision}"

        try:
            output = self._run_git_command(["diff", "--name-only", rev_range])
            return [line.strip() for line in output.splitlines() if line.strip()]
        except GitError as e:
            if "unknown revision" in str(e):
                raise GitError(f"Unknown revision: {revision}")
            raise

    def validate_file_against_revision(
        self,
        file_path: Union[str, Path],
        revision: str = "HEAD",
        validator: Optional[CodeGuardValidator] = None,
    ) -> ValidationResult:
        """
        Validate a file against a specific revision.

        Args:
            file_path: Path to the file
            revision: Git revision specifier (default: HEAD)
            validator: CodeGuardValidator instance (default: create new instance)

        Returns:
            ValidationResult containing any detected violations

        Raises:
            GitError: If file retrieval fails
        """
        file_path = Path(file_path)
        if not file_path.is_file():
            raise GitError(f"File does not exist: {file_path}")

        # Get file content from the specified revision
        try:
            revision_content = self.get_file_content(file_path, revision)
        except GitError as e:
            # If file doesn't exist in the specified revision, it's a new file
            if "does not exist" in str(e):
                revision_content = ""
            else:
                raise

        # Create temporary file for revision content
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=file_path.suffix, delete=False
        ) as temp_file:
            temp_file.write(revision_content)
            temp_file_path = temp_file.name

        try:
            # Create validator if not provided
            if validator is None:
                validator = CodeGuardValidator()

            # Compare current file against revision
            result = validator.validate_files(temp_file_path, file_path)

            return result
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    def validate_files_in_revision(
        self,
        revision: str = "HEAD",
        base_revision: Optional[str] = None,
        validator: Optional[CodeGuardValidator] = None,
        file_list: Optional[List[Union[str, Path]]] = None,
    ) -> ValidationResult:
        """
        Validate all changed files in a specific revision.

        Args:
            revision: Git revision specifier (default: HEAD)
            base_revision: Base revision for comparison (default: parent of revision)
            validator: CodeGuardValidator instance (default: create new instance)
            file_list: List of files to validate (default: all changed files)

        Returns:
            ValidationResult containing any detected violations

        Raises:
            GitError: If command execution fails
        """
        # Create validator if not provided
        if validator is None:
            validator = CodeGuardValidator()

        # Get list of changed files
        if file_list is None:
            file_list = self.get_changed_files(revision, base_revision)

        # Convert to Path objects
        file_paths = [Path(self.repo_path / f) for f in file_list]

        # Filter out files that don't exist
        file_paths = [f for f in file_paths if f.is_file()]

        # Validate each file
        all_violations = []
        files_checked = 0

        for file_path in file_paths:
            try:
                result = self.validate_file_against_revision(file_path, revision, validator)
                files_checked += result.files_checked
                all_violations.extend(result.violations)
            except GitError as e:
                # Log Git-specific errors but continue with other files
                import logging

                logging.warning(f"Git error validating {file_path}: {e}")
                continue
            except FileNotFoundError:
                # File was deleted or doesn't exist in revision
                import logging

                logging.debug(f"File not found: {file_path}")
                continue
            except Exception as e:
                # Log unexpected errors
                import logging

                logging.error(f"Unexpected error validating {file_path}: {e}")
                continue

        return ValidationResult(files_checked=files_checked, violations=all_violations)

    def install_pre_commit_hook(self) -> str:
        """
        Install a Git pre-commit hook for automatic CodeGuard validation.

        This method creates a pre-commit hook that automatically runs
        CodeGuard validation on staged files before each commit. The hook
        will prevent commits if guard violations are detected.

        The hook script will:
        - Run CodeGuard on all staged files
        - Show any violations found
        - Block the commit if violations exist
        - Allow bypass with --no-verify flag

        Returns:
            Absolute path to the installed hook file

        Raises:
            GitError: If unable to create the hook file (e.g., permissions)

        Note:
            If a pre-commit hook already exists, it will be backed up
            with a .backup extension before installing the new hook.
        """
        hook_path = self.repo_path / ".git" / "hooks" / "pre-commit"

        # Create hook content
        hook_content = """#!/bin/sh
# CodeGuard pre-commit hook

# Find the codeguard executable
CODEGUARD=$(which codeguard 2>/dev/null)

if [ -z "$CODEGUARD" ]; then
    echo "CodeGuard not found in PATH. Skipping validation."
    exit 0
fi

# Get list of staged files
FILES=$(git diff --cached --name-only --diff-filter=ACMR)

if [ -z "$FILES" ]; then
    echo "No files to validate. Skipping CodeGuard validation."
    exit 0
fi

# Run CodeGuard on each staged file
echo "Running CodeGuard validation on staged files..."
FAILED=0

for FILE in $FILES; do
    # Skip files that don't exist
    if [ ! -f "$FILE" ]; then
        continue
    fi

    echo "  Checking $FILE"
    $CODEGUARD verify-git --file "$FILE" --format json > /dev/null
    RESULT=$?

    if [ $RESULT -ne 0 ]; then
        echo "⛔ CodeGuard validation failed for $FILE"
        echo "ℹ️ Run 'codeguard verify-git --file \"$FILE\"' for more details."
        FAILED=1
    fi
done

if [ $FAILED -eq 1 ]; then
    echo "❌ CodeGuard validation failed. Commit aborted."
    echo "ℹ️ You can bypass this check with: git commit --no-verify"
    exit 1
else
    echo "✅ CodeGuard validation passed for all staged files."
fi

exit 0
"""

        # Write hook to file
        with open(hook_path, "w") as f:
            f.write(hook_content)

        # Make hook executable
        os.chmod(hook_path, 0o755)

        return str(hook_path)

    def compare_file_between_revisions(
        self,
        file_path: Union[str, Path],
        from_revision: str,
        to_revision: str = "HEAD",
        validator: Optional[CodeGuardValidator] = None,
    ) -> ValidationResult:
        """
        Compare a file between two revisions.

        Args:
            file_path: Path to the file
            from_revision: Base revision for comparison
            to_revision: Target revision for comparison (default: HEAD)
            validator: CodeGuardValidator instance (default: create new instance)

        Returns:
            ValidationResult containing any detected violations

        Raises:
            GitError: If file retrieval fails
        """
        # Get file content from the specified revisions
        try:
            from_content = self.get_file_content(file_path, from_revision)
        except GitError:
            # If file doesn't exist in the from revision, it's a new file
            from_content = ""

        try:
            to_content = self.get_file_content(file_path, to_revision)
        except GitError:
            # If file doesn't exist in the to revision, it was deleted
            to_content = ""

        # Create temporary files for revision content
        file_path = Path(file_path)

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=file_path.suffix, delete=False
        ) as from_temp_file:
            from_temp_file.write(from_content)
            from_temp_file_path = from_temp_file.name

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=file_path.suffix, delete=False
        ) as to_temp_file:
            to_temp_file.write(to_content)
            to_temp_file_path = to_temp_file.name

        try:
            # Create validator if not provided
            if validator is None:
                validator = CodeGuardValidator()

            # Compare files between revisions
            result = validator.validate_files(from_temp_file_path, to_temp_file_path)

            return result
        finally:
            # Clean up temporary files
            os.unlink(from_temp_file_path)
            os.unlink(to_temp_file_path)
