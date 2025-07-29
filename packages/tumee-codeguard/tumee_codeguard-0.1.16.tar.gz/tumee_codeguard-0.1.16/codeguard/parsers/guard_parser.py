"""
Guard Annotation Parser.

This module is responsible for parsing and extracting guard annotations from
source code comments across different programming languages.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, NamedTuple

from .language_parser import Comment, LanguageType, Region
from .language_parser import SemanticScope as LangSemanticScope


class SemanticScope(Enum):
    """
    Semantic scope identifiers for guard annotations.

    These scopes define what part of the code a guard annotation applies to.
    Guards can target specific parts of code structures like just the signature,
    just the body, or the entire construct.

    Core scopes:
        signature: Function/method/class signatures only
        body: Implementation body only
        function: Entire function (signature + body)
        block: Current code block
        statement: Single logical statement
        class_: Entire class definition
        method: Entire method
        docstring: Documentation strings
        import_: Import statements
        decorator: Decorators/annotations
        value: Variable values only
        expression: Single expression

    Aliases are provided for convenience (e.g., 'sig' for 'signature')
    """

    # Core scopes
    signature = "signature"  # Function/method/class signatures only
    body = "body"  # Implementation body only
    function = "function"  # Entire function (signature + body)
    block = "block"  # Current code block
    statement = "statement"  # Single logical statement
    class_ = "class"  # Entire class definition (using _ to avoid keyword)
    method = "method"  # Entire method
    docstring = "docstring"  # Documentation strings
    import_ = "import"  # Import statements (using _ to avoid keyword)
    decorator = "decorator"  # Decorators/annotations
    value = "value"  # Variable values only
    expression = "expression"  # Single expression

    # Aliases
    sig = "signature"
    func = "function"
    stmt = "statement"
    doc = "docstring"
    imports = "import"
    dec = "decorator"
    val = "value"
    expr = "expression"


class GuardWho(Enum):
    """
    Target audience for guard annotations.

    Defines who the guard rule applies to:
        ai: AI systems and code generation tools
        human: Human developers
        all: Both AI and human developers

    Legacy aliases (AI, HU, ALL) are supported for backwards compatibility.
    """

    ai = "ai"  # AI systems
    human = "human"  # Human developers
    # Legacy aliases for backwards compatibility
    AI = "ai"
    HU = "human"
    ALL = "all"  # Both AI and human


class GuardPermission(Enum):
    """
    Permission levels for guard annotations.

    Defines what operations are allowed on guarded code:
        r: Read-only - can reference/read but not modify
        w: Write - full access to read and modify
        n: None - no access (cannot reference, read, or modify)
        context: Context file marker (implies read permission)

    Various aliases are supported for flexibility:
        - Legacy: RO (read-only), ED (editable), FX (fixed)
        - Descriptive: read, write, readonly, readwrite, none
    """

    r = "r"  # Read-Only
    w = "w"  # Write
    n = "n"  # None/No access
    none = "n"  # Alias for n
    context = "context"  # Context file (implies read)
    # Legacy aliases for backwards compatibility
    RO = "r"
    ED = "w"
    FX = "n"
    # Flexible matching aliases
    read = "r"
    write = "w"
    readonly = "r"
    readwrite = "w"


@dataclass
class GuardDirective:
    """
    Represents a parsed guard directive from source code.

    A guard directive is a single guard annotation that specifies who can
    perform what actions on a piece of code. Multiple directives can apply
    to the same code region.

    Attributes:
        who: Target audience (AI, human, or all)
        permission: Permission level (read, write, or none)
        description: Original comment text containing the guard
        line_number: Line number where the guard was found
        line_count: Optional number of lines the guard applies to
        identifier: Optional specific identifier (e.g., "claude-4")
        identifiers: Optional list of multiple identifiers
        scope: Optional semantic scope (function, class, etc.)
        compound_scope: Optional compound scope expression (e.g., "def+doc")
        excluded_scopes: Optional list of excluded scopes in compound
        context_metadata: Optional metadata for context files
    """

    who: GuardWho
    permission: GuardPermission
    description: str
    line_number: int
    line_count: Optional[int] = None
    identifier: Optional[str] = None  # Specific AI model, team, etc.
    identifiers: Optional[List[str]] = None  # Multiple identifiers
    scope: Optional[SemanticScope] = None  # Semantic scope
    compound_scope: Optional[str] = None  # Compound scope (e.g., "def+doc")
    excluded_scopes: Optional[List[str]] = None  # Excluded scopes in compound
    context_metadata: Optional[Dict[str, str]] = None  # Context metadata (priority, scope, etc.)

    @property
    def tag(self) -> str:
        """Get the guard tag in standard format."""
        who_part = f"{self.who.value}"
        if self.identifiers:
            who_part += f"[{','.join(self.identifiers)}]"
        elif self.identifier:
            who_part += f"[{self.identifier}]"

        perm_part = f"{self.permission.value}"
        if self.compound_scope:
            perm_part += f".{self.compound_scope}"
        elif self.scope:
            perm_part += f".{self.scope.value}"
        elif self.line_count is not None:
            perm_part += f".{self.line_count}"

        return f"@guard:{who_part}:{perm_part}"

    def __str__(self) -> str:
        """String representation of the guard directive."""
        if self.description:
            return f"{self.tag} {self.description}"
        return self.tag

    def applies_to_identifier(self, identifier: str) -> bool:
        """Check if this directive applies to a specific identifier."""
        # If no specific identifiers, applies to all (wildcard)
        if not self.identifier and not self.identifiers:
            return True

        # Check single identifier
        if self.identifier:
            return self.identifier == "*" or self.identifier == identifier

        # Check multiple identifiers
        if self.identifiers:
            return "*" in self.identifiers or identifier in self.identifiers

        return False


class GuardStackEntry(NamedTuple):
    """
    Represents an entry in the guard stack.
    
    Attributes:
        directive: The guard directive
        start_line: Line where this guard starts applying
        end_line: Line where this guard stops applying (None for unbounded)
        scope_info: Optional semantic scope information
    """
    directive: 'GuardDirective'
    start_line: int
    end_line: Optional[int] = None
    scope_info: Optional[LangSemanticScope] = None


@dataclass
class GuardedRegion:
    """
    Represents a code region protected by guard annotations.

    A guarded region is a contiguous block of code that has one or more
    guard directives applied to it. The region's permissions are determined
    by combining all applicable directives.

    Attributes:
        start_line: Starting line number of the guarded region (1-based)
        end_line: Ending line number of the guarded region (inclusive)
        content: The actual code content within the region
        directives: List of guard directives that apply to this region
        region_name: Optional name for the region (e.g., from #region markers)
    """

    start_line: int
    end_line: int
    content: str
    directives: List[GuardDirective]
    region_name: Optional[str] = None

    @property
    def permissions(self) -> Dict[GuardWho, GuardPermission]:
        """Get a mapping of target audience to permission level."""
        return {d.who: d.permission for d in self.directives}

    def is_editable_by(self, who: GuardWho, identifier: Optional[str] = None) -> bool:
        """
        Check if the region is editable by the specified target.

        Args:
            who: Target to check editability for
            identifier: Specific identifier (e.g., "claude-4", "security-team")

        Returns:
            True if editable, False otherwise
        """
        # Find the most specific applicable directive
        most_specific_permission = None

        for directive in self.directives:
            if directive.who != who:
                continue

            # Check if directive applies to this identifier
            if identifier and not directive.applies_to_identifier(identifier):
                continue

            # More specific directives (with identifiers) take precedence
            if directive.identifier or directive.identifiers:
                most_specific_permission = directive.permission
                break  # Found specific match
            else:
                # Wildcard directive, use if no specific found
                if most_specific_permission is None:
                    most_specific_permission = directive.permission

        # Check if there's an "all" rule that applies
        if most_specific_permission is None:
            all_who = GuardWho("all") if hasattr(GuardWho, "all") else GuardWho.ALL
            for directive in self.directives:
                if directive.who == all_who:
                    if not identifier or directive.applies_to_identifier(identifier):
                        most_specific_permission = directive.permission
                        break

        # Apply permission if found
        if most_specific_permission is not None:
            return most_specific_permission == GuardPermission.w

        # Default: editable if no rules specified
        return True

    def is_fixed_for(self, who: GuardWho, identifier: Optional[str] = None) -> bool:
        """
        Check if the region is fixed (unchangeable) for the specified target.

        Args:
            who: Target to check fixity for
            identifier: Specific identifier (e.g., "claude-4", "security-team")

        Returns:
            True if fixed, False otherwise
        """
        # Find the most specific applicable directive
        most_specific_permission = None

        for directive in self.directives:
            if directive.who != who:
                continue

            # Check if directive applies to this identifier
            if identifier and not directive.applies_to_identifier(identifier):
                continue

            # More specific directives (with identifiers) take precedence
            if directive.identifier or directive.identifiers:
                most_specific_permission = directive.permission
                break  # Found specific match
            else:
                # Wildcard directive, use if no specific found
                if most_specific_permission is None:
                    most_specific_permission = directive.permission

        # Check if there's an "all" rule that applies
        if most_specific_permission is None:
            all_who = GuardWho("all") if hasattr(GuardWho, "all") else GuardWho.ALL
            for directive in self.directives:
                if directive.who == all_who:
                    if not identifier or directive.applies_to_identifier(identifier):
                        most_specific_permission = directive.permission
                        break

        # Apply permission if found
        if most_specific_permission is not None:
            return most_specific_permission == GuardPermission.n

        # Default: not fixed if no rules specified
        return False


class GuardParser:
    """
    Parser for guard annotations in source code.

    This class is responsible for extracting guard annotations from comments
    and associating them with the appropriate code regions. It supports
    various guard syntax formats including:

    - Basic: @guard:ai:r
    - With identifier: @guard:ai[claude-4]:r
    - With scope: @guard:ai:r.function
    - With metadata: @guard:ai:r[priority=high]
    - With description: @guard:ai:r This is protected code

    The parser also handles legacy formats and semantic scope associations.

    Attributes:
        GUARD_PATTERN: Compiled regex for matching guard annotations
    """

    # Regular expression to match guard annotations
    # Supports: @guard:target[identifier]:permission[metadata][.scope][+scope][-scope]
    GUARD_PATTERN = re.compile(
        r"@guard:([a-z]+)(?:\[([^\]]+)\])?:([a-z]+)(?:\[([^\]]+)\])?(?:\.([a-zA-Z0-9_+\-]+))?(?:\s+(.*))?",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        """Initialize the guard parser."""
        pass

    def parse_guard_annotation(self, line: str, line_number: int) -> Optional[GuardDirective]:
        """
        Parse a line of text to extract a guard annotation.

        This method looks for guard annotations in various formats including
        the standard @guard syntax and legacy formats. It handles identifier
        extraction, permission parsing, scope detection, and metadata parsing.

        Args:
            line: Line of text to parse (typically from a comment)
            line_number: Line number in the source file (1-based)

        Returns:
            GuardDirective object if a valid guard annotation is found,
            None if no guard annotation is present or if parsing fails

        Example:
            >>> parser.parse_guard_annotation("# @guard:ai:r.function", 10)
            GuardDirective(who=GuardWho.ai, permission=GuardPermission.r, ...)
        """
        match = self.GUARD_PATTERN.search(line)
        if not match:
            return None

        (
            who_str,
            identifier_str,
            permission_str,
            metadata_str,
            scope_str,
            description,
        ) = match.groups()
        description = description.strip() if description else ""

        # Parse identifiers (may be comma-separated)
        identifiers = None
        identifier = None
        if identifier_str:
            if "," in identifier_str:
                identifiers = [id.strip() for id in identifier_str.split(",")]
            else:
                identifier = identifier_str.strip()

        # Parse context metadata
        context_metadata = None
        if metadata_str and permission_str == "context":
            context_metadata = {}
            # Parse key=value pairs
            for pair in metadata_str.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    context_metadata[key.strip()] = value.strip()

        # Parse scope information
        line_count = None
        scope = None
        compound_scope = None
        excluded_scopes = None

        if scope_str:
            # Check if it's a line count (all digits)
            if scope_str.isdigit():
                line_count = int(scope_str)
            else:
                # Check for compound scope (contains + or -)
                if "+" in scope_str or "-" in scope_str:
                    compound_scope = scope_str
                    # Parse excluded scopes
                    if "-" in scope_str:
                        parts = scope_str.split("-")
                        excluded_scopes = [s.strip() for s in parts[1:] if s.strip()]
                else:
                    # Try to parse as semantic scope
                    try:
                        # Handle aliases and special cases
                        scope_value = scope_str.lower()
                        if scope_value == "class":
                            scope = SemanticScope.class_
                        elif scope_value == "import" or scope_value == "imports":
                            scope = SemanticScope.import_
                        else:
                            # Try direct enum lookup
                            scope = SemanticScope(scope_value)
                    except ValueError:
                        # Try by name (for aliases)
                        try:
                            scope = SemanticScope[scope_value]
                        except (ValueError, KeyError):
                            # Check if it's a valid scope alias
                            scope_aliases = {
                                "sig": SemanticScope.signature,
                                "func": SemanticScope.function,
                                "doc": SemanticScope.docstring,
                                "stmt": SemanticScope.statement,
                                "expr": SemanticScope.expression,
                                "dec": SemanticScope.decorator,
                                "val": SemanticScope.value,
                            }
                            if scope_value in scope_aliases:
                                scope = scope_aliases[scope_value]
                            else:
                                # Invalid scope - return None to reject directive
                                return None

        # Normalize to lowercase for enum lookup
        who_str = who_str.lower()
        permission_str = permission_str.lower()

        try:
            # Try direct enum lookup first
            who = GuardWho(who_str)
            # Handle flexible permission matching
            if permission_str in ["read", "readonly"]:
                permission = GuardPermission.r
            elif permission_str in ["write", "readwrite"]:
                permission = GuardPermission.w
            elif permission_str == "none":
                permission = GuardPermission.n
            else:
                permission = GuardPermission(permission_str)
        except ValueError:
            # Try legacy names
            try:
                who = GuardWho[who_str.upper()]
                permission = GuardPermission[permission_str.upper()]
            except (ValueError, KeyError):
                # Invalid who or permission value
                return None

        return GuardDirective(
            who=who,
            permission=permission,
            description=description,
            line_number=line_number,
            line_count=line_count,
            identifier=identifier,
            identifiers=identifiers,
            scope=scope,
            compound_scope=compound_scope,
            excluded_scopes=excluded_scopes,
            context_metadata=context_metadata,
        )

    def extract_guard_directives_from_comments(
        self, comments: List[Comment]
    ) -> List[Tuple[Comment, List[GuardDirective]]]:
        """
        Extract guard directives from a list of comments.

        Args:
            comments: List of comment objects

        Returns:
            List of tuples containing (comment, directives)
        """
        result = []

        for comment in comments:
            directives = []

            # For block comments, check each line
            if comment.is_block_comment:
                lines = comment.text.splitlines()
                for i, line in enumerate(lines):
                    # Calculate line number within the file
                    line_number = comment.start_line + i
                    directive = self.parse_guard_annotation(line, line_number)
                    if directive:
                        directives.append(directive)
            else:
                # Single line comment
                directive = self.parse_guard_annotation(comment.text, comment.start_line)
                if directive:
                    directives.append(directive)

            if directives:
                result.append((comment, directives))

        return result

    def associate_directives_with_code(
        self,
        source_lines: List[str],
        comment_directives: List[Tuple[Comment, List[GuardDirective]]],
        regions: List[Region],
        semantic_scopes: Optional[List["SemanticScope"]] = None,
    ) -> List[GuardedRegion]:
        """
        Associate guard directives with code regions.

        Args:
            source_lines: Lines of source code
            comment_directives: List of (comment, directives) tuples
            regions: List of explicit regions in the code

        Returns:
            List of guarded regions
        """
        guarded_regions = []

        # Case 1: Explicit regions with guard directives
        region_map = {r.start_line: r for r in regions}
        for comment, directives in comment_directives:
            # Check if the comment precedes a region
            next_line = comment.end_line + 1
            if next_line in region_map:
                region = region_map[next_line]
                content = "\n".join(source_lines[region.start_line - 1 : region.end_line])
                guarded_regions.append(
                    GuardedRegion(
                        start_line=region.start_line,
                        end_line=region.end_line,
                        content=content,
                        directives=directives,
                        region_name=region.name,
                    )
                )
                continue

        # Case 2: Semantic scope-based guard directives
        if semantic_scopes:
            for comment, directives in comment_directives:
                # Check if any directive has a semantic scope OR no line count
                # (guards without explicit scope should apply to next semantic structure)
                for directive in directives:
                    if directive.scope or directive.compound_scope or directive.line_count is None:
                        # Find the semantic scope that starts after this comment
                        next_line = comment.end_line + 1

                        # Find matching semantic scope
                        for scope in semantic_scopes:
                            if scope.start_line >= next_line:
                                # Apply the guard based on the semantic scope type
                                start_line = scope.start_line
                                end_line = scope.end_line
                                content = scope.content

                                # Handle specific scope parts
                                if directive.scope:
                                    if (
                                        directive.scope == SemanticScope.signature
                                        and scope.definition_lines
                                    ):
                                        start_line, end_line = scope.definition_lines
                                        content = "\n".join(source_lines[start_line - 1 : end_line])
                                    elif directive.scope == SemanticScope.body and scope.body_lines:
                                        start_line, end_line = scope.body_lines
                                        content = "\n".join(source_lines[start_line - 1 : end_line])
                                    elif (
                                        directive.scope == SemanticScope.docstring
                                        and scope.docstring_lines
                                    ):
                                        start_line, end_line = scope.docstring_lines
                                        content = "\n".join(source_lines[start_line - 1 : end_line])

                                # Handle compound scopes
                                elif directive.compound_scope:
                                    lines_to_include = []
                                    compound = directive.compound_scope

                                    # Parse compound scope (e.g., "def+doc", "func-doc")
                                    if "+" in compound:
                                        # Addition - include multiple parts
                                        parts = compound.split("+")
                                        for part in parts:
                                            part = part.strip()
                                            if (
                                                part in ["def", "definition"]
                                                and scope.definition_lines
                                            ):
                                                for i in range(
                                                    scope.definition_lines[0] - 1,
                                                    scope.definition_lines[1],
                                                ):
                                                    if i not in lines_to_include:
                                                        lines_to_include.append(i)
                                            elif (
                                                part in ["doc", "docstring"]
                                                and scope.docstring_lines
                                            ):
                                                for i in range(
                                                    scope.docstring_lines[0] - 1,
                                                    scope.docstring_lines[1],
                                                ):
                                                    if i not in lines_to_include:
                                                        lines_to_include.append(i)
                                            elif part == "body" and scope.body_lines:
                                                for i in range(
                                                    scope.body_lines[0] - 1, scope.body_lines[1]
                                                ):
                                                    if i not in lines_to_include:
                                                        lines_to_include.append(i)

                                    elif "-" in compound:
                                        # Subtraction - exclude parts
                                        base_part, exclude_parts = compound.split("-", 1)
                                        base_part = base_part.strip()

                                        # Start with the base scope
                                        if base_part in ["func", "function", "method", "class"]:
                                            lines_to_include = list(
                                                range(scope.start_line - 1, scope.end_line)
                                            )

                                        # Remove excluded parts
                                        exclude_list = exclude_parts.split("-")
                                        for exclude in exclude_list:
                                            exclude = exclude.strip()
                                            if (
                                                exclude in ["doc", "docstring"]
                                                and scope.docstring_lines
                                            ):
                                                for i in range(
                                                    scope.docstring_lines[0] - 1,
                                                    scope.docstring_lines[1],
                                                ):
                                                    if i in lines_to_include:
                                                        lines_to_include.remove(i)

                                    # Create content from selected lines
                                    if lines_to_include:
                                        lines_to_include.sort()
                                        start_line = lines_to_include[0] + 1
                                        end_line = lines_to_include[-1] + 1
                                        content_lines = []
                                        for i in lines_to_include:
                                            if i < len(source_lines):
                                                content_lines.append(source_lines[i])
                                        content = "\n".join(content_lines)

                                # If no specific scope was requested and no line count,
                                # apply to the entire semantic structure
                                elif not directive.scope and not directive.compound_scope and directive.line_count is None:
                                    # Apply to entire semantic structure
                                    pass  # Already set start_line, end_line, content from scope

                                # Create guarded region
                                guarded_regions.append(
                                    GuardedRegion(
                                        start_line=start_line,
                                        end_line=end_line,
                                        content=content,
                                        directives=[directive],
                                    )
                                )
                                break

        # Case 3: Single-line guard directives (apply to next non-comment line)
        # Only use this fallback when no semantic scopes are available or for explicit line counts
        # Sort comment_directives by line number
        comment_directives.sort(key=lambda x: x[0].start_line)

        for comment, directives in comment_directives:
            # Skip comments that we've already associated with regions
            if any(gr.start_line == comment.end_line + 1 for gr in guarded_regions):
                continue
            
            # Skip if we have semantic scopes and no explicit line count
            # (these should have been handled in Case 2)
            if semantic_scopes and not any(d.line_count is not None for d in directives):
                continue

            # Find the next non-comment line
            next_line = comment.end_line + 1
            while next_line <= len(source_lines):
                # Skip lines that are part of other comments
                is_comment_line = any(
                    c.start_line <= next_line <= c.end_line for c, _ in comment_directives
                )

                if not is_comment_line:
                    # Found a non-comment line
                    # Process based on line count or indentation
                    start_idx = next_line - 1  # Convert to 0-based index
                    if start_idx >= len(source_lines):
                        break

                    # Check for line count in directives
                    has_line_count = any(d.line_count is not None for d in directives)

                    if has_line_count:
                        # Use the specified line count for region size
                        max_line_count = max((d.line_count or 0) for d in directives)
                        end_idx = min(start_idx + max_line_count - 1, len(source_lines) - 1)
                    else:
                        # Determine region end based on indentation (traditional approach)
                        start_line_content = source_lines[start_idx]
                        start_indent = len(start_line_content) - len(start_line_content.lstrip())

                        # Find all lines with same or greater indentation
                        end_idx = start_idx
                        for i in range(start_idx + 1, len(source_lines)):
                            line = source_lines[i]
                            if not line.strip():  # Skip empty lines
                                end_idx = i
                                continue

                            indent = len(line) - len(line.lstrip())
                            if indent >= start_indent:
                                end_idx = i
                            else:
                                break

                    # Create guarded region
                    content = "\n".join(source_lines[start_idx : end_idx + 1])
                    guarded_regions.append(
                        GuardedRegion(
                            start_line=next_line,
                            end_line=end_idx + 1,  # Convert back to 1-based index
                            content=content,
                            directives=directives,
                        )
                    )
                    break

                next_line += 1

        # Case 3: Block comment guard directives (apply to next line after comment)
        # Already handled in the loop above

        return guarded_regions

    def build_regions_with_stack(
        self,
        source_lines: List[str],
        comment_directives: List[Tuple[Comment, List[GuardDirective]]],
        semantic_scopes: Optional[List[LangSemanticScope]] = None,
    ) -> List[GuardedRegion]:
        """
        Build guarded regions using a stack-based approach for proper precedence.
        
        This method processes the file line by line, maintaining a stack of active
        guards and creating regions based on the effective permissions at each line.
        
        Args:
            source_lines: Lines of source code
            comment_directives: List of (comment, directives) tuples
            semantic_scopes: Optional list of semantic scopes
            
        Returns:
            List of guarded regions with proper precedence handling
        """
        # Create a map of line -> directives for easy lookup
        directive_map: Dict[int, List[GuardDirective]] = {}
        for comment, directives in comment_directives:
            directive_map[comment.end_line] = directives
        
        # Stack to track active guards
        guard_stack: List[GuardStackEntry] = []
        
        # List to collect regions as we build them
        regions: List[GuardedRegion] = []
        
        # Current region being built
        current_region_start: Optional[int] = None
        current_region_lines: List[str] = []
        current_effective_directive: Optional[GuardDirective] = None
        
        # Process each line
        for line_idx, line in enumerate(source_lines):
            line_num = line_idx + 1  # 1-based line numbers
            
            # Step 1: Check for new guard directives on this line
            if line_num in directive_map:  # Check comment line
                for directive in directive_map[line_num]:
                    # Guards apply starting from the guard comment line
                    start_line = line_num
                    
                    # Calculate end line for this directive
                    if directive.line_count is not None:
                        # Line-limited guard
                        end_line = start_line + directive.line_count - 1
                        guard_stack.append(GuardStackEntry(
                            directive, start_line, end_line, None
                        ))
                    elif directive.scope or directive.compound_scope:
                        # Semantic scope guard - find matching scope
                        end_line = None
                        if semantic_scopes:
                            for scope in semantic_scopes:
                                if scope.start_line >= start_line:
                                    # Apply scope-specific filtering
                                    if directive.scope == SemanticScope.signature and scope.definition_lines:
                                        # Only protect the signature/definition line(s)
                                        guard_start, guard_end = scope.definition_lines
                                        guard_stack.append(GuardStackEntry(
                                            directive, guard_start, guard_end, scope
                                        ))
                                        end_line = guard_end
                                    elif directive.scope == SemanticScope.body and scope.body_lines:
                                        # Only protect the body (not signature/definition)
                                        guard_start, guard_end = scope.body_lines
                                        guard_stack.append(GuardStackEntry(
                                            directive, guard_start, guard_end, scope
                                        ))
                                        end_line = guard_end
                                    elif directive.scope == SemanticScope.docstring and scope.docstring_lines:
                                        # Only protect the docstring
                                        guard_start, guard_end = scope.docstring_lines
                                        guard_stack.append(GuardStackEntry(
                                            directive, guard_start, guard_end, scope
                                        ))
                                        end_line = guard_end
                                    elif directive.compound_scope:
                                        # Handle compound scopes later in region building
                                        guard_stack.append(GuardStackEntry(
                                            directive, scope.start_line, scope.end_line, scope
                                        ))
                                        end_line = scope.end_line
                                    else:
                                        # Default: protect entire scope
                                        guard_stack.append(GuardStackEntry(
                                            directive, scope.start_line, scope.end_line, scope
                                        ))
                                        end_line = scope.end_line
                                    break
                        if end_line is None:
                            # Semantic scope requested but not found - skip
                            continue
                    elif semantic_scopes:
                        # No explicit scope but semantic scopes available
                        # Apply to next semantic structure
                        for scope in semantic_scopes:
                            if scope.start_line >= start_line:
                                guard_stack.append(GuardStackEntry(
                                    directive, scope.start_line, scope.end_line, scope
                                ))
                                break
                        else:
                            # No semantic scope found after guard - unbounded
                            guard_stack.append(GuardStackEntry(
                                directive, start_line, None, None
                            ))
                    else:
                        # Unbounded guard (no semantic scopes available)
                        guard_stack.append(GuardStackEntry(
                            directive, start_line, None, None
                        ))
            
            # Step 2: Remove expired guards
            guard_stack = [
                entry for entry in guard_stack
                if entry.end_line is None or line_num <= entry.end_line
            ]
            
            # Step 3: Determine effective directive for this line
            effective_directive = None
            if guard_stack:
                # Get the top of stack (most recent guard)
                top_entry = guard_stack[-1]
                if line_num >= top_entry.start_line:
                    effective_directive = top_entry.directive
            
            # Step 4: Build or extend regions
            if effective_directive != current_effective_directive:
                # Permission changed - close current region if any
                if current_region_start is not None and current_region_lines:
                    regions.append(GuardedRegion(
                        start_line=current_region_start,
                        end_line=line_num - 1,
                        content="\n".join(current_region_lines),
                        directives=[current_effective_directive],
                    ))
                
                # Start new region if we have a directive
                if effective_directive:
                    current_region_start = line_num
                    current_region_lines = [line]
                    current_effective_directive = effective_directive
                else:
                    current_region_start = None
                    current_region_lines = []
                    current_effective_directive = None
            else:
                # Same permission - extend current region
                if current_region_start is not None:
                    current_region_lines.append(line)
        
        # Close final region if any
        if current_region_start is not None and current_region_lines:
            regions.append(GuardedRegion(
                start_line=current_region_start,
                end_line=len(source_lines),
                content="\n".join(current_region_lines),
                directives=[current_effective_directive],
            ))
        
        return regions

    def extract_guarded_regions(
        self,
        source_code: str,
        language_type: LanguageType,
        comments: List[Comment],
        regions: List[Region],
        semantic_scopes: Optional[List[LangSemanticScope]] = None,
    ) -> List[GuardedRegion]:
        """
        Extract guarded regions from source code.

        Args:
            source_code: Source code content
            language_type: Programming language
            comments: Extracted comments from the source code
            regions: Extracted regions from the source code
            semantic_scopes: Extracted semantic scopes from the source code

        Returns:
            List of guarded regions found in the source code
        """
        source_lines = source_code.splitlines()

        # Extract guard directives from comments
        comment_directives = self.extract_guard_directives_from_comments(comments)

        # Use the new stack-based approach
        guarded_regions = self.build_regions_with_stack(
            source_lines, comment_directives, semantic_scopes
        )

        return guarded_regions

    def extract_guarded_regions_simple(self, source_code: str) -> List[GuardedRegion]:
        """
        Simple extraction of guarded regions from source code.

        This is a simplified version that doesn't use language-specific parsing.
        It uses a stack-based approach to handle overlapping guards correctly.
        
        Note: Without semantic parsing, semantic scope tags (like .func, .body) 
        will result in an error.

        Args:
            source_code: Source code content

        Returns:
            List of guarded regions found in the source code
        """
        lines = source_code.splitlines()
        
        # First pass: find all guard directives
        directive_map: Dict[int, GuardDirective] = {}
        for i, line in enumerate(lines):
            line_number = i + 1  # 1-based line numbering
            directive = self.parse_guard_annotation(line, line_number)
            
            if directive:
                # Check for semantic scope without parsing capability
                if directive.scope or directive.compound_scope:
                    raise ValueError(
                        f"Semantic scope guard at line {line_number} requires language parsing. "
                        f"Use extract_guarded_regions() with proper language parser instead."
                    )
                directive_map[line_number] = directive
        
        # Stack to track active guards
        guard_stack: List[GuardStackEntry] = []
        
        # List to collect regions
        regions: List[GuardedRegion] = []
        
        # Current region being built
        current_region_start: Optional[int] = None
        current_region_lines: List[str] = []
        current_effective_directive: Optional[GuardDirective] = None
        
        # Process each line
        for line_idx, line in enumerate(lines):
            line_num = line_idx + 1  # 1-based
            
            # Step 1: Check for new guard directive on this line (as a comment)
            if line_num in directive_map:
                directive = directive_map[line_num]
                
                # Calculate end line (guards apply starting from THIS line)
                start_line = line_num
                if directive.line_count is not None:
                    # Line-limited guard
                    end_line = start_line + directive.line_count - 1
                else:
                    # Unbounded guard - extends to EOF or next guard
                    end_line = None
                
                guard_stack.append(GuardStackEntry(
                    directive, start_line, end_line, None
                ))
            
            # Step 2: Remove expired guards
            guard_stack = [
                entry for entry in guard_stack
                if entry.end_line is None or line_num <= entry.end_line
            ]
            
            # Step 3: Determine effective directive for this line
            effective_directive = None
            if guard_stack:
                # Get the top of stack (most recent guard)
                top_entry = guard_stack[-1]
                if line_num >= top_entry.start_line:
                    effective_directive = top_entry.directive
            
            # Step 4: Build or extend regions
            if effective_directive != current_effective_directive:
                # Permission changed - close current region if any
                if current_region_start is not None and current_region_lines:
                    regions.append(GuardedRegion(
                        start_line=current_region_start,
                        end_line=line_num - 1,
                        content="\n".join(current_region_lines),
                        directives=[current_effective_directive],
                    ))
                
                # Start new region if we have a directive
                if effective_directive:
                    current_region_start = line_num
                    current_region_lines = [line]
                    current_effective_directive = effective_directive
                else:
                    current_region_start = None
                    current_region_lines = []
                    current_effective_directive = None
            else:
                # Same permission - extend current region
                if current_region_start is not None:
                    current_region_lines.append(line)
        
        # Close final region if any
        if current_region_start is not None and current_region_lines:
            regions.append(GuardedRegion(
                start_line=current_region_start,
                end_line=len(lines),
                content="\n".join(current_region_lines),
                directives=[current_effective_directive],
            ))
        
        return regions
