#!/usr/bin/env python3
"""
Section validation module for comparing external tool parsing with internal parsing.

This module implements the validation mode that allows external tools (like VS Code plugins)
to verify their guard section parsing matches exactly with CodeGuard's internal parsing.

Important: Guards create overlapping protection layers, not sequential non-overlapping sections.
A single line of code can be covered by multiple guard annotations with different targets,
permissions, and scopes.
"""

import hashlib
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..version import __version__

# Exit codes
EXIT_SUCCESS = 0  # Perfect match
EXIT_VALIDATION_MISMATCH = 1  # Validation differences found
EXIT_PARSING_ERROR = 2  # Error parsing source file
EXIT_JSON_ERROR = 3  # Invalid JSON format or structure
EXIT_FILE_NOT_FOUND = 4  # Source file not found
EXIT_FILE_CHANGED = 5  # File content changed since plugin parse
EXIT_VERSION_INCOMPATIBLE = 6  # Plugin/tool version mismatch
EXIT_INTERNAL_ERROR = 7  # Unexpected internal error

# Status values in JSON response
STATUS_MATCH = "MATCH"  # Perfect match
STATUS_MISMATCH = "MISMATCH"  # Validation differences
STATUS_ERROR_PARSING = "ERROR_PARSING"  # Could not parse file
STATUS_ERROR_JSON = "ERROR_JSON"  # Invalid request format
STATUS_ERROR_FILE_NOT_FOUND = "ERROR_FILE_NOT_FOUND"
STATUS_ERROR_FILE_CHANGED = "ERROR_FILE_CHANGED"
STATUS_ERROR_VERSION = "ERROR_VERSION"
STATUS_ERROR_INTERNAL = "ERROR_INTERNAL"

# Discrepancy types
DISCREPANCY_TYPES = {
    "boundary_mismatch": "Guard region start/end lines don't match",
    "guard_missing": "Plugin found guard, tool did not",
    "guard_extra": "Tool found guard, plugin did not",
    "guard_interpretation": "Same guard parsed differently",
    "permission_mismatch": "Different permission interpretation",
    "scope_mismatch": "Different scope interpretation",
    "target_mismatch": "Different target (ai/human) interpretation",
    "identifier_mismatch": "Different identifier parsing",
    "layer_mismatch": "Different overlapping guard layers at line",
    "effective_permission_mismatch": "Different effective permissions after layer resolution",
    "scope_boundary_mismatch": "Guard scope ends at different line",
    "inheritance_mismatch": "Different guard inheritance interpretation",
    "override_mismatch": "Different interpretation of guard overrides",
    "content_hash_mismatch": "Guard region content changed",
    "line_count_mismatch": "File has different number of lines",
}


@dataclass
class ParsedGuard:
    """Represents a parsed guard annotation."""

    raw: str
    target: str
    identifiers: List[str]
    permission: str
    scope: Optional[str]
    scope_modifiers: List[str]


@dataclass
class GuardRegion:
    """Represents a guard region with overlapping support."""

    index: int
    guard: str
    parsed_guard: ParsedGuard
    declaration_line: int
    start_line: int
    end_line: int
    content_hash: Optional[str] = None
    content_preview: Optional[str] = None


@dataclass
class LineCoverage:
    """Represents which guards apply to a specific line."""

    line: int
    guards: List[int]  # Indices of guards that apply to this line


@dataclass
class Discrepancy:
    """Represents a validation discrepancy."""

    type: str
    severity: str  # "ERROR" or "WARNING"
    message: str
    line: Optional[int] = None
    guard_index: Optional[int] = None
    plugin_region: Optional[Dict[str, Any]] = None
    tool_region: Optional[Dict[str, Any]] = None
    plugin_guards: Optional[List[Dict[str, Any]]] = None
    tool_guards: Optional[List[Dict[str, Any]]] = None
    plugin_effective: Optional[str] = None
    tool_effective: Optional[str] = None
    target: Optional[str] = None


