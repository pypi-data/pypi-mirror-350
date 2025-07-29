#!/usr/bin/env python3
"""
CodeGuard - Code Change Detection and Guard Validation Tool

This tool identifies, tracks, and validates code modifications with a focus on
respecting designated "guarded" regions across multiple programming languages.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

from .core.validator import CodeGuardValidator
from .utils.logging_config import get_logger
from .utils.reporter import Reporter
from .vcs.git_integration import GitError, GitIntegration
from .version import __version__

# Set up module logger
logger = get_logger(__name__)

# Constants
DEFAULT_MAX_CONTENT_LINES = 10
DEFAULT_MCP_PORT = 8000
DEFAULT_MCP_HOST = "127.0.0.1"


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CodeGuard CLI.

    Args:
        args: Command line arguments (defaults to sys.argv if None)

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    if args is None:
        args = sys.argv[1:]

    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # Handle -acl shorthand option
    if hasattr(parsed_args, "acl") and parsed_args.acl:
        # Create a new Namespace with the acl command arguments
        acl_args = argparse.Namespace(
            path=parsed_args.acl,
            verbose=getattr(parsed_args, "verbose", 0) > 0,
            recursive=False,
            format="json",
            repo_path=None,
        )
        return cmd_acl(acl_args)

    # If no subcommand is provided, show help
    if not hasattr(parsed_args, "func"):
        parser.print_help()
        return 1

    # Execute the appropriate function for the subcommand
    try:
        return parsed_args.func(parsed_args)
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """
    Create the command-line argument parser.

    Returns:
        Configured ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        prog="codeguard",
        description="Code Change Detection and Guard Validation Tool",
        epilog="For more information, visit: https://github.com/TuMee-Dev/TuMee-Code-Validator",
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # Global options
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity level (can be repeated)",
    )

    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress non-error output")

    parser.add_argument(
        "-f",
        "--format",
        choices=["json", "yaml", "text", "html", "markdown", "console"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--console-style",
        choices=["plain", "minimal", "detailed", "compact"],
        default="detailed",
        help="Style for console output (default: detailed)",
    )

    parser.add_argument(
        "--no-content", action="store_true", help="Don't include content in reports"
    )

    parser.add_argument("--no-diff", action="store_true", help="Don't include diffs in reports")

    parser.add_argument(
        "--max-content-lines",
        type=int,
        default=10,
        help="Maximum number of content lines to include in reports (default: 10)",
    )

    parser.add_argument("--output", help="Output file path (if not provided, output to stdout)")

    parser.add_argument(
        "--target",
        choices=["ai", "human", "all", "AI", "HU", "ALL"],
        default="ai",
        help="Target audience for guard checks (default: ai)",
    )

    parser.add_argument(
        "--context-lines",
        type=int,
        default=3,
        help="Number of context lines to include around changes in violations (default: 3)",
    )

    parser.add_argument(
        "--normalize-whitespace",
        action="store_true",
        default=True,
        help="Normalize whitespace in comparisons (default: True)",
    )

    parser.add_argument(
        "--normalize-line-endings",
        action="store_true",
        default=True,
        help="Normalize line endings in comparisons (default: True)",
    )

    parser.add_argument(
        "--ignore-blank-lines",
        action="store_true",
        default=True,
        help="Ignore blank lines in comparisons (default: True)",
    )

    parser.add_argument(
        "--ignore-indentation",
        action="store_true",
        default=False,
        help="Ignore indentation changes in comparisons (default: False)",
    )

    # Add -acl as a global shorthand option for ACL information retrieval
    parser.add_argument(
        "-acl",
        metavar="PATH",
        help="Get effective permissions for a path (shorthand for 'acl' command)",
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # ACL Information Command
    acl_parser = subparsers.add_parser(
        "acl", help="Get effective permissions for a file or directory"
    )
    acl_parser.add_argument("path", help="Path to get permissions for")
    acl_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Include detailed source information"
    )
    acl_parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively check children (for directories)",
    )
    acl_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "yaml", "text"],
        default="json",
        help="Output format (default: json)",
    )
    acl_parser.add_argument("--repo-path", help="Repository root path (default: autodetect)")
    acl_parser.add_argument(
        "--identifier", help="Specific identifier (e.g., claude-4, security-team)"
    )
    acl_parser.add_argument(
        "--include-context", action="store_true", help="Include context file information"
    )
    acl_parser.set_defaults(func=cmd_acl)

    # Batch ACL Information Command
    batch_acl_parser = subparsers.add_parser(
        "batch-acl", help="Get permissions for multiple paths in a batch"
    )
    batch_acl_parser.add_argument("paths", nargs="+", help="Paths to get permissions for")
    batch_acl_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Include detailed source information"
    )
    batch_acl_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "yaml", "text"],
        default="json",
        help="Output format (default: json)",
    )
    batch_acl_parser.add_argument("--repo-path", help="Repository root path (default: autodetect)")
    batch_acl_parser.set_defaults(func=cmd_batch_acl)

    # Context Files Commands
    context_parser = subparsers.add_parser("context", help="Get context files for a directory")
    context_parser.add_argument("directory", help="Directory to search for context files")
    context_parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        default=True,
        help="Search subdirectories (default: True)",
    )
    context_parser.add_argument(
        "--priority", choices=["high", "medium", "low"], help="Filter by priority level"
    )
    context_parser.add_argument(
        "--for", dest="for_use", help="Filter by usage scope (e.g., testing, configuration)"
    )
    context_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "yaml", "text"],
        default="text",
        help="Output format (default: text)",
    )
    context_parser.add_argument("--repo-path", help="Repository root path (default: autodetect)")
    context_parser.set_defaults(func=cmd_context)

    # List All Context Files
    list_context_parser = subparsers.add_parser(
        "list-context", help="List all context files in the project"
    )
    list_context_parser.add_argument(
        "--directory", default=".", help="Starting directory (default: current directory)"
    )
    list_context_parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        default=True,
        help="Search subdirectories (default: True)",
    )
    list_context_parser.add_argument(
        "--priority", choices=["high", "medium", "low"], help="Filter by priority level"
    )
    list_context_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "yaml", "text"],
        default="text",
        help="Output format (default: text)",
    )
    list_context_parser.add_argument(
        "--repo-path", help="Repository root path (default: autodetect)"
    )
    list_context_parser.set_defaults(func=cmd_list_context)

    # Directory Guard Management Commands
    dir_guard_cmd = subparsers.add_parser(
        "aiattributes", help="Manage directory-level guard annotations via .ai-attributes files"
    )
    dir_guard_subparsers = dir_guard_cmd.add_subparsers(title="actions", dest="action")

    # Create .ai-attributes file
    create_attrs_parser = dir_guard_subparsers.add_parser(
        "create", help="Create or update an .ai-attributes file"
    )
    create_attrs_parser.add_argument(
        "--directory",
        default=".",
        help="Directory to create .ai-attributes in (default: current directory)",
    )
    create_attrs_parser.add_argument(
        "--rule",
        action="append",
        help="Add a rule in the format 'pattern:guard' (e.g. '*.py:AI-RO'). Can be specified multiple times.",
    )
    create_attrs_parser.add_argument(
        "--description",
        action="append",
        help="Add a description in the format 'pattern:description'. Can be specified multiple times.",
    )
    create_attrs_parser.set_defaults(func=cmd_create_aiattributes)

    # List rules from .ai-attributes files
    list_attrs_parser = dir_guard_subparsers.add_parser(
        "list", help="List rules from .ai-attributes files"
    )
    list_attrs_parser.add_argument(
        "--directory", default=".", help="Directory to start from (default: current directory)"
    )
    list_attrs_parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively list rules from all .ai-attributes files in the directory tree",
    )
    list_attrs_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "yaml", "text"],
        default="text",
        help="Output format (default: text)",
    )
    list_attrs_parser.set_defaults(func=cmd_list_aiattributes)

    # Validate .ai-attributes files
    validate_attrs_parser = dir_guard_subparsers.add_parser(
        "validate", help="Validate .ai-attributes files"
    )
    validate_attrs_parser.add_argument(
        "--directory", default=".", help="Directory to start from (default: current directory)"
    )
    validate_attrs_parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively validate all .ai-attributes files in the directory tree",
    )
    validate_attrs_parser.add_argument(
        "--fix", action="store_true", help="Attempt to fix invalid .ai-attributes files"
    )
    validate_attrs_parser.set_defaults(func=cmd_validate_aiattributes)

    # Show directory with guard annotations
    show_guarded_dirs_parser = subparsers.add_parser(
        "list-guarded-directories", help="List directories with guard annotations"
    )
    show_guarded_dirs_parser.add_argument(
        "--directory", default=".", help="Directory to start from (default: current directory)"
    )
    show_guarded_dirs_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "yaml", "text"],
        default="text",
        help="Output format (default: text)",
    )
    show_guarded_dirs_parser.set_defaults(func=cmd_list_guarded_directories)

    # verify command
    verify_parser = subparsers.add_parser("verify", help="Compare two files directly")
    verify_parser.add_argument("--original", required=True, help="Path to original file")
    verify_parser.add_argument("--modified", required=True, help="Path to modified file")
    verify_parser.add_argument("--report", help="Path to save report")
    verify_parser.set_defaults(func=cmd_verify)

    # verify-disk command
    verify_disk_parser = subparsers.add_parser(
        "verify-disk", help="Compare modified file against current version on disk"
    )
    verify_disk_parser.add_argument("--modified", required=True, help="Path to modified file")
    verify_disk_parser.add_argument("--report", help="Path to save report")
    verify_disk_parser.set_defaults(func=cmd_verify_disk)

    # verify-git command
    verify_git_parser = subparsers.add_parser(
        "verify-git", help="Compare against last checked-in version in git"
    )
    verify_git_parser.add_argument("--file", required=True, help="Path to file")
    verify_git_parser.add_argument(
        "--revision", default="HEAD", help="Git revision to compare against (default: HEAD)"
    )
    verify_git_parser.add_argument(
        "--repo-path", help="Path to git repository (default: autodetect)"
    )
    verify_git_parser.add_argument("--report", help="Path to save report")
    verify_git_parser.set_defaults(func=cmd_verify_git)

    # verify-revision command
    verify_revision_parser = subparsers.add_parser(
        "verify-revision", help="Compare against specific revision"
    )
    verify_revision_parser.add_argument("--file", required=True, help="Path to file")
    verify_revision_parser.add_argument(
        "--from-revision", required=True, help="Base revision for comparison"
    )
    verify_revision_parser.add_argument(
        "--to-revision", default="HEAD", help="Target revision for comparison (default: HEAD)"
    )
    verify_revision_parser.add_argument(
        "--repo-path", help="Path to git repository (default: autodetect)"
    )
    verify_revision_parser.add_argument("--report", help="Path to save report")
    verify_revision_parser.set_defaults(func=cmd_verify_revision)

    # scan command
    scan_parser = subparsers.add_parser("scan", help="Batch operations on directories")
    scan_parser.add_argument("--directory", required=True, help="Path to directory")
    scan_parser.add_argument(
        "--report-format",
        choices=["json", "yaml", "text", "html", "markdown", "console"],
        default="text",
        help="Format for report",
    )
    scan_parser.add_argument("--include", help="Glob pattern to include files")
    scan_parser.add_argument("--exclude", help="Glob pattern to exclude files")
    scan_parser.add_argument("--report", help="Path to save report")
    scan_parser.set_defaults(func=cmd_scan)

    # install-hook command
    install_hook_parser = subparsers.add_parser("install-hook", help="Install git pre-commit hook")
    install_hook_parser.add_argument(
        "--git-repo", help="Path to git repository (default: current directory)"
    )
    install_hook_parser.set_defaults(func=cmd_install_hook)

    # serve command
    serve_parser = subparsers.add_parser("serve", help="Start MCP server")
    serve_parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_MCP_PORT,
        help=f"Port to listen on (default: {DEFAULT_MCP_PORT})",
    )
    serve_parser.add_argument(
        "--host", default=DEFAULT_MCP_HOST, help="Host to bind to (default: 127.0.0.1)"
    )
    serve_parser.add_argument("--config", help="Path to config file")
    serve_parser.set_defaults(func=cmd_serve)

    # validate-sections command
    validate_sections_parser = subparsers.add_parser(
        "validate-sections",
        help="Validate that external tool's guard section parsing matches our internal parsing",
    )
    validate_sections_parser.add_argument(
        "--json-file", required=True, help="Path to JSON validation request file from external tool"
    )
    validate_sections_parser.add_argument(
        "--file", help="Optional override for source file path (defaults to path specified in JSON)"
    )
    validate_sections_parser.set_defaults(func=cmd_validate_sections)

    return parser


