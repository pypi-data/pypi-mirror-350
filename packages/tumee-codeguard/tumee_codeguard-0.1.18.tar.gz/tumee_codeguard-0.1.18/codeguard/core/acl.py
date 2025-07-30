"""
Access Control List (ACL) functionality for CodeGuard.

This module provides utilities for retrieving and formatting access control
information about files and directories based on the directory-level guard system.
"""

import json
import pathlib
from typing import Dict, List, Optional, Union

import yaml

from .validator import CodeGuardValidator


def get_effective_permissions(
    path: Union[str, pathlib.Path],
    repo_path: Optional[Union[str, pathlib.Path]] = None,
    verbose: bool = False,
    recursive: bool = False,
    format: str = "json",
    identifier: Optional[str] = None,
    include_context: bool = False,
) -> str:
    """
    Get effective permissions for a path.

    Args:
        path: Path to get permissions for
        repo_path: Repository root path
        verbose: Whether to include detailed source information
        recursive: Whether to recursively check children (for directories)
        format: Output format (json, yaml, text)
        identifier: Specific identifier (e.g., "claude-4", "security-team")
        include_context: Whether to include context file information

    Returns:
        Formatted permissions information
    """
    # Create validator with directory guard support
    validator = CodeGuardValidator(repo_path=repo_path, use_directory_guards=True)

    # Get permissions
    permissions = validator.get_effective_permissions(
        path=path, verbose=verbose, recursive=recursive
    )

    # Filter by identifier if provided
    if identifier and "permissions" in permissions:
        # Filter permissions by identifier
        if "ai" in permissions["permissions"] and isinstance(
            permissions["permissions"]["ai"], dict
        ):
            # If AI permissions are detailed (with identifiers), filter them
            ai_perms = permissions["permissions"]["ai"]
            if identifier in ai_perms:
                permissions["permissions"]["ai"] = {identifier: ai_perms[identifier]}
            else:
                # Identifier not found, return none
                permissions["permissions"]["ai"] = {identifier: "none"}

    # Add context file information if requested
    if include_context and hasattr(validator, "directory_guard"):
        from .directory_guard import DirectoryGuard

        dir_guard = validator.directory_guard
        if dir_guard:
            is_context, metadata = dir_guard.is_context_file(path)
            permissions["is_context"] = is_context
            if is_context and metadata:
                permissions["context_metadata"] = metadata

    # Format output
    if format.lower() == "json":
        return json.dumps(permissions, indent=2)
    elif format.lower() == "yaml":
        try:
            return yaml.dump(permissions, sort_keys=False)
        except Exception:
            # Fallback to JSON if YAML is not available
            return json.dumps(permissions, indent=2)
    else:
        # Text format
        return _format_permissions_as_text(permissions, verbose, recursive)


def _format_permissions_as_text(permissions: Dict, verbose: bool, recursive: bool) -> str:
    """
    Format permissions information as text.

    Args:
        permissions: Permissions dictionary
        verbose: Whether detailed information is included
        recursive: Whether recursive information is included

    Returns:
        Text representation of permissions
    """
    lines = []

    # Check for error
    if permissions.get("status") == "error":
        lines.append(f"Error: {permissions.get('error')}")
        return "\n".join(lines)

    # Basic information
    lines.append(f"Path: {permissions['path']}")
    lines.append(f"Type: {permissions['type']}")
    lines.append(f"Code: {permissions['code']}")
    lines.append("")

    # Permissions
    lines.append("Permissions:")
    lines.append(f"  AI: {permissions['permissions']['ai']}")
    if "human" in permissions["permissions"]:
        lines.append(f"  Human: {permissions['permissions']['human']}")
    lines.append("")

    # Permission sources if verbose
    if verbose and "permission_sources" in permissions:
        lines.append("Permission Sources:")
        for source in permissions["permission_sources"]:
            lines.append(f"  Level: {source['level']}")
            lines.append(f"  File: {source['file']}")
            lines.append(f"  Pattern: {source['pattern']}")
            lines.append(f"  Permission: {source['permission']}")
            lines.append("")

    # File-level guards if verbose
    if verbose and "file_level_guards" in permissions and permissions["file_level_guards"]:
        lines.append("File-Level Guards:")
        for guard in permissions["file_level_guards"]:
            lines.append(f"  Line {guard['line']}: {guard['annotation']}")
            if "description" in guard and guard["description"]:
                lines.append(f"    Description: {guard['description']}")
        lines.append("")

    # Directory information if recursive
    if recursive and permissions["type"] == "directory" and "children" in permissions:
        lines.append("Directory Summary:")
        lines.append(f"  Total Children: {permissions['children']['total']}")
        lines.append(f"  Permissions Consistent: {permissions['children']['consistent']}")

        if not permissions["children"]["consistent"]:
            lines.append("  Inconsistent Paths:")
            for path in permissions["children"]["inconsistent_paths"]:
                lines.append(f"    - {path}")

        lines.append("")

        # Child permissions if verbose and recursive
        if verbose and "child_permissions" in permissions:
            lines.append("Child Permissions:")
            for child in permissions["child_permissions"]:
                lines.append(f"  {child['path']}: {child['code']}")
            lines.append("")

    return "\n".join(lines)