def compute_file_hash(file_path: str) -> str:
    """Compute SHA-256 hash of file contents."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_content_hash(lines: List[str]) -> str:
    """Compute SHA-256 hash of content lines."""
    content = "\n".join(lines)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def create_error_response(
    exit_code: int, status: str, error: str, details: Optional[Dict[str, Any]] = None
) -> int:
    """Create and output an error response."""
    response = {"validation_result": {"status": status, "exit_code": exit_code, "error": error}}

    if details:
        response["validation_result"]["details"] = details

    sys.stdout.write(json.dumps(response, indent=2))
    sys.stdout.flush()
    return exit_code


def create_success_response(request: Dict[str, Any], internal_regions: List[GuardRegion]) -> int:
    """Create and output a success response."""
    # Calculate statistics
    total_lines = request["validation_request"]["total_lines"]
    line_coverage = build_line_coverage(internal_regions, total_lines)

    # Count lines with multiple guards
    lines_with_multiple = sum(1 for guards in line_coverage.values() if len(guards) > 1)
    max_overlapping = max(len(guards) for guards in line_coverage.values()) if line_coverage else 0

    response = {
        "validation_result": {
            "status": STATUS_MATCH,
            "exit_code": EXIT_SUCCESS,
            "file_path": request["validation_request"]["file_path"],
            "timestamp": datetime.now().isoformat() + "Z",
            "tool_version": __version__,
            "plugin_version": request["validation_request"]["plugin_version"],
            "discrepancies": [],
            "statistics": {
                "total_lines": total_lines,
                "plugin_guard_regions": len(request["validation_request"]["guard_regions"]),
                "tool_guard_regions": len(internal_regions),
                "matching_regions": len(request["validation_request"]["guard_regions"]),
                "max_overlapping_guards": max_overlapping,
                "lines_with_multiple_guards": lines_with_multiple,
            },
        }
    }

    sys.stdout.write(json.dumps(response, indent=2))
    sys.stdout.flush()
    return EXIT_SUCCESS


def create_mismatch_response(
    request: Dict[str, Any], internal_regions: List[GuardRegion], discrepancies: List[Discrepancy]
) -> int:
    """Create and output a mismatch response."""
    # Calculate statistics
    total_lines = request["validation_request"]["total_lines"]
    matching_regions = len(request["validation_request"]["guard_regions"]) - len(
        [d for d in discrepancies if d.type in ["guard_missing", "guard_extra"]]
    )

    # Count affected lines
    affected_lines = set()
    for d in discrepancies:
        if d.line:
            affected_lines.add(d.line)

    response = {
        "validation_result": {
            "status": STATUS_MISMATCH,
            "exit_code": EXIT_VALIDATION_MISMATCH,
            "file_path": request["validation_request"]["file_path"],
            "timestamp": datetime.now().isoformat() + "Z",
            "tool_version": __version__,
            "plugin_version": request["validation_request"]["plugin_version"],
            "discrepancies": [asdict(d) for d in discrepancies],
            "statistics": {
                "total_lines": total_lines,
                "plugin_guard_regions": len(request["validation_request"]["guard_regions"]),
                "tool_guard_regions": len(internal_regions),
                "matching_regions": matching_regions,
                "discrepancy_count": len(discrepancies),
                "affected_lines": len(affected_lines),
            },
        }
    }

    sys.stdout.write(json.dumps(response, indent=2))
    sys.stdout.flush()
    return EXIT_VALIDATION_MISMATCH


def validate_request_structure(request: Dict[str, Any]) -> Optional[str]:
    """Validate the structure of the validation request."""
    # Check for required top-level fields
    if "validation_request" not in request:
        return "Missing required field: validation_request"

    vr = request["validation_request"]

    # Check required fields in validation_request
    required_fields = [
        "file_path",
        "file_hash",
        "total_lines",
        "timestamp",
        "plugin_version",
        "plugin_name",
        "guard_regions",
    ]

    for field in required_fields:
        if field not in vr:
            return f"Missing required field: validation_request.{field}"

    # Validate guard_regions
    if not isinstance(vr["guard_regions"], list):
        return "validation_request.guard_regions must be a list"

    for i, region in enumerate(vr["guard_regions"]):
        # Check required region fields
        required_region_fields = [
            "index",
            "guard",
            "parsed_guard",
            "declaration_line",
            "start_line",
            "end_line",
        ]
        for field in required_region_fields:
            if field not in region:
                return f"Missing required field in guard_region {i}: {field}"

        # Validate parsed_guard structure
        pg = region["parsed_guard"]
        required_guard_fields = ["raw", "target", "identifiers", "permission", "scope"]
        for field in required_guard_fields:
            if field not in pg:
                return f"Missing required field in guard_region {i} parsed_guard: {field}"

    # Validate optional line_coverage if present
    if "line_coverage" in vr:
        if not isinstance(vr["line_coverage"], list):
            return "validation_request.line_coverage must be a list"

        for i, coverage in enumerate(vr["line_coverage"]):
            if "line" not in coverage or "guards" not in coverage:
                return f"Invalid line_coverage entry {i}: must have 'line' and 'guards'"

    return None


def parse_file_guards(file_path: str) -> List[GuardRegion]:
    """Parse a file and extract guard regions using CodeGuard's internal parser."""
    from ..parsers.guard_parser import GuardParser
    from ..parsers.language_parser import LanguageParser

    # Read file content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines(keepends=True)

    # Create parsers
    lang_parser = LanguageParser()
    guard_parser = GuardParser()

    # Parse the file
    try:
        language, comments, regions = lang_parser.parse_file(file_path)
    except Exception as e:
        raise Exception(f"Failed to parse file: {str(e)}")

    # Extract guarded regions
    guarded_regions = guard_parser.extract_guarded_regions(content, language, comments, regions)

    # Convert to GuardRegion objects
    guard_regions = []

    for i, guard_region in enumerate(guarded_regions):
        # Each guarded region may have multiple directives, but we'll use the first one
        # as the primary guard for this region
        directive = guard_region.directives[0] if guard_region.directives else None

        if directive:
            # Convert GuardWho enum value to string
            who_str = directive.who.value if hasattr(directive.who, "value") else str(directive.who)
            target = "ai" if who_str == "ai" else "human" if who_str == "human" else "all"

            # Convert GuardPermission enum value to string
            perm_str = (
                directive.permission.value
                if hasattr(directive.permission, "value")
                else str(directive.permission)
            )
            permission = "read-only" if perm_str == "r" else "write" if perm_str == "w" else "none"

            # Handle identifiers - can be a single identifier or list
            identifiers = (
                directive.identifiers
                if directive.identifiers
                else ([directive.identifier] if directive.identifier else ["*"])
            )

            parsed_guard = ParsedGuard(
                raw=directive.tag,
                target=target,
                identifiers=identifiers,
                permission=permission,
                scope=directive.scope.value if directive.scope else "file",
                scope_modifiers=[],
            )

            # Calculate content hash for the region
            region_lines = [
                lines[j - 1]
                for j in range(guard_region.start_line, guard_region.end_line + 1)
                if j - 1 < len(lines)
            ]
            content_hash = compute_content_hash(region_lines)

            # Get content preview (first line of the guarded code)
            preview_line = guard_region.start_line
            content_preview = (
                lines[preview_line - 1].strip() if preview_line - 1 < len(lines) else ""
            )

            guard_regions.append(
                GuardRegion(
                    index=i,
                    guard=directive.tag,
                    parsed_guard=parsed_guard,
                    declaration_line=directive.line_number,
                    start_line=guard_region.start_line,
                    end_line=guard_region.end_line,
                    content_hash=content_hash,
                    content_preview=content_preview,
                )
            )

    return guard_regions