def create_validator_from_args(args: argparse.Namespace) -> CodeGuardValidator:
    """
    Create a CodeGuardValidator instance from command-line arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Configured CodeGuardValidator instance
    """
    return CodeGuardValidator(
        normalize_whitespace=args.normalize_whitespace,
        normalize_line_endings=args.normalize_line_endings,
        ignore_blank_lines=args.ignore_blank_lines,
        ignore_indentation=args.ignore_indentation,
        target=args.target,
        context_lines=args.context_lines,
    )


def create_reporter_from_args(args: argparse.Namespace) -> Reporter:
    """
    Create a Reporter instance from command-line arguments.

    Args:
        args: Parsed command-line arguments

    Returns:
        Configured Reporter instance
    """
    # Determine output file
    output_file = args.output

    # For command-specific report paths
    if hasattr(args, "report") and args.report:
        output_file = args.report

    # Determine format
    report_format = args.format

    # For scan command's report format
    if hasattr(args, "report_format") and args.report_format:
        report_format = args.report_format

    return Reporter(
        format=report_format,
        output_file=output_file,
        console_style=args.console_style,
        include_content=not args.no_content,
        include_diff=not args.no_diff,
        max_content_lines=args.max_content_lines,
    )


def cmd_verify(args: argparse.Namespace) -> int:
    """
    Execute the 'verify' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    original_path = Path(args.original)
    modified_path = Path(args.modified)

    if not original_path.is_file():
        print(f"Error: Original file does not exist: {original_path}")
        return 1

    if not modified_path.is_file():
        print(f"Error: Modified file does not exist: {modified_path}")
        return 1

    # Create validator and reporter
    validator = create_validator_from_args(args)
    reporter = create_reporter_from_args(args)

    # Validate files
    result = validator.validate_files(original_path, modified_path)

    # Generate report
    # If no output file is specified, print to stdout
    if not args.output and not getattr(args, "report", None):
        report_text = reporter.generate_report(result)
        print(report_text)
    else:
        reporter.generate_report(result)

    # Return exit code based on status
    return 0 if result.status == "SUCCESS" else 1


def cmd_verify_disk(args: argparse.Namespace) -> int:
    """
    Execute the 'verify-disk' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    modified_path = Path(args.modified)

    if not modified_path.is_file():
        print(f"Error: Modified file does not exist: {modified_path}")
        return 1

    # Assume original file is the one on disk with the same name
    original_path = Path(modified_path.name)

    if not original_path.is_file():
        print(f"Error: Original file does not exist on disk: {original_path}")
        return 1

    # Create validator and reporter
    validator = create_validator_from_args(args)
    reporter = create_reporter_from_args(args)

    # Validate files
    result = validator.validate_files(original_path, modified_path)

    # Generate report
    reporter.generate_report(result)

    # Return exit code based on status
    return 0 if result.status == "SUCCESS" else 1