def batch_get_permissions(
    paths: List[Union[str, pathlib.Path]],
    repo_path: Optional[Union[str, pathlib.Path]] = None,
    verbose: bool = False,
    format: str = "json",
) -> str:
    """
    Get permissions for multiple paths in a batch.

    Args:
        paths: List of paths to get permissions for
        repo_path: Repository root path
        verbose: Whether to include detailed source information
        format: Output format (json, yaml, text)

    Returns:
        Formatted permissions information
    """
    # Create validator with directory guard support
    validator = CodeGuardValidator(repo_path=repo_path, use_directory_guards=True)

    # Get permissions for each path
    results = []
    for path in paths:
        permissions = validator.get_effective_permissions(
            path=path, verbose=verbose, recursive=False  # Don't recurse in batch mode
        )
        results.append(permissions)

    # Create response
    response = {"batch_results": results, "total": len(results), "status": "success"}

    # Format output
    if format.lower() == "json":
        return json.dumps(response, indent=2)
    elif format.lower() == "yaml":
        try:
            return yaml.dump(response, sort_keys=False)
        except Exception:
            # Fallback to JSON if YAML is not available
            return json.dumps(response, indent=2)
    else:
        # Text format
        lines = []
        lines.append(f"Batch Results ({len(results)} paths):")
        lines.append("")

        for i, result in enumerate(results, 1):
            lines.append(f"Path {i}: {result['path']}")
            lines.append(f"Type: {result['type']}")
            lines.append(f"Code: {result.get('code', 'N/A')}")

            if "permissions" in result:
                lines.append(f"AI Permission: {result['permissions'].get('ai', 'N/A')}")
                lines.append(f"Human Permission: {result['permissions'].get('human', 'N/A')}")

            if result.get("status") == "error":
                lines.append(f"Error: {result.get('error', 'Unknown error')}")

            lines.append("")

        return "\n".join(lines)


def get_context_files(
    directory: Union[str, pathlib.Path],
    repo_path: Optional[Union[str, pathlib.Path]] = None,
    recursive: bool = True,
    priority: Optional[str] = None,
    for_use: Optional[str] = None,
    format: str = "json",
) -> str:
    """
    Get all context files in a directory.

    Args:
        directory: Directory to search
        repo_path: Repository root path
        recursive: Whether to search subdirectories
        priority: Filter by priority level (high, medium, low)
        for_use: Filter by usage scope (testing, configuration, etc.)
        format: Output format (json, yaml, text)

    Returns:
        Formatted context file information
    """
    from .directory_guard import DirectoryGuard

    # Create directory guard
    dir_guard = DirectoryGuard(repo_path)

    # Get all context files
    context_files = dir_guard.get_context_files(directory, recursive)

    # Filter by priority if specified
    if priority:
        context_files = [
            cf for cf in context_files if cf.get("metadata", {}).get("priority") == priority
        ]

    # Filter by usage scope if specified
    if for_use:
        context_files = [
            cf
            for cf in context_files
            if for_use in cf.get("metadata", {}).get("for", "").split(",")
        ]

    # Create response
    response = {
        "directory": str(directory),
        "context_files": context_files,
        "total": len(context_files),
        "filters": {"priority": priority, "for": for_use},
        "status": "success",
    }

    # Format output
    if format.lower() == "json":
        return json.dumps(response, indent=2)
    elif format.lower() == "yaml":
        try:
            return yaml.dump(response, sort_keys=False)
        except Exception:
            return json.dumps(response, indent=2)
    else:
        # Text format
        lines = []
        lines.append(f"Context Files in {directory}:")
        lines.append(f"Total: {len(context_files)}")
        if priority or for_use:
            lines.append("Filters:")
            if priority:
                lines.append(f"  Priority: {priority}")
            if for_use:
                lines.append(f"  For: {for_use}")
        lines.append("")

        for cf in context_files:
            lines.append(f"- {cf['path']}")
            metadata = cf.get("metadata", {})
            if metadata:
                if "priority" in metadata:
                    lines.append(f"  Priority: {metadata['priority']}")
                if "for" in metadata:
                    lines.append(f"  For: {metadata['for']}")
                if "inherit" in metadata:
                    lines.append(f"  Inherit: {metadata['inherit']}")
            lines.append("")

        return "\n".join(lines)