def build_line_coverage(guard_regions: List[GuardRegion], total_lines: int) -> Dict[int, List[int]]:
    """Build a mapping of line numbers to guard indices that apply to that line."""
    line_coverage = {}

    for region in guard_regions:
        for line in range(region.start_line, min(region.end_line + 1, total_lines + 1)):
            if line not in line_coverage:
                line_coverage[line] = []
            line_coverage[line].append(region.index)

    return line_coverage


def compare_guard_regions(
    plugin_regions: List[Dict[str, Any]],
    tool_regions: List[GuardRegion],
    total_lines: int,
    plugin_line_coverage: List[Dict[str, Any]] = None,
) -> List[Discrepancy]:
    """Compare plugin guard regions with tool guard regions and identify discrepancies."""
    discrepancies = []

    # Build line coverage for tool regions
    tool_line_coverage = build_line_coverage(tool_regions, total_lines)

    # Create lookup maps for easier comparison
    plugin_by_index = {r["index"]: r for r in plugin_regions}
    tool_by_index = {r.index: r for r in tool_regions}

    # Compare individual guard regions
    for plugin_region in plugin_regions:
        idx = plugin_region["index"]

        # Find matching tool region by guard and approximate location
        matching_tool_region = None
        for tool_region in tool_regions:
            if (
                tool_region.guard == plugin_region["guard"]
                and abs(tool_region.declaration_line - plugin_region["declaration_line"]) <= 2
            ):
                matching_tool_region = tool_region
                break

        if not matching_tool_region:
            discrepancies.append(
                Discrepancy(
                    type="guard_missing",
                    severity="ERROR",
                    guard_index=idx,
                    message=f"Plugin guard region {idx} not found in tool parsing",
                    plugin_region=plugin_region,
                )
            )
            continue

        # Check boundaries
        if (
            plugin_region["start_line"] != matching_tool_region.start_line
            or plugin_region["end_line"] != matching_tool_region.end_line
        ):
            discrepancies.append(
                Discrepancy(
                    type="boundary_mismatch",
                    severity="ERROR",
                    guard_index=idx,
                    plugin_region={
                        "guard": plugin_region["guard"],
                        "start_line": plugin_region["start_line"],
                        "end_line": plugin_region["end_line"],
                    },
                    tool_region={
                        "guard": matching_tool_region.guard,
                        "start_line": matching_tool_region.start_line,
                        "end_line": matching_tool_region.end_line,
                    },
                    message=f"Guard region boundary differs: plugin [{plugin_region['start_line']}-{plugin_region['end_line']}] vs tool [{matching_tool_region.start_line}-{matching_tool_region.end_line}]",
                )
            )

        # Compare guard interpretation
        pg = plugin_region.get("parsed_guard", {})
        tg = matching_tool_region.parsed_guard

        if pg and tg:
            # Compare target
            if pg.get("target") != tg.target:
                discrepancies.append(
                    Discrepancy(
                        type="target_mismatch",
                        severity="ERROR",
                        guard_index=idx,
                        message=f"Target mismatch: plugin '{pg.get('target')}' vs tool '{tg.target}'",
                    )
                )

            # Compare permission
            if pg.get("permission") != tg.permission:
                discrepancies.append(
                    Discrepancy(
                        type="permission_mismatch",
                        severity="ERROR",
                        guard_index=idx,
                        message=f"Permission mismatch: plugin '{pg.get('permission')}' vs tool '{tg.permission}'",
                    )
                )

            # Compare identifiers
            plugin_ids = set(pg.get("identifiers", ["*"]))
            tool_ids = set(tg.identifiers)
            if plugin_ids != tool_ids:
                discrepancies.append(
                    Discrepancy(
                        type="identifier_mismatch",
                        severity="WARNING",
                        guard_index=idx,
                        message=f"Identifier mismatch: plugin {plugin_ids} vs tool {tool_ids}",
                    )
                )

            # Compare scope
            if pg.get("scope") != tg.scope:
                discrepancies.append(
                    Discrepancy(
                        type="scope_mismatch",
                        severity="WARNING",
                        guard_index=idx,
                        message=f"Scope mismatch: plugin '{pg.get('scope')}' vs tool '{tg.scope}'",
                    )
                )

    # Check for tool regions not in plugin
    for tool_region in tool_regions:
        found = False
        for plugin_region in plugin_regions:
            if (
                tool_region.guard == plugin_region["guard"]
                and abs(tool_region.declaration_line - plugin_region["declaration_line"]) <= 2
            ):
                found = True
                break

        if not found:
            discrepancies.append(
                Discrepancy(
                    type="guard_extra",
                    severity="ERROR",
                    line=tool_region.declaration_line,
                    message=f"Tool guard region not found in plugin parsing",
                    tool_region=asdict(tool_region),
                )
            )

    # Compare line coverage if provided
    if plugin_line_coverage:
        plugin_coverage_map = {
            entry["line"]: set(entry["guards"]) for entry in plugin_line_coverage
        }

        # Check specific lines mentioned in plugin coverage
        for line_entry in plugin_line_coverage:
            line = line_entry["line"]
            plugin_guards = set(line_entry["guards"])
            tool_guards = set(tool_line_coverage.get(line, []))

            # Only report if there's an actual mismatch (not when both are empty)
            if plugin_guards != tool_guards and (plugin_guards or tool_guards):
                # Get guard details for better error message
                plugin_guard_details = []
                tool_guard_details = []

                for g_idx in plugin_guards:
                    if g_idx in plugin_by_index:
                        plugin_guard_details.append(
                            {"index": g_idx, "guard": plugin_by_index[g_idx]["guard"]}
                        )

                for g_idx in tool_guards:
                    if g_idx in tool_by_index:
                        tool_guard_details.append(
                            {"index": g_idx, "guard": tool_by_index[g_idx].guard}
                        )

                discrepancies.append(
                    Discrepancy(
                        type="layer_mismatch",
                        severity="ERROR",
                        line=line,
                        plugin_guards=plugin_guard_details,
                        tool_guards=tool_guard_details,
                        message=f"Different guards apply to line {line}",
                    )
                )

    return discrepancies