def cmd_verify_git(args: argparse.Namespace) -> int:
    """
    Execute the 'verify-git' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    file_path = Path(args.file)

    if not file_path.is_file():
        print(f"Error: File does not exist: {file_path}")
        return 1

    # Create validator and reporter
    validator = create_validator_from_args(args)
    reporter = create_reporter_from_args(args)

    # Initialize git integration
    try:
        git = GitIntegration(args.repo_path)
    except GitError as e:
        print(f"Error: {str(e)}")
        return 1

    # Validate file against git revision
    try:
        result = git.validate_file_against_revision(file_path, args.revision, validator)
    except GitError as e:
        print(f"Error: {str(e)}")
        return 1

    # Generate report
    reporter.generate_report(result)

    # Return exit code based on status
    return 0 if result.status == "SUCCESS" else 1


def cmd_verify_revision(args: argparse.Namespace) -> int:
    """
    Execute the 'verify-revision' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    file_path = Path(args.file)

    # Create validator and reporter
    validator = create_validator_from_args(args)
    reporter = create_reporter_from_args(args)

    # Initialize git integration
    try:
        git = GitIntegration(args.repo_path)
    except GitError as e:
        print(f"Error: {str(e)}")
        return 1

    # Compare file between revisions
    try:
        result = git.compare_file_between_revisions(
            file_path, args.from_revision, args.to_revision, validator
        )
    except GitError as e:
        print(f"Error: {str(e)}")
        return 1

    # Generate report
    reporter.generate_report(result)

    # Return exit code based on status
    return 0 if result.status == "SUCCESS" else 1


