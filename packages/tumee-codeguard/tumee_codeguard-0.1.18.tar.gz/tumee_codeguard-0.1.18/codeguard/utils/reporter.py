"""
Reporter for CodeGuard.

This module provides functionality for generating reports of validation results
in different formats.
"""

import json
from enum import Enum
from typing import Any, Dict, Optional, TextIO, Union

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Lazy load rich for fancy terminal output
RICH_AVAILABLE = None
_rich_console = None
_rich_table = None
_rich_panel = None
_rich_syntax = None
_rich_text = None


def _check_rich():
    """Check if rich is available and import it lazily."""
    global RICH_AVAILABLE, _rich_console, _rich_table, _rich_panel, _rich_syntax, _rich_text
    if RICH_AVAILABLE is None:
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.syntax import Syntax
            from rich.table import Table
            from rich.text import Text

            _rich_console = Console
            _rich_table = Table
            _rich_panel = Panel
            _rich_syntax = Syntax
            _rich_text = Text
            RICH_AVAILABLE = True
        except ImportError:
            RICH_AVAILABLE = False
    return RICH_AVAILABLE


from ..core.validator import GuardViolation, ValidationResult


class ReportFormat(Enum):
    """
    Supported output formats for validation reports.

    Values:
        JSON: Machine-readable JSON format
        YAML: Human-friendly YAML format
        TEXT: Plain text format for terminals
        HTML: HTML format with syntax highlighting
        MARKDOWN: Markdown format for documentation
        CONSOLE: Rich console output with colors and formatting
    """

    JSON = "json"
    YAML = "yaml"
    TEXT = "text"
    HTML = "html"
    MARKDOWN = "markdown"
    CONSOLE = "console"  # Rich console output


class ConsoleStyle(Enum):
    """
    Console output styling options for the CONSOLE format.

    Values:
        PLAIN: No special formatting, plain text
        MINIMAL: Basic formatting with minimal decorations
        DETAILED: Full details with code snippets and diffs
        COMPACT: Condensed output for many violations
    """

    PLAIN = "plain"
    MINIMAL = "minimal"
    DETAILED = "detailed"
    COMPACT = "compact"