def validate_sections(
    json_file_path: str, source_file_path: Optional[str] = None, verbose: bool = False
) -> int:
    """
    Validate that external tool's guard section parsing matches our internal parsing.

    Args:
        json_file_path: Path to JSON validation request
        source_file_path: Optional override for source file path (defaults to path in JSON)
        verbose: Include detailed parsing information

    Returns:
        Exit code
    """
    try:
        # Load validation request
        with open(json_file_path, "r") as f:
            request = json.load(f)
    except FileNotFoundError:
        return create_error_response(
            EXIT_FILE_NOT_FOUND,
            STATUS_ERROR_FILE_NOT_FOUND,
            f"JSON file not found: {json_file_path}",
        )
    except json.JSONDecodeError as e:
        return create_error_response(
            EXIT_JSON_ERROR,
            STATUS_ERROR_JSON,
            f"Invalid JSON format",
            {"error": str(e), "line": e.lineno, "column": e.colno},
        )

    # Validate request structure
    validation_error = validate_request_structure(request)
    if validation_error:
        return create_error_response(EXIT_JSON_ERROR, STATUS_ERROR_JSON, validation_error)

    # Get file path
    file_path = source_file_path or request["validation_request"]["file_path"]

    # Check file exists
    if not os.path.exists(file_path):
        return create_error_response(
            EXIT_FILE_NOT_FOUND,
            STATUS_ERROR_FILE_NOT_FOUND,
            f"Source file not found: {file_path}",
            {"file_path": file_path},
        )

    # Verify file hasn't changed
    current_hash = compute_file_hash(file_path)
    if current_hash != request["validation_request"]["file_hash"]:
        # Get line count for additional context
        with open(file_path, "r") as f:
            current_lines = len(f.readlines())

        return create_error_response(
            EXIT_FILE_CHANGED,
            STATUS_ERROR_FILE_CHANGED,
            "File content has changed since plugin parsing",
            {
                "plugin_file_hash": request["validation_request"]["file_hash"],
                "current_file_hash": current_hash,
                "plugin_line_count": request["validation_request"]["total_lines"],
                "current_line_count": current_lines,
            },
        )

    # Parse file independently
    try:
        internal_regions = parse_file_guards(file_path)
    except Exception as e:
        return create_error_response(
            EXIT_PARSING_ERROR,
            STATUS_ERROR_PARSING,
            "Failed to parse source file",
            {"parser_error": str(e), "file_path": file_path},
        )

    # Compare guard regions
    discrepancies = compare_guard_regions(
        request["validation_request"]["guard_regions"],
        internal_regions,
        request["validation_request"]["total_lines"],
        request["validation_request"].get("line_coverage", []),
    )

    if not discrepancies:
        return create_success_response(request, internal_regions)
    else:
        return create_mismatch_response(request, internal_regions, discrepancies)