def cmd_scan(args: argparse.Namespace) -> int:
    """
    Execute the 'scan' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"Error: Directory does not exist: {directory}")
        return 1

    # Create validator and reporter
    validator = create_validator_from_args(args)
    reporter = create_reporter_from_args(args)

    # Scan directory
    result = validator.validate_directory(directory, args.include, args.exclude)

    # Generate report
    reporter.generate_report(result)

    # Return exit code based on status
    return 0 if result.status == "SUCCESS" else 1


def cmd_install_hook(args: argparse.Namespace) -> int:
    """
    Execute the 'install-hook' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    repo_path = args.git_repo if args.git_repo else None

    # Initialize git integration
    try:
        git = GitIntegration(repo_path)
    except GitError as e:
        print(f"Error: {str(e)}")
        return 1

    # Install pre-commit hook
    try:
        hook_path = git.install_pre_commit_hook()
        print(f"Pre-commit hook installed: {hook_path}")
        return 0
    except Exception as e:
        print(f"Error installing pre-commit hook: {str(e)}")
        return 1


def cmd_acl(args: argparse.Namespace) -> int:
    """
    Execute the 'acl' command to get effective permissions for a file or directory.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    from .core.acl import get_effective_permissions

    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        return 1

    try:
        # Get effective permissions
        result = get_effective_permissions(
            path=path,
            repo_path=args.repo_path,
            verbose=args.verbose,
            recursive=args.recursive,
            format=args.format,
            identifier=getattr(args, "identifier", None),
            include_context=getattr(args, "include_context", False),
        )

        # Output the result
        print(result)

        return 0
    except Exception as e:
        print(f"Error getting effective permissions: {str(e)}")
        return 1


def cmd_batch_acl(args: argparse.Namespace) -> int:
    """
    Execute the 'batch-acl' command to get permissions for multiple paths.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    from .core.acl import batch_get_permissions

    # Convert paths to Path objects and validate
    paths = [Path(p) for p in args.paths]
    invalid_paths = [p for p in paths if not p.exists()]

    if invalid_paths:
        print(f"Error: The following paths do not exist:")
        for p in invalid_paths:
            print(f"  - {p}")
        return 1

    try:
        # Get batch permissions
        result = batch_get_permissions(
            paths=paths, repo_path=args.repo_path, verbose=args.verbose, format=args.format
        )

        # Output the result
        print(result)

        return 0
    except Exception as e:
        print(f"Error getting batch permissions: {str(e)}")
        return 1


