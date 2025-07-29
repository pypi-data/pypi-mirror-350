"""
Language-specific parser integration with tree-sitter.

This module handles language-specific parsing using tree-sitter, extracting
comments and determining region boundaries across different programming languages.
"""

import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

import tree_sitter_c_sharp
import tree_sitter_cpp
import tree_sitter_css
import tree_sitter_go
import tree_sitter_html
import tree_sitter_java
import tree_sitter_javascript
import tree_sitter_php

# Import all tree-sitter language modules
import tree_sitter_python
import tree_sitter_ruby
import tree_sitter_rust
import tree_sitter_typescript

# Import tree-sitter for language-aware parsing
from tree_sitter import Language, Node, Parser


class LanguageType(Enum):
    """Supported programming languages."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    PHP = "php"
    HTML = "html"
    CSS = "css"
    UNKNOWN = "unknown"


class CommentStyle:
    """Represents comment styles for a language."""

    def __init__(
        self,
        line_comment: str,
        block_comment_start: Optional[str] = None,
        block_comment_end: Optional[str] = None,
        has_region_markers: bool = False,
        region_start: Optional[str] = None,
        region_end: Optional[str] = None,
    ):
        self.line_comment = line_comment
        self.block_comment_start = block_comment_start
        self.block_comment_end = block_comment_end
        self.has_region_markers = has_region_markers
        self.region_start = region_start
        self.region_end = region_end


# Define comment styles for supported languages
COMMENT_STYLES = {
    LanguageType.PYTHON: CommentStyle(
        line_comment="#",
        block_comment_start='"""',
        block_comment_end='"""',
        has_region_markers=True,
        region_start="# region",
        region_end="# endregion",
    ),
    LanguageType.JAVASCRIPT: CommentStyle(
        line_comment="//",
        block_comment_start="/*",
        block_comment_end="*/",
        has_region_markers=True,
        region_start="//region",
        region_end="//endregion",
    ),
    LanguageType.TYPESCRIPT: CommentStyle(
        line_comment="//",
        block_comment_start="/*",
        block_comment_end="*/",
        has_region_markers=True,
        region_start="//region",
        region_end="//endregion",
    ),
    LanguageType.JAVA: CommentStyle(
        line_comment="//",
        block_comment_start="/*",
        block_comment_end="*/",
        has_region_markers=True,
        region_start="//region",
        region_end="//endregion",
    ),
    LanguageType.CSHARP: CommentStyle(
        line_comment="//",
        block_comment_start="/*",
        block_comment_end="*/",
        has_region_markers=True,
        region_start="#region",
        region_end="#endregion",
    ),
    LanguageType.CPP: CommentStyle(
        line_comment="//",
        block_comment_start="/*",
        block_comment_end="*/",
        has_region_markers=True,
        region_start="#pragma region",
        region_end="#pragma endregion",
    ),
    LanguageType.GO: CommentStyle(
        line_comment="//", block_comment_start="/*", block_comment_end="*/"
    ),
    LanguageType.RUST: CommentStyle(
        line_comment="//", block_comment_start="/*", block_comment_end="*/"
    ),
    LanguageType.RUBY: CommentStyle(
        line_comment="#", block_comment_start="=begin", block_comment_end="=end"
    ),
    LanguageType.PHP: CommentStyle(
        line_comment="//", block_comment_start="/*", block_comment_end="*/"
    ),
    LanguageType.HTML: CommentStyle(
        line_comment=None, block_comment_start="<!--", block_comment_end="-->"
    ),
    LanguageType.CSS: CommentStyle(
        line_comment=None, block_comment_start="/*", block_comment_end="*/"
    ),
    LanguageType.UNKNOWN: CommentStyle(
        line_comment="#", block_comment_start=None, block_comment_end=None
    ),
}


class Comment:
    """Represents a comment in source code."""

    def __init__(self, text: str, start_line: int, end_line: int, is_block_comment: bool = False):
        self.text = text
        self.start_line = start_line
        self.end_line = end_line
        self.is_block_comment = is_block_comment


class Region:
    """Represents a region in source code."""

    def __init__(self, name: str, start_line: int, end_line: int, content: str):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.content = content


