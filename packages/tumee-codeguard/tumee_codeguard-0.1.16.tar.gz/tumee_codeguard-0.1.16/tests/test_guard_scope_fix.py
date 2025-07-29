"""
Test cases to verify that guards without explicit scope apply to semantic structures,
not to end-of-file.
"""

import pytest
from codeguard.parsers.guard_parser import GuardParser
from codeguard.parsers.language_parser import LanguageParser, LanguageType


def test_guard_applies_to_function_not_eof():
    """Test that a guard without scope applies to the next function only."""
    source_code = '''
# @guard:ai:r
def calculate_payment(amount: float, rate: float) -> float:
    """Calculate payment with interest."""
    return amount * (1 + rate)

# This function should NOT be protected
def another_function():
    pass
'''
    
    parser = GuardParser()
    lang_parser = LanguageParser()
    
    # Parse the code to get comments and semantic scopes
    comments = lang_parser.extract_comments(source_code, LanguageType.PYTHON)
    semantic_scopes = lang_parser.extract_semantic_scopes(source_code, LanguageType.PYTHON)
    
    # Extract guarded regions
    regions = parser.extract_guarded_regions(
        source_code, 
        LanguageType.PYTHON, 
        comments, 
        [], 
        semantic_scopes
    )
    
    # Should have exactly one guarded region
    assert len(regions) == 1
    
    # The region should cover only the first function
    region = regions[0]
    assert region.start_line == 3  # def calculate_payment...
    assert region.end_line == 5    # return amount * (1 + rate)
    assert "calculate_payment" in region.content
    assert "another_function" not in region.content


def test_guard_with_explicit_scope():
    """Test that guards with explicit scope still work correctly."""
    source_code = '''
# @guard:ai:r.sig
def process_data(data: dict) -> dict:
    """Process the data."""
    return transform(data)

# @guard:ai:n.body
def secure_function():
    # Only the body is protected
    secret = get_secret()
    process_secret(secret)
'''
    
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
    
    assert len(regions) == 2
    
    # First region should be signature only
    assert regions[0].start_line == 3
    assert regions[0].end_line == 3
    assert "def process_data" in regions[0].content
    assert "transform(data)" not in regions[0].content
    
    # Second region should be body only
    assert "secret = get_secret()" in regions[1].content
    assert "def secure_function" not in regions[1].content


def test_guard_with_line_count():
    """Test that guards with explicit line counts still work."""
    source_code = '''
# @guard:ai:r.3
config = {
    "api_key": "secret",
    "endpoint": "https://api.example.com"
}

# This should not be protected
other_config = {"public": "data"}
'''
    
    parser = GuardParser()
    lang_parser = LanguageParser()
    
    comments = lang_parser.extract_comments(source_code, LanguageType.PYTHON)
    
    regions = parser.extract_guarded_regions(
        source_code, 
        LanguageType.PYTHON, 
        comments, 
        [], 
        None  # No semantic scopes
    )
    
    assert len(regions) == 1
    assert regions[0].start_line == 2  # Includes guard comment line
    assert regions[0].end_line == 4  # 3 lines total
    assert "api_key" in regions[0].content
    assert "other_config" not in regions[0].content


def test_guard_without_semantic_scopes():
    """Test that guards without semantic scopes are handled correctly."""
    source_code = '''
# @guard:ai:r
some_code = "value"
more_code = "another"
'''
    
    parser = GuardParser()
    
    # Use simple extraction (no semantic parsing)
    regions = parser.extract_guarded_regions_simple(source_code)
    
    # Without semantic scopes, guard extends to EOF or next guard
    assert len(regions) == 1
    assert regions[0].start_line == 2  # Includes guard comment line
    assert regions[0].end_line == 4


def test_multiple_guards_on_class():
    """Test guards on class structures."""
    source_code = '''
# @guard:ai:r
class PaymentProcessor:
    """Handles payment processing."""
    
    def __init__(self):
        self.config = load_config()
    
    def process(self, amount):
        return self._calculate(amount)

# This class should not be protected
class Logger:
    def log(self, message):
        print(message)
'''
    
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
    
    assert len(regions) == 1
    assert "class PaymentProcessor" in regions[0].content
    assert "class Logger" not in regions[0].content