def cmd_context(args: argparse.Namespace) -> int:
    """
    Execute the 'context' command to get context files for a directory.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    from .core.acl import get_context_files

    directory = Path(args.directory)

    if not directory.exists():
        print(f"Error: Directory does not exist: {directory}")
        return 1

    try:
        # Get context files
        result = get_context_files(
            directory=directory,
            repo_path=args.repo_path,
            recursive=args.recursive,
            priority=args.priority,
            for_use=args.for_use,
            format=args.format,
        )

        # Output the result
        print(result)

        return 0
    except Exception as e:
        print(f"Error getting context files: {str(e)}")
        return 1


def cmd_list_context(args: argparse.Namespace) -> int:
    """
    Execute the 'list-context' command to list all context files in the project.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    from .core.acl import get_context_files

    directory = Path(args.directory)

    if not directory.exists():
        print(f"Error: Directory does not exist: {directory}")
        return 1

    try:
        # Get context files
        result = get_context_files(
            directory=directory,
            repo_path=args.repo_path,
            recursive=args.recursive,
            priority=args.priority,
            for_use=None,  # No filter for list-context
            format=args.format,
        )

        # Output the result
        print(result)

        return 0
    except Exception as e:
        print(f"Error listing context files: {str(e)}")
        return 1


def cmd_create_aiattributes(args: argparse.Namespace) -> int:
    """
    Execute the 'aiattributes create' command to create or update an .ai-attributes file.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    from .core.directory_guard import DirectoryGuard

    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"Error: Directory does not exist: {directory}")
        return 1

    # Path to the .ai-attributes file
    attrs_file = directory / DirectoryGuard.ATTRIBUTES_FILENAME

    # Parse existing file if it exists
    rules = []
    if attrs_file.exists():
        try:
            with open(attrs_file, "r") as f:
                existing_content = f.read()

            # If there's existing content, keep it as a base
            rules.append(existing_content.rstrip())
        except Exception as e:
            print(f"Error reading existing .ai-attributes file: {str(e)}")
            return 1
    else:
        # Add a header if creating a new file
        rules.append("# CodeGuard Directory-Level Guard Annotations")
        rules.append("#")
        rules.append("# Format: <pattern> @GUARD:<WHO>-<PERMISSION> [description]")
        rules.append("#")
        rules.append("# Examples:")
        rules.append("# * @GUARD:AI-RO All files in this directory are AI read-only")
        rules.append("# *.py @GUARD:ALL-FX All Python files are fixed for everyone")
        rules.append("# data/*.json @GUARD:HU-ED JSON files in data dir are human editable")
        rules.append("")

    # Add new rules
    if args.rule:
        for rule_str in args.rule:
            try:
                # Validate the rule format (pattern:guard)
                pattern, guard = rule_str.split(":", 1)
                pattern = pattern.strip()
                guard = guard.strip()

                # Validate guard directive format
                if not guard.startswith(("AI-", "HU-", "ALL-")):
                    raise ValueError(
                        f"Invalid guard format: {guard}. Must start with AI-, HU-, or ALL-"
                    )

                if not guard.split("-")[1] in ("RO", "ED", "FX"):
                    raise ValueError(f"Invalid permission in guard: {guard}. Must be RO, ED, or FX")

                # Add the rule
                desc = ""
                if args.description:
                    # Find a matching description for this pattern
                    for desc_str in args.description:
                        if desc_str.startswith(f"{pattern}:"):
                            desc = desc_str.split(":", 1)[1].strip()
                            break

                rule_line = f"{pattern} @GUARD:{guard}"
                if desc:
                    rule_line += f" {desc}"

                rules.append(rule_line)

            except ValueError as e:
                print(f"Error parsing rule '{rule_str}': {str(e)}")
                return 1

    # Write the file
    try:
        with open(attrs_file, "w") as f:
            f.write("\n".join(rules) + "\n")

        print(f"Created/updated .ai-attributes file at: {attrs_file}")
        return 0
    except Exception as e:
        print(f"Error writing .ai-attributes file: {str(e)}")
        return 1


def cmd_list_aiattributes(args: argparse.Namespace) -> int:
    """
    Execute the 'aiattributes list' command to list rules from .ai-attributes files.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    import json

    import yaml

    from .core.directory_guard import DirectoryGuard

    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"Error: Directory does not exist: {directory}")
        return 1

    # Find .ai-attributes files
    ai_attributes_files = []
    if args.recursive:
        # Find all .ai-attributes files recursively
        for root, _, files in os.walk(directory):
            root_path = Path(root)
            if DirectoryGuard.ATTRIBUTES_FILENAME in files:
                ai_attributes_files.append(root_path / DirectoryGuard.ATTRIBUTES_FILENAME)
    else:
        # Just check the specified directory
        attrs_file = directory / DirectoryGuard.ATTRIBUTES_FILENAME
        if attrs_file.exists():
            ai_attributes_files.append(attrs_file)

    if not ai_attributes_files:
        print(f"No .ai-attributes files found in {directory}")
        return 0

    # Parse each file and collect rules
    results = []

    for attrs_file in ai_attributes_files:
        try:
            # Create a temporary DirectoryGuard to parse the file
            dg = DirectoryGuard()
            rules = dg.parse_attributes_file(attrs_file)

            file_result = {"file": str(attrs_file), "rules": []}

            # Convert rules to a serializable format
            for rule in rules:
                rule_data = {
                    "pattern": rule.pattern,
                    "who": rule.who.name,
                    "permission": rule.permission.name,
                    "description": rule.description,
                    "source_line": rule.source_line,
                }
                file_result["rules"].append(rule_data)

            results.append(file_result)

        except Exception as e:
            print(f"Error parsing {attrs_file}: {str(e)}")
            continue

    # Format and output results
    if args.format == "json":
        print(json.dumps(results, indent=2))
    elif args.format == "yaml":
        try:
            print(yaml.dump(results, sort_keys=False))
        except Exception:
            # Fallback to JSON if YAML is not available
            print(json.dumps(results, indent=2))
    else:
        # Text format
        for file_result in results:
            print(f"File: {file_result['file']}")
            print("-" * 60)

            if not file_result["rules"]:
                print("No rules found.")
                print()
                continue

            for rule in file_result["rules"]:
                print(f"Pattern: {rule['pattern']}")
                print(f"Guard: {rule['who']}-{rule['permission']}")
                if rule["description"]:
                    print(f"Description: {rule['description']}")
                print(f"Line: {rule['source_line']}")
                print()

    return 0