class SemanticScope:
    """Represents a semantic scope in source code."""

    def __init__(
        self,
        scope_type: str,
        start_line: int,
        end_line: int,
        content: str,
        name: Optional[str] = None,
        definition_lines: Optional[Tuple[int, int]] = None,
        body_lines: Optional[Tuple[int, int]] = None,
        docstring_lines: Optional[Tuple[int, int]] = None,
    ):
        self.scope_type = scope_type  # function, class, method, block, etc.
        self.start_line = start_line
        self.end_line = end_line
        self.content = content
        self.name = name  # Function/class/method name if applicable
        self.definition_lines = definition_lines  # (start, end) for signature
        self.body_lines = body_lines  # (start, end) for body
        self.docstring_lines = docstring_lines  # (start, end) for docstring


class TreeSitterManager:
    """
    Manager for loading and initializing tree-sitter parsers.

    This class manages the loading of tree-sitter language libraries and
    initializing parsers for different languages.
    """

    def __init__(self):
        """Initialize the tree-sitter manager."""
        self.languages = {}
        self.parsers = {}
        self.language_queries = {}
        self.scope_queries = {}

        # Initialize tree-sitter languages using the new API
        self._initialize_languages()

    def _initialize_languages(self):
        """Initialize tree-sitter languages using the 0.24.0 API."""
        # Track missing languages for better error reporting
        self.missing_languages = []

        # Import language modules and create Language objects
        language_modules = {
            LanguageType.PYTHON: ("tree_sitter_python", tree_sitter_python),
            LanguageType.JAVASCRIPT: ("tree_sitter_javascript", tree_sitter_javascript),
            LanguageType.TYPESCRIPT: ("tree_sitter_typescript", tree_sitter_typescript),
            LanguageType.JAVA: ("tree_sitter_java", tree_sitter_java),
            LanguageType.CSHARP: ("tree_sitter_c_sharp", tree_sitter_c_sharp),
            LanguageType.CPP: ("tree_sitter_cpp", tree_sitter_cpp),
            LanguageType.GO: ("tree_sitter_go", tree_sitter_go),
            LanguageType.RUST: ("tree_sitter_rust", tree_sitter_rust),
            LanguageType.RUBY: ("tree_sitter_ruby", tree_sitter_ruby),
            LanguageType.PHP: ("tree_sitter_php", tree_sitter_php),
            LanguageType.HTML: ("tree_sitter_html", tree_sitter_html),
            LanguageType.CSS: ("tree_sitter_css", tree_sitter_css),
        }

        # Initialize each language
        for lang_type, (module_name, module) in language_modules.items():
            try:
                # Get the language function from the module
                if lang_type == LanguageType.TYPESCRIPT:
                    # TypeScript has a special case
                    language_obj = module.language_typescript()
                elif lang_type == LanguageType.PHP:
                    # PHP also has a special case
                    language_obj = module.language_php()
                else:
                    # Standard case
                    language_obj = module.language()

                # Create Language wrapper and parser
                try:
                    language = Language(language_obj)
                    parser = Parser(language)
                except Exception as e:
                    logging.error(f"Failed to create parser for {lang_type.value}: {e}")
                    raise

                self.languages[lang_type] = language
                self.parsers[lang_type] = parser

                # Create queries for this language
                self._create_comment_query_for_language(lang_type, language)
                self._create_scope_queries_for_language(lang_type, language)
            except (AttributeError, ImportError) as e:
                # Language module not installed or has wrong API
                self.missing_languages.append((lang_type, module_name))
                logging.warning(
                    f"Tree-sitter language module not available for {lang_type.value}: {module_name}"
                )
            except Exception as e:
                logging.error(f"Failed to initialize {lang_type.value}: {e}")

    def _create_scope_queries_for_language(self, lang_type: LanguageType, language):
        """Create queries for semantic scopes in the given language."""
        # Scope queries for different languages
        scope_queries = {
            LanguageType.PYTHON: """
                (function_definition name: (identifier) @func_name) @function
                (class_definition name: (identifier) @class_name) @class
                (if_statement) @if_block
                (for_statement) @for_block
                (while_statement) @while_block
                (with_statement) @with_block
                (try_statement) @try_block
                (decorated_definition) @decorated
                (import_statement) @import
                (import_from_statement) @import
            """,
            LanguageType.JAVASCRIPT: """
                (function_declaration name: (identifier) @func_name) @function
                (class_declaration name: (identifier) @class_name) @class
                (method_definition name: (property_identifier) @method_name) @method
                (arrow_function) @arrow_function
                (if_statement) @if_block
                (for_statement) @for_block
                (while_statement) @while_block
                (statement_block) @block
                (import_statement) @import
            """,
            LanguageType.TYPESCRIPT: """
                (function_declaration name: (identifier) @func_name) @function
                (class_declaration (type_identifier) @class_name) @class
                (method_definition name: (property_identifier) @method_name) @method
                (arrow_function) @arrow_function
                (if_statement) @if_block
                (for_statement) @for_block
                (while_statement) @while_block
                (statement_block) @block
                (import_statement) @import
            """,
            LanguageType.JAVA: """
                (method_declaration name: (identifier) @method_name) @method
                (class_declaration name: (identifier) @class_name) @class
                (interface_declaration name: (identifier) @interface_name) @interface
                (if_statement) @if_block
                (for_statement) @for_block
                (while_statement) @while_block
                (block) @block
                (import_declaration) @import
            """,
            LanguageType.CSHARP: """
                (method_declaration name: (identifier) @method_name) @method
                (local_function_statement name: (identifier) @func_name) @function
                (class_declaration name: (identifier) @class_name) @class
                (property_declaration name: (identifier) @property_name) @property
                (if_statement) @if_block
                (for_statement) @for_block
                (while_statement) @while_block
                (block) @block
                (using_directive) @import
            """,
        }

        if lang_type in scope_queries:
            try:
                # Try to create query - handle both Language wrapper and raw language objects
                if hasattr(language, 'query'):
                    query = language.query(scope_queries[lang_type])
                else:
                    # For raw language objects, try using tree_sitter.Query
                    from tree_sitter import Query
                    query = Query(language, scope_queries[lang_type])
                self.scope_queries[lang_type] = query
            except Exception as e:
                # If the query fails, log and continue
                logging.warning(f"Failed to create scope query for {lang_type}: {e}")
                pass

    def _create_comment_query_for_language(self, lang_type: LanguageType, language):
        """Create a query for comments in the given language."""
        # Default comment queries for different languages
        comment_queries = {
            LanguageType.PYTHON: """
                (comment) @line_comment
                (string) @docstring
            """,
            LanguageType.JAVASCRIPT: """
                (comment) @comment
            """,
            LanguageType.TYPESCRIPT: """
                (comment) @comment
            """,
            LanguageType.JAVA: """
                (line_comment) @line_comment
                (block_comment) @block_comment
            """,
            LanguageType.CSHARP: """
                (comment) @comment
            """,
            LanguageType.CPP: """
                (comment) @comment
            """,
            LanguageType.GO: """
                (comment) @comment
            """,
            LanguageType.RUST: """
                (line_comment) @line_comment
                (block_comment) @block_comment
            """,
            LanguageType.RUBY: """
                (comment) @comment
            """,
            LanguageType.PHP: """
                (comment) @comment
            """,
            LanguageType.HTML: """
                (comment) @comment
            """,
            LanguageType.CSS: """
                (comment) @comment
            """,
        }

        if lang_type in comment_queries:
            try:
                # Try to create query - handle both Language wrapper and raw language objects
                if hasattr(language, 'query'):
                    query = language.query(comment_queries[lang_type])
                else:
                    # For raw language objects, try using tree_sitter.Query
                    from tree_sitter import Query
                    query = Query(language, comment_queries[lang_type])
                self.language_queries[lang_type] = query
            except Exception as e:
                # If the query fails, log and continue - we'll use regex parsing instead
                logging.debug(f"Failed to create comment query for {lang_type}: {e}")
                pass

    def get_parser(self, language_type: LanguageType) -> Optional[Parser]:
        """
        Get a parser for the specified language.

        Args:
            language_type: Language to get parser for

        Returns:
            Parser instance if available, None otherwise
        """
        return self.parsers.get(language_type)

    def has_parser(self, language_type: LanguageType) -> bool:
        """
        Check if a parser is available for the specified language.

        Args:
            language_type: Language to check

        Returns:
            True if parser is available, False otherwise
        """
        return language_type in self.parsers

    def get_query(self, language_type: LanguageType) -> Optional[Any]:
        """
        Get the comment query for the specified language.

        Args:
            language_type: Language to get query for

        Returns:
            Query instance if available, None otherwise
        """
        return self.language_queries.get(language_type)

    def get_language(self, language_type: LanguageType) -> Optional[Language]:
        """
        Get the language instance for the specified language type.

        Args:
            language_type: Language to get

        Returns:
            Language instance if available, None otherwise
        """
        return self.languages.get(language_type)

    def get_scope_query(self, language_type: LanguageType) -> Optional[Any]:
        """
        Get the scope query for the specified language.

        Args:
            language_type: Language to get scope query for

        Returns:
            Query instance if available, None otherwise
        """
        return self.scope_queries.get(language_type)


