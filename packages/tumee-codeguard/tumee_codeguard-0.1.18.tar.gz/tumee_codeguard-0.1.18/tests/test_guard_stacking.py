"""
Test cases for guard region stacking behavior.

These tests verify that overlapping guards are handled correctly using
a stack-based approach where the most recent guard takes precedence.
"""

import pytest
from codeguard.parsers.guard_parser import GuardParser, GuardWho, GuardPermission
from codeguard.parsers.language_parser import LanguageParser, LanguageType


class TestGuardStacking:
    """Test cases for guard region stacking behavior."""

    def test_basic_guard_extension_to_eof(self):
        """Test that guards without scope extend to EOF."""
        source_code = '''# @guard:ai:r
line 1
line 2
line 3'''
        
        parser = GuardParser()
        regions = parser.extract_guarded_regions_simple(source_code)
        
        assert len(regions) == 1
        assert regions[0].start_line == 1
        assert regions[0].end_line == 4
        assert regions[0].directives[0].permission == GuardPermission.r
        assert "# @guard:ai:r\nline 1\nline 2\nline 3" in regions[0].content

    def test_guard_replacement(self):
        """Test that new guards supersede previous ones."""
        source_code = '''# @guard:ai:r
line 1
line 2
# @guard:ai:w
line 3
line 4'''
        
        parser = GuardParser()
        regions = parser.extract_guarded_regions_simple(source_code)
        
        assert len(regions) == 2
        # First region: ai:r
        assert regions[0].start_line == 1
        assert regions[0].end_line == 3
        assert regions[0].directives[0].permission == GuardPermission.r
        assert "# @guard:ai:r\nline 1\nline 2" in regions[0].content
        
        # Second region: ai:w
        assert regions[1].start_line == 4
        assert regions[1].end_line == 6
        assert regions[1].directives[0].permission == GuardPermission.w
        assert "# @guard:ai:w\nline 3\nline 4" in regions[1].content

    def test_line_limited_guard_expiration(self):
        """Test that line-limited guards expire and revert to previous state."""
        source_code = '''# @guard:ai:r
line 1
# @guard:ai:w.2
line 2
line 3
line 4
line 5'''
        
        parser = GuardParser()
        regions = parser.extract_guarded_regions_simple(source_code)
        
        assert len(regions) == 3
        
        # First region: ai:r (includes first guard and line 1)
        assert regions[0].start_line == 1
        assert regions[0].end_line == 2
        assert regions[0].directives[0].permission == GuardPermission.r
        
        # Second region: ai:w (limited to 2 lines starting from guard)
        assert regions[1].start_line == 3
        assert regions[1].end_line == 4  # @guard:ai:w.2 and line 2
        assert regions[1].directives[0].permission == GuardPermission.w
        
        # Third region: ai:r (reverted after w.2 expires)
        assert regions[2].start_line == 5
        assert regions[2].end_line == 7
        assert regions[2].directives[0].permission == GuardPermission.r

    def test_complex_stacking(self):
        """Test complex overlapping with multiple guards."""
        source_code = '''# @guard:ai:r
line 1
# @guard:human:n
line 2
# @guard:ai:w.1
line 3
line 4
# @guard:ai:n
line 5'''
        
        parser = GuardParser()
        regions = parser.extract_guarded_regions_simple(source_code)
        
        # Note: Simple parser only tracks one audience at a time
        # The most recent guard wins
        assert len(regions) == 5
        
        # Region 1: ai:r
        assert regions[0].directives[0].permission == GuardPermission.r
        assert regions[0].directives[0].who == GuardWho.ai
        
        # Region 2: human:n (replaces ai:r)
        assert regions[1].directives[0].permission == GuardPermission.n
        assert regions[1].directives[0].who == GuardWho.human
        
        # Region 3: ai:w.1 (replaces human:n)
        assert regions[2].directives[0].permission == GuardPermission.w
        assert regions[2].directives[0].who == GuardWho.ai
        
        # Region 4: human:n (reverts after ai:w.1 expires)
        assert regions[3].directives[0].permission == GuardPermission.n
        assert regions[3].directives[0].who == GuardWho.human
        
        # Region 5: ai:n (new guard)
        assert regions[4].directives[0].permission == GuardPermission.n
        assert regions[4].directives[0].who == GuardWho.ai

    def test_no_gaps_between_regions(self):
        """Test that there are no gaps between regions."""
        source_code = '''# @guard:ai:r
line 1
line 2
# @guard:ai:w
line 3
line 4'''
        
        parser = GuardParser()
        regions = parser.extract_guarded_regions_simple(source_code)
        
        # Verify continuous coverage
        assert regions[0].end_line + 1 == regions[1].start_line

    def test_semantic_scope_error_in_simple_parser(self):
        """Test that semantic scopes raise error in simple parser."""
        source_code = '''# @guard:ai:r.func
def my_function():
    pass'''
        
        parser = GuardParser()
        with pytest.raises(ValueError, match="Semantic scope guard.*requires language parsing"):
            parser.extract_guarded_regions_simple(source_code)

    def test_multiple_line_limited_guards(self):
        """Test multiple overlapping line-limited guards."""
        source_code = '''# @guard:ai:r
line 1
# @guard:ai:w.3
line 2
# @guard:ai:n.1
line 3
line 4
line 5'''
        
        parser = GuardParser()
        regions = parser.extract_guarded_regions_simple(source_code)
        
        # Region 1: ai:r (lines 1-2)
        assert regions[0].start_line == 1
        assert regions[0].end_line == 2
        
        # Region 2: ai:w.3 starts (lines 3-4 before ai:n.1 overrides)
        assert regions[1].start_line == 3
        assert regions[1].end_line == 4
        assert regions[1].directives[0].permission == GuardPermission.w
        
        # Region 3: ai:n.1 takes over (line 5 only)
        assert regions[2].start_line == 5
        assert regions[2].end_line == 5
        assert regions[2].directives[0].permission == GuardPermission.n
        
        # Region 4: ai:r resumes after both expire (lines 6-8)
        assert regions[3].start_line == 6
        assert regions[3].end_line == 8
        assert regions[3].directives[0].permission == GuardPermission.r

    def test_guard_with_semantic_scope_and_language_parser(self):
        """Test guards with semantic scopes using full language parser."""
        source_code = '''# @guard:ai:r
def protected_function():
    return 42

def unprotected_function():
    return 0'''
        
        parser = GuardParser()
        lang_parser = LanguageParser()
        
        comments = lang_parser.extract_comments(source_code, LanguageType.PYTHON)
        semantic_scopes = lang_parser.extract_semantic_scopes(source_code, LanguageType.PYTHON)
        
        regions = parser.extract_guarded_regions(
            source_code,
            LanguageType.PYTHON,
            comments,
            [],
            semantic_scopes
        )
        
        # Should protect only the first function
        assert len(regions) == 1
        assert "protected_function" in regions[0].content
        assert "unprotected_function" not in regions[0].content