def cmd_validate_aiattributes(args: argparse.Namespace) -> int:
    """
    Execute the 'aiattributes validate' command to validate .ai-attributes files.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    from .core.directory_guard import DirectoryGuard
    from .parsers.guard_parser import GuardPermission, GuardWho

    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"Error: Directory does not exist: {directory}")
        return 1

    # Find .ai-attributes files
    ai_attributes_files = []
    if args.recursive:
        # Find all .ai-attributes files recursively
        for root, _, files in os.walk(directory):
            root_path = Path(root)
            if DirectoryGuard.ATTRIBUTES_FILENAME in files:
                ai_attributes_files.append(root_path / DirectoryGuard.ATTRIBUTES_FILENAME)
    else:
        # Just check the specified directory
        attrs_file = directory / DirectoryGuard.ATTRIBUTES_FILENAME
        if attrs_file.exists():
            ai_attributes_files.append(attrs_file)

    if not ai_attributes_files:
        print(f"No .ai-attributes files found in {directory}")
        return 0

    # Validate each file
    has_errors = False

    for attrs_file in ai_attributes_files:
        print(f"Validating {attrs_file}...")

        try:
            # Read the file
            with open(attrs_file, "r") as f:
                lines = f.readlines()

            # Track errors for this file
            file_errors = []
            modified_lines = lines.copy()

            # Process each line
            for i, line in enumerate(lines):
                line = line.strip()
                line_num = i + 1

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Try to parse the line
                try:
                    # Check if the line has required components
                    parts = line.split()
                    if len(parts) < 2:
                        file_errors.append(
                            (
                                line_num,
                                f"Line {line_num}: Invalid format. Expected '<pattern> @GUARD:<WHO>-<PERMISSION>'",
                            )
                        )
                        continue

                    pattern = parts[0]

                    # Find guard directive
                    guard_parts = None
                    for part in parts[1:]:
                        if part.startswith("@GUARD:"):
                            guard_parts = part.split("@GUARD:")[1].split("-")
                            break

                    if not guard_parts:
                        file_errors.append((line_num, f"Line {line_num}: Missing @GUARD directive"))
                        continue

                    if len(guard_parts) != 2:
                        file_errors.append(
                            (
                                line_num,
                                f"Line {line_num}: Invalid @GUARD format. Expected '<WHO>-<PERMISSION>'",
                            )
                        )
                        continue

                    # Validate WHO part
                    who = guard_parts[0]
                    try:
                        GuardWho[who]
                    except KeyError:
                        file_errors.append(
                            (
                                line_num,
                                f"Line {line_num}: Invalid WHO value '{who}'. Must be AI, HU, or ALL",
                            )
                        )

                        if args.fix:
                            # Try to fix WHO part
                            if who.upper() in ("AI", "HU", "ALL"):
                                fixed_who = who.upper()
                                modified_lines[i] = line.replace(
                                    f"@GUARD:{who}", f"@GUARD:{fixed_who}"
                                )
                                file_errors[-1] = (
                                    line_num,
                                    f"Line {line_num}: Fixed WHO value from '{who}' to '{fixed_who}'",
                                )

                        continue

                    # Validate PERMISSION part
                    permission = guard_parts[1]
                    try:
                        GuardPermission[permission]
                    except KeyError:
                        file_errors.append(
                            (
                                line_num,
                                f"Line {line_num}: Invalid PERMISSION value '{permission}'. Must be RO, ED, or FX",
                            )
                        )

                        if args.fix:
                            # Try to fix PERMISSION part
                            if permission.upper() in ("RO", "ED", "FX"):
                                fixed_permission = permission.upper()
                                modified_lines[i] = line.replace(
                                    f"-{permission}", f"-{fixed_permission}"
                                )
                                file_errors[-1] = (
                                    line_num,
                                    f"Line {line_num}: Fixed PERMISSION value from '{permission}' to '{fixed_permission}'",
                                )

                        continue

                except Exception as e:
                    file_errors.append((line_num, f"Line {line_num}: Parsing error: {str(e)}"))

            # Report and fix errors if needed
            if file_errors:
                has_errors = True
                print(f"Found {len(file_errors)} errors in {attrs_file}:")
                for line_num, error in file_errors:
                    print(f"  {error}")

                if args.fix and any(modified_lines[i] != lines[i] for i in range(len(lines))):
                    # Write the fixed file
                    with open(attrs_file, "w") as f:
                        f.writelines(modified_lines)
                    print(f"Fixed {attrs_file}")
            else:
                print(f"No errors found in {attrs_file}")

            print()

        except Exception as e:
            print(f"Error validating {attrs_file}: {str(e)}")
            has_errors = True

    return 1 if has_errors else 0


def cmd_list_guarded_directories(args: argparse.Namespace) -> int:
    """
    Execute the 'list-guarded-directories' command to list directories with guard annotations.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    import json

    import yaml

    from .core.directory_guard import DirectoryGuard

    directory = Path(args.directory)

    if not directory.is_dir():
        print(f"Error: Directory does not exist: {directory}")
        return 1

    # Find all .ai-attributes files recursively
    guarded_dirs = []

    for root, _, files in os.walk(directory):
        root_path = Path(root)
        if DirectoryGuard.ATTRIBUTES_FILENAME in files:
            try:
                # Create a temporary DirectoryGuard to parse the file
                dg = DirectoryGuard()
                rules = dg.parse_attributes_file(root_path / DirectoryGuard.ATTRIBUTES_FILENAME)

                dir_info = {
                    "path": str(root_path),
                    "rules_count": len(rules),
                    "patterns": [rule.pattern for rule in rules],
                }

                guarded_dirs.append(dir_info)
            except Exception as e:
                print(f"Error parsing {root_path / DirectoryGuard.ATTRIBUTES_FILENAME}: {str(e)}")
                continue

    # Format and output results
    if args.format == "json":
        print(json.dumps(guarded_dirs, indent=2))
    elif args.format == "yaml":
        try:
            print(yaml.dump(guarded_dirs, sort_keys=False))
        except Exception:
            # Fallback to JSON if YAML is not available
            print(json.dumps(guarded_dirs, indent=2))
    else:
        # Text format
        print(f"Found {len(guarded_dirs)} guarded directories:")
        print()

        for dir_info in guarded_dirs:
            print(f"Directory: {dir_info['path']}")
            print(f"Rules: {dir_info['rules_count']}")
            print("Patterns:")
            for pattern in dir_info["patterns"]:
                print(f"  - {pattern}")
            print()

    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    """
    Execute the 'serve' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    try:
        # Import MCP server components
        from .mcp.server import MCPServer
    except ImportError:
        print("Error: FastAPI and FastAPI-MCP are required for the MCP server.")
        print("Install with: pip install fastapi fastapi-mcp uvicorn")
        return 1

    # Start MCP server
    try:
        server = MCPServer(args.host, args.port)
        print(f"Starting MCP server on {args.host}:{args.port}")
        server.run()
        return 0
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}")
        return 1


def cmd_validate_sections(args: argparse.Namespace) -> int:
    """
    Execute the 'validate-sections' command.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    from .core.section_validator import validate_sections

    try:
        # Call the validation function
        exit_code = validate_sections(
            json_file_path=args.json_file, source_file_path=args.file, verbose=args.verbose > 0
        )
        return exit_code
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 7  # EXIT_INTERNAL_ERROR


if __name__ == "__main__":
    sys.exit(main())