class Reporter:
    """
    Reporter for generating validation result reports.

    This class handles the generation of validation reports in various formats,
    suitable for different use cases (human reading, CI/CD integration,
    documentation, etc.). It supports both file and stream output.

    Attributes:
        format: The report format to generate
        output_file: Output destination (file path or file object)
        style: Console output style (for CONSOLE format)
        console: Rich console instance (if available)
    """

    def __init__(
        self,
        format: Union[str, ReportFormat] = ReportFormat.TEXT,
        output_file: Optional[Union[str, TextIO]] = None,
        console_style: Union[str, ConsoleStyle] = ConsoleStyle.DETAILED,
        include_content: bool = True,
        include_diff: bool = True,
        max_content_lines: int = 10,
    ) -> None:
        """
        Initialize the reporter with specified options.

        Args:
            format: Report format to generate (default: TEXT).
                   Can be a ReportFormat enum value or string.
            output_file: Optional output destination. Can be:
                        - File path as string
                        - File-like object (must have write() method)
                        - None for stdout (default)
            console_style: Style for CONSOLE format output (default: DETAILED)
            include_content: Whether to include code content in reports
                           (default: True)
            include_diff: Whether to include diff summaries when available
                         (default: True)
            max_content_lines: Maximum lines of content to show per violation
                             (default: 10, 0 for unlimited)
        """
        if isinstance(format, str):
            try:
                self.format = ReportFormat(format.lower())
            except ValueError:
                self.format = ReportFormat.TEXT
        else:
            self.format = format

        self.output_file = output_file

        if isinstance(console_style, str):
            try:
                self.console_style = ConsoleStyle(console_style.lower())
            except ValueError:
                self.console_style = ConsoleStyle.DETAILED
        else:
            self.console_style = console_style

        self.include_content = include_content
        self.include_diff = include_diff
        self.max_content_lines = max_content_lines

        # Initialize rich console lazily
        self._console = None

    @property
    def console(self):
        """Get the Rich console, initializing if needed."""
        if self._console is None and _check_rich():
            self._console = _rich_console()
        return self._console

    def generate_report(self, result: ValidationResult, output: Optional[TextIO] = None) -> str:
        """
        Generate a formatted report for validation results.

        This method generates a report in the configured format and writes it
        to the specified output destination. The report includes a summary,
        violation details, and optionally code content and diffs.

        Args:
            result: ValidationResult object containing violations and statistics
            output: Optional file-like object to write to. If None, uses the
                   output_file specified during initialization or stdout.

        Returns:
            The generated report as a string (same content that was written)

        Raises:
            IOError: If unable to write to the output file
            ImportError: If YAML format requested but PyYAML not installed
        """
        if self.format == ReportFormat.JSON:
            report = self._generate_json_report(result)
        elif self.format == ReportFormat.YAML and YAML_AVAILABLE:
            report = self._generate_yaml_report(result)
        elif self.format == ReportFormat.HTML:
            report = self._generate_html_report(result)
        elif self.format == ReportFormat.MARKDOWN:
            report = self._generate_markdown_report(result)
        elif self.format == ReportFormat.CONSOLE and RICH_AVAILABLE:
            # Rich console output is generated differently
            self._generate_console_report(result)
            report = "Report displayed on console"
        else:
            report = self._generate_text_report(result)

        # Write to output if provided
        output_target = output or self.output_file
        if output_target:
            if isinstance(output_target, str):
                with open(output_target, "w", encoding="utf-8") as f:
                    f.write(report)
            else:
                output_target.write(report)

        return report

    def _generate_json_report(self, result: ValidationResult) -> str:
        """
        Generate a JSON report for validation results.

        Args:
            result: Validation result to report

        Returns:
            JSON report as string
        """
        report_dict = self._prepare_report_dict(result)
        return json.dumps(report_dict, indent=2)

    def _generate_yaml_report(self, result: ValidationResult) -> str:
        """
        Generate a YAML report for validation results.

        Args:
            result: Validation result to report

        Returns:
            YAML report as string
        """
        if not YAML_AVAILABLE:
            return "YAML not available. Install pyyaml package."

        report_dict = self._prepare_report_dict(result)
        return yaml.dump(report_dict, sort_keys=False)

    def _generate_text_report(self, result: ValidationResult) -> str:
        """
        Generate a plain text report for validation results.

        Args:
            result: Validation result to report

        Returns:
            Text report as string
        """
        lines = []

        lines.append("=========================")
        lines.append("CodeGuard Validation Report")
        lines.append("=========================")
        lines.append("")

        # Summary
        lines.append("Summary:")
        lines.append(f"  Files checked: {result.files_checked}")
        lines.append(f"  Violations found: {result.violations_found}")
        lines.append(f"  Critical violations: {result.critical_count}")
        lines.append(f"  Warning violations: {result.warning_count}")
        lines.append(f"  Info violations: {result.info_count}")
        lines.append(f"  Status: {result.status}")
        lines.append("")

        # Violations
        if result.violations_found > 0:
            lines.append("Violations:")
            lines.append("")

            for i, violation in enumerate(result.violations, 1):
                severity_prefix = {
                    "critical": "! CRITICAL ",
                    "warning": "! WARNING ",
                    "info": "  INFO    ",
                }.get(violation.severity, "  ")

                lines.append(f"{severity_prefix}Violation #{i}")
                lines.append(f"  File: {violation.file}:{violation.line}")
                lines.append(f"  Guard Type: {violation.guard_type}")
                if hasattr(violation, "violated_by") and violation.violated_by:
                    lines.append(f"  Violated By: {violation.violated_by}")
                lines.append(f"  Message: {violation.message}")
                if hasattr(violation, "guard_source") and violation.guard_source:
                    lines.append(f"  Guard Source: {violation.guard_source}")

                if self.include_diff and violation.diff_summary:
                    lines.append("  Diff:")
                    for diff_line in violation.diff_summary.splitlines():
                        lines.append(f"    {diff_line}")

                if self.include_content:
                    lines.append("  Original Content:")
                    orig_lines = violation.original_content.splitlines()[: self.max_content_lines]
                    for line in orig_lines:
                        lines.append(f"    {line}")
                    if len(violation.original_content.splitlines()) > self.max_content_lines:
                        lines.append(
                            f"    ... ({len(violation.original_content.splitlines()) - self.max_content_lines} more lines)"
                        )

                    lines.append("  Modified Content:")
                    mod_lines = violation.modified_content.splitlines()[: self.max_content_lines]
                    for line in mod_lines:
                        lines.append(f"    {line}")
                    if len(violation.modified_content.splitlines()) > self.max_content_lines:
                        lines.append(
                            f"    ... ({len(violation.modified_content.splitlines()) - self.max_content_lines} more lines)"
                        )

                lines.append("")
        else:
            lines.append("No violations found.")

        return "\n".join(lines)

    def _generate_html_report(self, result: ValidationResult) -> str:
        """
        Generate an HTML report for validation results.

        Args:
            result: Validation result to report

        Returns:
            HTML report as string
        """
        violations_html = []

        for i, violation in enumerate(result.violations, 1):
            severity_class = {"critical": "critical", "warning": "warning", "info": "info"}.get(
                violation.severity, ""
            )

            violation_html = f"""
            <div class="violation {severity_class}">
                <h3>Violation #{i} - {violation.severity.upper()}</h3>
                <div class="violation-details">
                    <p><strong>File:</strong> {violation.file}:{violation.line}</p>
                    <p><strong>Guard Type:</strong> {violation.guard_type}</p>
                    {f'<p><strong>Violated By:</strong> {violation.violated_by}</p>' if hasattr(violation, 'violated_by') and violation.violated_by else ''}
                    <p><strong>Message:</strong> {violation.message}</p>
                    {f'<p><strong>Guard Source:</strong> {violation.guard_source}</p>' if hasattr(violation, 'guard_source') and violation.guard_source else ''}
            """

            if self.include_diff and violation.diff_summary:
                violation_html += f"""
                    <div class="diff">
                        <h4>Diff:</h4>
                        <pre>{violation.diff_summary}</pre>
                    </div>
                """

            if self.include_content:
                orig_lines = violation.original_content.splitlines()[: self.max_content_lines]
                orig_content = "\n".join(orig_lines)
                if len(violation.original_content.splitlines()) > self.max_content_lines:
                    orig_content += f"\n... ({len(violation.original_content.splitlines()) - self.max_content_lines} more lines)"

                mod_lines = violation.modified_content.splitlines()[: self.max_content_lines]
                mod_content = "\n".join(mod_lines)
                if len(violation.modified_content.splitlines()) > self.max_content_lines:
                    mod_content += f"\n... ({len(violation.modified_content.splitlines()) - self.max_content_lines} more lines)"

                violation_html += f"""
                    <div class="content">
                        <h4>Original Content:</h4>
                        <pre>{orig_content}</pre>
                        <h4>Modified Content:</h4>
                        <pre>{mod_content}</pre>
                    </div>
                """

            violation_html += """
                </div>
            </div>
            """

            violations_html.append(violation_html)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CodeGuard Validation Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                }}
                h1, h2, h3, h4 {{
                    margin-top: 0;
                }}
                .summary {{
                    margin-bottom: 20px;
                    padding: 15px;
                    background-color: #f5f5f5;
                    border-radius: 5px;
                }}
                .summary table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .summary table td, .summary table th {{
                    padding: 8px;
                    text-align: left;
                }}
                .violation {{
                    margin-bottom: 20px;
                    padding: 15px;
                    border-radius: 5px;
                }}
                .critical {{
                    background-color: #ffebee;
                    border-left: 5px solid #f44336;
                }}
                .warning {{
                    background-color: #fff8e1;
                    border-left: 5px solid #ffc107;
                }}
                .info {{
                    background-color: #e3f2fd;
                    border-left: 5px solid #2196f3;
                }}
                .violation-details {{
                    margin-left: 10px;
                }}
                pre {{
                    background-color: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                .diff pre {{
                    white-space: pre-wrap;
                }}
                .success {{
                    color: #4caf50;
                    font-weight: bold;
                }}
                .failed {{
                    color: #f44336;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>CodeGuard Validation Report</h1>

            <div class="summary">
                <h2>Summary</h2>
                <table>
                    <tr>
                        <td><strong>Files Checked:</strong></td>
                        <td>{result.files_checked}</td>
                    </tr>
                    <tr>
                        <td><strong>Violations Found:</strong></td>
                        <td>{result.violations_found}</td>
                    </tr>
                    <tr>
                        <td><strong>Critical Violations:</strong></td>
                        <td>{result.critical_count}</td>
                    </tr>
                    <tr>
                        <td><strong>Warning Violations:</strong></td>
                        <td>{result.warning_count}</td>
                    </tr>
                    <tr>
                        <td><strong>Info Violations:</strong></td>
                        <td>{result.info_count}</td>
                    </tr>
                    <tr>
                        <td><strong>Status:</strong></td>
                        <td class="{result.status.lower()}">{result.status}</td>
                    </tr>
                </table>
            </div>

            <h2>Violations</h2>

            {f"<div class='violations'>{''.join(violations_html)}</div>" if result.violations_found > 0 else "<p>No violations found.</p>"}

        </body>
        </html>
        """

        return html

    def _generate_markdown_report(self, result: ValidationResult) -> str:
        """
        Generate a Markdown report for validation results.

        Args:
            result: Validation result to report

        Returns:
            Markdown report as string
        """
        lines = []

        lines.append("# CodeGuard Validation Report")
        lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Files Checked | {result.files_checked} |")
        lines.append(f"| Violations Found | {result.violations_found} |")
        lines.append(f"| Critical Violations | {result.critical_count} |")
        lines.append(f"| Warning Violations | {result.warning_count} |")
        lines.append(f"| Info Violations | {result.info_count} |")
        lines.append(f"| Status | {result.status} |")
        lines.append("")

        # Violations
        lines.append("## Violations")
        lines.append("")

        if result.violations_found > 0:
            for i, violation in enumerate(result.violations, 1):
                severity_emoji = {"critical": "❌", "warning": "⚠️", "info": "ℹ️"}.get(
                    violation.severity, ""
                )

                lines.append(f"### {severity_emoji} Violation #{i} - {violation.severity.upper()}")
                lines.append("")
                lines.append(f"**File:** {violation.file}:{violation.line}")
                lines.append(f"**Guard Type:** {violation.guard_type}")
                if hasattr(violation, "violated_by") and violation.violated_by:
                    lines.append(f"**Violated By:** {violation.violated_by}")
                lines.append(f"**Message:** {violation.message}")
                if hasattr(violation, "guard_source") and violation.guard_source:
                    lines.append(f"**Guard Source:** {violation.guard_source}")
                lines.append("")

                if self.include_diff and violation.diff_summary:
                    lines.append("#### Diff:")
                    lines.append("")
                    lines.append("```diff")
                    lines.append(violation.diff_summary)
                    lines.append("```")
                    lines.append("")

                if self.include_content:
                    lines.append("#### Original Content:")
                    lines.append("")
                    lines.append("```")
                    orig_lines = violation.original_content.splitlines()[: self.max_content_lines]
                    lines.append("\n".join(orig_lines))
                    if len(violation.original_content.splitlines()) > self.max_content_lines:
                        lines.append(
                            f"... ({len(violation.original_content.splitlines()) - self.max_content_lines} more lines)"
                        )
                    lines.append("```")
                    lines.append("")

                    lines.append("#### Modified Content:")
                    lines.append("")
                    lines.append("```")
                    mod_lines = violation.modified_content.splitlines()[: self.max_content_lines]
                    lines.append("\n".join(mod_lines))
                    if len(violation.modified_content.splitlines()) > self.max_content_lines:
                        lines.append(
                            f"... ({len(violation.modified_content.splitlines()) - self.max_content_lines} more lines)"
                        )
                    lines.append("```")
                    lines.append("")
        else:
            lines.append("No violations found.")
            lines.append("")

        return "\n".join(lines)

    def _generate_console_report(self, result: ValidationResult) -> None:
        """
        Generate a rich console report for validation results.

        Args:
            result: Validation result to report
        """
        if not _check_rich() or not self.console:
            print(self._generate_text_report(result))
            return

        # Summary table
        summary_table = _rich_table(title="CodeGuard Validation Summary")
        summary_table.add_column("Metric")
        summary_table.add_column("Value")

        summary_table.add_row("Files Checked", str(result.files_checked))
        summary_table.add_row("Violations Found", str(result.violations_found))
        summary_table.add_row("Critical Violations", str(result.critical_count))
        summary_table.add_row("Warning Violations", str(result.warning_count))
        summary_table.add_row("Info Violations", str(result.info_count))

        status_color = "green" if result.status == "SUCCESS" else "red"
        status_text = _rich_text(result.status, style=f"bold {status_color}")
        summary_table.add_row("Status", status_text)

        self.console.print(summary_table)
        self.console.print()

        # Violations
        if result.violations_found > 0:
            self.console.print("[bold]Violations:[/bold]")
            self.console.print()

            for i, violation in enumerate(result.violations, 1):
                severity_color = {"critical": "red", "warning": "yellow", "info": "blue"}.get(
                    violation.severity, "white"
                )

                if self.console_style == ConsoleStyle.COMPACT:
                    # Compact style
                    self.console.print(
                        f"[bold {severity_color}]#{i}[/bold {severity_color}] [{severity_color}]{violation.severity.upper()}[/{severity_color}] {violation.file}:{violation.line} - {violation.message}"
                    )
                else:
                    # Detailed style
                    panel_title = f"Violation #{i} - {violation.severity.upper()}"

                    content = []
                    content.append(f"[bold]File:[/bold] {violation.file}:{violation.line}")
                    content.append(f"[bold]Guard Type:[/bold] {violation.guard_type}")
                    if hasattr(violation, "violated_by") and violation.violated_by:
                        content.append(f"[bold]Violated By:[/bold] {violation.violated_by}")
                    content.append(f"[bold]Message:[/bold] {violation.message}")
                    if hasattr(violation, "guard_source") and violation.guard_source:
                        content.append(f"[bold]Guard Source:[/bold] {violation.guard_source}")

                    if self.include_diff and violation.diff_summary:
                        content.append("")
                        content.append("[bold]Diff:[/bold]")

                        diff_syntax = _rich_syntax(
                            violation.diff_summary,
                            "diff",
                            theme="monokai",
                            line_numbers=False,
                            word_wrap=True,
                        )
                        content.append(diff_syntax)

                    if self.include_content and self.console_style == ConsoleStyle.DETAILED:
                        content.append("")
                        content.append("[bold]Original Content:[/bold]")

                        # Determine language for syntax highlighting
                        language = "python"  # Default
                        if violation.file.endswith((".js", ".jsx")):
                            language = "javascript"
                        elif violation.file.endswith((".ts", ".tsx")):
                            language = "typescript"
                        elif violation.file.endswith(".java"):
                            language = "java"
                        elif violation.file.endswith(".cs"):
                            language = "csharp"
                        elif violation.file.endswith((".c", ".cpp", ".h", ".hpp")):
                            language = "cpp"

                        orig_lines = violation.original_content.splitlines()[
                            : self.max_content_lines
                        ]
                        orig_content = "\n".join(orig_lines)

                        original_syntax = _rich_syntax(
                            orig_content,
                            language,
                            theme="monokai",
                            line_numbers=True,
                            start_line=violation.line,
                            word_wrap=True,
                        )
                        content.append(original_syntax)

                        if len(violation.original_content.splitlines()) > self.max_content_lines:
                            content.append(
                                f"... ({len(violation.original_content.splitlines()) - self.max_content_lines} more lines)"
                            )

                        content.append("")
                        content.append("[bold]Modified Content:[/bold]")

                        mod_lines = violation.modified_content.splitlines()[
                            : self.max_content_lines
                        ]
                        mod_content = "\n".join(mod_lines)

                        modified_syntax = _rich_syntax(
                            mod_content,
                            language,
                            theme="monokai",
                            line_numbers=True,
                            start_line=violation.line,
                            word_wrap=True,
                        )
                        content.append(modified_syntax)

                        if len(violation.modified_content.splitlines()) > self.max_content_lines:
                            content.append(
                                f"... ({len(violation.modified_content.splitlines()) - self.max_content_lines} more lines)"
                            )

                    panel = _rich_panel(
                        "\n".join(str(item) for item in content),
                        title=panel_title,
                        border_style=severity_color,
                    )
                    self.console.print(panel)
        else:
            self.console.print("[bold green]No violations found.[/bold green]")

    def _prepare_report_dict(self, result: ValidationResult) -> Dict[str, Any]:
        """
        Prepare a dictionary representation of the validation result.

        Args:
            result: Validation result to convert

        Returns:
            Dictionary representation
        """
        report_dict = result.to_dict()

        # Filter out content if not included
        if not self.include_content:
            for violation in report_dict["violations"]:
                violation.pop("original_content", None)
                violation.pop("modified_content", None)

        # Filter out diff if not included
        if not self.include_diff:
            for violation in report_dict["violations"]:
                violation.pop("diff_summary", None)

        return report_dict