class LanguageParser:
    """
    Parser for extracting comments and regions from source code.

    This class integrates with tree-sitter to provide language-aware parsing
    capabilities.
    """

    def __init__(self):
        """Initialize the language parser."""
        self.ts_manager = TreeSitterManager()
        self._warned_languages = set()  # Track which languages we've warned about

    def detect_language(self, file_path: Union[str, Path]) -> LanguageType:
        """
        Detect the programming language from a file path.

        Args:
            file_path: Path to the file

        Returns:
            Detected language type
        """
        ext = os.path.splitext(str(file_path))[1].lower()

        # Map file extensions to language types
        ext_map = {
            ".py": LanguageType.PYTHON,
            ".js": LanguageType.JAVASCRIPT,
            ".jsx": LanguageType.JAVASCRIPT,
            ".ts": LanguageType.TYPESCRIPT,
            ".tsx": LanguageType.TYPESCRIPT,
            ".java": LanguageType.JAVA,
            ".cs": LanguageType.CSHARP,
            ".cpp": LanguageType.CPP,
            ".cc": LanguageType.CPP,
            ".c": LanguageType.CPP,
            ".h": LanguageType.CPP,
            ".hpp": LanguageType.CPP,
            ".go": LanguageType.GO,
            ".rs": LanguageType.RUST,
            ".rb": LanguageType.RUBY,
            ".php": LanguageType.PHP,
            ".html": LanguageType.HTML,
            ".htm": LanguageType.HTML,
            ".css": LanguageType.CSS,
        }

        return ext_map.get(ext, LanguageType.UNKNOWN)

    def extract_comments(self, source_code: str, language: LanguageType) -> List[Comment]:
        """
        Extract comments from source code.

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            List of extracted comments
        """
        # Try to use tree-sitter parser first
        if self.ts_manager and self.ts_manager.has_parser(language):
            try:
                return self._extract_comments_tree_sitter(source_code, language)
            except Exception as e:
                # Log the error and fall back to regex
                logging.warning(f"Tree-sitter extraction failed for {language.value}: {e}")
                return self._extract_comments_regex(source_code, language)
        else:
            # Fall back to regex if no parser is available for this specific language
            return self._extract_comments_regex(source_code, language)

    def _extract_comments_tree_sitter(
        self, source_code: str, language: LanguageType
    ) -> List[Comment]:
        """
        Extract comments using tree-sitter parser.

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            List of extracted comments
        """
        comments = []

        # Get the parser for this language
        parser = self.ts_manager.get_parser(language)
        if not parser:
            return self._extract_comments_regex(source_code, language)

        # Special handling for PHP - inject <?php tags if missing (only in memory for parsing)
        original_source = source_code
        php_line_offset = 0
        if language == LanguageType.PHP and not source_code.strip().startswith("<?"):
            source_code = "<?php\n" + source_code + "\n?>"
            php_line_offset = 1  # We added one line at the beginning

        # Parse the source code - handle both API styles
        try:
            # Try the modern way first
            if hasattr(parser, "parse_string"):
                tree = parser.parse_string(bytes(source_code, "utf-8"))
            else:
                # Fall back to old way
                tree = parser.parse(bytes(source_code, "utf-8"))
        except Exception as e:
            import logging

            logging.warning(f"Failed to parse source code: {e}")
            return self._extract_comments_regex(original_source, language)

        # Get the pre-defined query for this language if available
        query = self.ts_manager.get_query(language)

        # If no pre-defined query exists, create a generic one
        if not query:
            query_str = "(comment) @comment"
            lang = self.ts_manager.get_language(language)
            if not lang:
                # No language object available, fall back to regex
                return self._extract_comments_regex(source_code, language)

            try:
                # Try different query creation methods
                if hasattr(lang, "query"):
                    query = lang.query(query_str)
                elif hasattr(lang, "create_query"):
                    query = lang.create_query(query_str)
                else:
                    # No query method available, fall back to regex
                    return self._extract_comments_regex(source_code, language)
            except Exception:
                # If creating a query fails, fall back to regex
                return self._extract_comments_regex(source_code, language)

        try:
            # Execute the query to find comments
            captures = query.captures(tree.root_node)
            source_lines = source_code.splitlines()

            # Handle both old and new API styles
            if isinstance(captures, dict):
                # New API (0.22.0+) - captures is a dict
                for tag, nodes in captures.items():
                    for node in nodes:
                        # Extract comment text and position
                        start_point = node.start_point
                        end_point = node.end_point

                        start_line = (
                            start_point[0] + 1 - php_line_offset
                        )  # Convert to 1-based line numbers and adjust for PHP
                        end_line = end_point[0] + 1 - php_line_offset

                        # Get the raw content from the source code
                        start_byte = node.start_byte
                        end_byte = node.end_byte
                        node_text = source_code[start_byte:end_byte]

                        # Determine if it's a block comment based on tag or content
                        is_block_comment = False

                        # Detect block comments based on tag
                        if tag in ("block_comment", "docstring"):
                            is_block_comment = True

                        # Detect block comments based on content for different languages
                        elif language in (
                            LanguageType.JAVASCRIPT,
                            LanguageType.TYPESCRIPT,
                            LanguageType.JAVA,
                            LanguageType.CSHARP,
                            LanguageType.CPP,
                            LanguageType.CSS,
                        ):
                            is_block_comment = "/*" in node_text and "*/" in node_text

                        elif language == LanguageType.PYTHON:
                            # Python docstrings or block comments
                            is_block_comment = (
                                node_text.startswith('"""') and node_text.endswith('"""')
                            ) or (node_text.startswith("'''") and node_text.endswith("'''"))

                        elif language == LanguageType.HTML:
                            is_block_comment = "<!--" in node_text and "-->" in node_text

                        elif language == LanguageType.RUBY:
                            is_block_comment = "=begin" in node_text and "=end" in node_text

                        # Create the comment object
                        comments.append(
                            Comment(
                                text=node_text,
                                start_line=start_line,
                                end_line=end_line,
                                is_block_comment=is_block_comment,
                            )
                        )
            else:
                # Old API - captures is a list of tuples
                for node, tag in captures:
                    # Extract comment text and position
                    start_point = node.start_point
                    end_point = node.end_point

                    start_line = (
                        start_point[0] + 1 - php_line_offset
                    )  # Convert to 1-based line numbers and adjust for PHP
                    end_line = end_point[0] + 1 - php_line_offset

                    # Get the raw content from the source code
                    start_byte = node.start_byte
                    end_byte = node.end_byte
                    node_text = source_code[start_byte:end_byte]

                    # Determine if it's a block comment based on tag or content
                    is_block_comment = False

                    # Detect block comments based on tag
                    if tag in ("block_comment", "docstring"):
                        is_block_comment = True

                    # Detect block comments based on content for different languages
                    elif language in (
                        LanguageType.JAVASCRIPT,
                        LanguageType.TYPESCRIPT,
                        LanguageType.JAVA,
                        LanguageType.CSHARP,
                        LanguageType.CPP,
                        LanguageType.CSS,
                    ):
                        is_block_comment = "/*" in node_text and "*/" in node_text

                    elif language == LanguageType.PYTHON:
                        # Python docstrings or block comments
                        is_block_comment = (
                            node_text.startswith('"""') and node_text.endswith('"""')
                        ) or (node_text.startswith("'''") and node_text.endswith("'''"))

                    elif language == LanguageType.HTML:
                        is_block_comment = "<!--" in node_text and "-->" in node_text

                    elif language == LanguageType.RUBY:
                        is_block_comment = "=begin" in node_text and "=end" in node_text

                    # Create the comment object
                    comments.append(
                        Comment(
                            text=node_text,
                            start_line=start_line,
                            end_line=end_line,
                            is_block_comment=is_block_comment,
                        )
                    )

            # Sort comments by line number
            comments.sort(key=lambda c: c.start_line)
            return comments

        except Exception as e:
            # Log the error and fall back to regex-based extraction
            import logging

            logging.warning(f"Tree-sitter comment extraction failed: {e}")
            return self._extract_comments_regex(source_code, language)

    def _extract_comments_regex(self, source_code: str, language: LanguageType) -> List[Comment]:
        """
        Extract comments using regular expressions (fallback method).

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            List of extracted comments
        """
        comments = []
        style = COMMENT_STYLES.get(language, COMMENT_STYLES[LanguageType.UNKNOWN])
        lines = source_code.splitlines()

        # Process line comments
        if style.line_comment:
            i = 0
            while i < len(lines):
                line = lines[i]
                line_number = i + 1

                if line.strip().startswith(style.line_comment):
                    # Found a line comment
                    # Check for consecutive line comments (treat as a block)
                    start_line = line_number
                    end_line = line_number
                    comment_lines = [line]

                    # Check next lines
                    j = i + 1
                    while j < len(lines) and lines[j].strip().startswith(style.line_comment):
                        comment_lines.append(lines[j])
                        end_line = j + 1
                        j += 1

                    # Create comment object
                    text = "\n".join(comment_lines)
                    is_block = (end_line - start_line) > 0  # Multiple lines make a block

                    comments.append(
                        Comment(
                            text=text,
                            start_line=start_line,
                            end_line=end_line,
                            is_block_comment=is_block,
                        )
                    )

                    i = j  # Skip processed lines
                else:
                    i += 1

        # Process block comments
        if style.block_comment_start and style.block_comment_end:
            i = 0
            while i < len(lines):
                line = lines[i]
                line_number = i + 1

                if style.block_comment_start in line:
                    # Found a block comment start
                    start_idx = line.find(style.block_comment_start)
                    start_line = line_number

                    # Check if block end is on the same line
                    if (
                        style.block_comment_end
                        in line[start_idx + len(style.block_comment_start) :]
                    ):
                        # Single-line block comment
                        comments.append(
                            Comment(
                                text=line,
                                start_line=start_line,
                                end_line=start_line,
                                is_block_comment=True,
                            )
                        )
                        i += 1
                        continue

                    # Multi-line block comment
                    comment_lines = [line]
                    end_line = start_line
                    found_end = False

                    # Search for end marker
                    j = i + 1
                    while j < len(lines) and not found_end:
                        comment_lines.append(lines[j])
                        end_line = j + 1

                        if style.block_comment_end in lines[j]:
                            found_end = True

                        j += 1

                    # Create comment object
                    if found_end:
                        text = "\n".join(comment_lines)
                        comments.append(
                            Comment(
                                text=text,
                                start_line=start_line,
                                end_line=end_line,
                                is_block_comment=True,
                            )
                        )

                        i = j  # Skip processed lines
                    else:
                        # No end marker found, treat as a single-line comment
                        comments.append(
                            Comment(
                                text=line,
                                start_line=start_line,
                                end_line=start_line,
                                is_block_comment=False,
                            )
                        )
                        i += 1
                else:
                    i += 1

        return comments

    def extract_regions(self, source_code: str, language: LanguageType) -> List[Region]:
        """
        Extract regions from source code.

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            List of extracted regions
        """
        # First, extract all comments using tree-sitter
        comments = self.extract_comments(source_code, language)

        # Get region markers for this language
        style = COMMENT_STYLES.get(language, COMMENT_STYLES[LanguageType.UNKNOWN])

        # If language doesn't support regions, return empty list
        if not style.has_region_markers:
            return []

        # Process region markers in comments
        regions = []
        region_stack = []
        lines = source_code.splitlines()

        # Extract region markers from comments
        for comment in comments:
            comment_text = comment.text.strip()

            # Check for region start marker
            if style.region_start and style.region_start in comment_text:
                # Extract region name
                name_part = comment_text.split(style.region_start, 1)[1].strip()
                name = name_part.split("\n")[0].strip() if "\n" in name_part else name_part

                # Store region start info
                region_stack.append((name, comment.start_line, comment.end_line))

            # Check for region end marker
            elif style.region_end and style.region_end in comment_text and region_stack:
                # Pop the most recent region start
                name, start_marker_line, start_content_line = region_stack.pop()

                # Calculate region content (from after start marker to before end marker)
                start_idx = start_content_line  # Line after the comment with region start
                end_idx = comment.start_line - 1  # Line before the comment with region end

                # Extract the content
                region_lines = lines[start_idx:end_idx]
                content = "\n".join(region_lines)

                # Create region object
                regions.append(
                    Region(
                        name=name, start_line=start_content_line, end_line=end_idx, content=content
                    )
                )

        # Handle special case for C# preprocessor regions
        if language == LanguageType.CSHARP:
            self._extract_csharp_preprocessor_regions(source_code, regions)

        # Sort regions by start line
        regions.sort(key=lambda r: r.start_line)
        return regions

    def _extract_csharp_preprocessor_regions(self, source_code: str, regions: List[Region]):
        """
        Extract preprocessor regions from C# code.

        These are special because they're not comments but preprocessor directives.

        Args:
            source_code: Source code content
            regions: List to append extracted regions to
        """
        lines = source_code.splitlines()
        region_stack = []

        for i, line in enumerate(lines):
            line_number = i + 1
            line_stripped = line.strip()

            # Check for preprocessor region start
            if line_stripped.startswith("#region"):
                name = line_stripped[7:].strip()  # Extract name after #region
                region_stack.append((name, line_number))

            # Check for preprocessor region end
            elif line_stripped.startswith("#endregion") and region_stack:
                name, start_line = region_stack.pop()

                # Extract region content
                content_start = start_line  # Line after the #region
                content_end = line_number - 1  # Line before the #endregion
                content = "\n".join(lines[content_start:content_end])

                # Add region
                regions.append(
                    Region(
                        name=name,
                        start_line=content_start + 1,  # Start after the region marker
                        end_line=content_end,  # End before the endregion marker
                        content=content,
                    )
                )

    def extract_semantic_scopes(
        self, source_code: str, language: LanguageType
    ) -> List[SemanticScope]:
        """
        Extract semantic scopes from source code using tree-sitter.

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            List of semantic scopes found in the source code
        """
        # Try to use tree-sitter parser first
        if self.ts_manager and self.ts_manager.has_parser(language):
            return self._extract_scopes_tree_sitter(source_code, language)
        else:
            # Fall back to heuristic-based extraction
            return self._extract_scopes_heuristic(source_code, language)

    def _extract_scopes_tree_sitter(
        self, source_code: str, language: LanguageType
    ) -> List[SemanticScope]:
        """
        Extract semantic scopes using tree-sitter parser.

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            List of extracted semantic scopes
        """
        scopes = []

        # Get the parser for this language
        parser = self.ts_manager.get_parser(language)
        if not parser:
            return self._extract_scopes_heuristic(source_code, language)

        # Parse the source code
        try:
            if hasattr(parser, "parse_string"):
                tree = parser.parse_string(bytes(source_code, "utf-8"))
            else:
                tree = parser.parse(bytes(source_code, "utf-8"))
        except Exception:
            return self._extract_scopes_heuristic(source_code, language)

        # Get the scope query for this language
        query = self.ts_manager.get_scope_query(language)
        if not query:
            return self._extract_scopes_heuristic(source_code, language)

        try:
            # Execute the query to find scopes
            captures_dict = query.captures(tree.root_node)
            source_lines = source_code.splitlines()

            # Process captures to create semantic scopes
            for tag, nodes in captures_dict.items():
                for node in nodes:
                    start_line = node.start_point[0] + 1
                    end_line = node.end_point[0] + 1

                    # Extract content
                    start_byte = node.start_byte
                    end_byte = node.end_byte
                    content = source_code[start_byte:end_byte]

                    # Determine scope type from tag
                    scope_type = self._map_tag_to_scope_type(tag)

                    # Extract name if applicable
                    name = None
                    if tag.endswith("_name"):
                        name = node.text.decode("utf-8")
                    elif scope_type in ["function", "method", "class"]:
                        # Try to find the name child node
                        for child in node.children:
                            if child.type in [
                                "identifier",
                                "property_identifier",
                                "type_identifier",
                            ]:
                                name = child.text.decode("utf-8")
                                break

                    # For functions/methods/classes, extract definition and body
                    definition_lines = None
                    body_lines = None
                    docstring_lines = None

                    if scope_type in ["function", "method", "class"]:
                        # Extract definition and body parts
                        definition_lines, body_lines, docstring_lines = self._extract_scope_parts(
                            node, source_code, language
                        )

                    # Create semantic scope
                    scope = SemanticScope(
                        scope_type=scope_type,
                        start_line=start_line,
                        end_line=end_line,
                        content=content,
                        name=name,
                        definition_lines=definition_lines,
                        body_lines=body_lines,
                        docstring_lines=docstring_lines,
                    )
                    scopes.append(scope)

            return scopes

        except Exception:
            return self._extract_scopes_heuristic(source_code, language)

    def _map_tag_to_scope_type(self, tag: str) -> str:
        """Map tree-sitter tag to semantic scope type."""
        tag_map = {
            "function": "function",
            "method": "method",
            "class": "class",
            "if_block": "block",
            "for_block": "block",
            "while_block": "block",
            "with_block": "block",
            "try_block": "block",
            "block": "block",
            "import": "import",
            "decorated": "decorator",
            "arrow_function": "function",
            "interface": "class",
            "property": "value",
        }
        return tag_map.get(tag, "statement")

    def _extract_scope_parts(
        self, node: Node, source_code: str, language: LanguageType
    ) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        Extract signature, body, and docstring parts of a scope.

        Returns:
            Tuple of (definition_lines, body_lines, docstring_lines)
        """
        definition_lines = None
        body_lines = None
        docstring_lines = None

        # Language-specific extraction logic
        if language == LanguageType.PYTHON:
            # Find the colon that ends the definition
            for child in node.children:
                if child.type == "parameters":
                    # Signature ends after parameters
                    definition_lines = (node.start_point[0] + 1, child.end_point[0] + 1)
                elif child.type == "block":
                    # Body is the block
                    body_lines = (child.start_point[0] + 1, child.end_point[0] + 1)
                    # Check for docstring as first statement
                    if child.children and child.children[0].type == "expression_statement":
                        expr = child.children[0]
                        if expr.children and expr.children[0].type == "string":
                            docstring_lines = (expr.start_point[0] + 1, expr.end_point[0] + 1)

        elif language in [LanguageType.JAVASCRIPT, LanguageType.TYPESCRIPT]:
            # Find parameter list and body
            for child in node.children:
                if child.type == "formal_parameters":
                    definition_lines = (node.start_point[0] + 1, child.end_point[0] + 1)
                elif child.type == "statement_block":
                    body_lines = (child.start_point[0] + 1, child.end_point[0] + 1)

        return definition_lines, body_lines, docstring_lines

    def _extract_scopes_heuristic(
        self, source_code: str, language: LanguageType
    ) -> List[SemanticScope]:
        """
        Extract semantic scopes using heuristic methods (fallback).

        Args:
            source_code: Source code content
            language: Programming language

        Returns:
            List of extracted semantic scopes
        """
        scopes = []
        lines = source_code.splitlines()

        # Language-specific patterns
        if language == LanguageType.PYTHON:
            # Pattern for Python functions and classes
            import re

            func_pattern = re.compile(r"^(\s*)def\s+(\w+)\s*\(")
            class_pattern = re.compile(r"^(\s*)class\s+(\w+)")

            for i, line in enumerate(lines):
                # Check for function
                func_match = func_pattern.match(line)
                if func_match:
                    indent = len(func_match.group(1))
                    name = func_match.group(2)
                    start_line = i + 1

                    # Find end of function
                    end_line = self._find_scope_end_by_indent(lines, i, indent)

                    # Extract content
                    content = "\n".join(lines[i:end_line])

                    scopes.append(
                        SemanticScope(
                            scope_type="function",
                            start_line=start_line,
                            end_line=end_line + 1,
                            content=content,
                            name=name,
                        )
                    )

                # Check for class
                class_match = class_pattern.match(line)
                if class_match:
                    indent = len(class_match.group(1))
                    name = class_match.group(2)
                    start_line = i + 1

                    # Find end of class
                    end_line = self._find_scope_end_by_indent(lines, i, indent)

                    # Extract content
                    content = "\n".join(lines[i:end_line])

                    scopes.append(
                        SemanticScope(
                            scope_type="class",
                            start_line=start_line,
                            end_line=end_line + 1,
                            content=content,
                            name=name,
                        )
                    )

        return scopes

    def _find_scope_end_by_indent(self, lines: List[str], start_idx: int, base_indent: int) -> int:
        """Find the end of a scope based on indentation."""
        end_idx = start_idx

        for i in range(start_idx + 1, len(lines)):
            line = lines[i]
            if not line.strip():  # Skip empty lines
                continue

            # Calculate indentation
            indent = len(line) - len(line.lstrip())

            # If indentation is less than or equal to base, scope ended
            if indent <= base_indent:
                return i - 1

            end_idx = i

        return end_idx

    def parse_file(
        self, file_path: Union[str, Path]
    ) -> Tuple[LanguageType, List[Comment], List[Region]]:
        """
        Parse a file to extract language, comments, and regions.

        Args:
            file_path: Path to the file

        Returns:
            Tuple of (language, comments, regions)
        """
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        language = self.detect_language(file_path)

        # Check if parser is available for this language
        if language != LanguageType.UNKNOWN and not self.ts_manager.has_parser(language):
            # Check if this is a missing language we haven't warned about
            if language not in self._warned_languages:
                self._warned_languages.add(language)
                # Check if it's in the list of missing languages
                for lang_type, module_name in self.ts_manager.missing_languages:
                    if lang_type == language:
                        logging.info(
                            f"Note: Tree-sitter parser for {language.value} is not available. "
                            f"Install with: pip install {module_name}"
                        )
                        break

        comments = self.extract_comments(source_code, language)
        regions = self.extract_regions(source_code, language)

        return language, comments, regions
