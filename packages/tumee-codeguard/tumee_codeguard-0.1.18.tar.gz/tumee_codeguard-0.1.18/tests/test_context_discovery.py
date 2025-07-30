"""
Tests for context file discovery and management.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple

from codeguard.core.directory_guard import DirectoryGuard
from codeguard.parsers.guard_parser import GuardWho, GuardPermission


class TestContextDiscovery:
    """Test context file discovery and management functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def create_context_file(self, directory: Path, filename: str, content: str) -> Path:
        """Create a context file in the given directory."""
        file_path = directory / filename
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    
    def test_basic_context_file_discovery(self, temp_dir):
        """Test basic context file discovery."""
        # Create .ai-attributes to define context files
        attrs_content = """
CLAUDE.md @guard:ai:context
ai_context.md @guard:ai:context
"""
        attrs_file = temp_dir / ".ai-attributes"
        with open(attrs_file, "w") as f:
            f.write(attrs_content)
        
        # Create context files
        self.create_context_file(temp_dir, "CLAUDE.md", "# Claude Context")
        self.create_context_file(temp_dir, "ai_context.md", "# AI Context")
        
        # Create a regular file
        self.create_context_file(temp_dir, "README.md", "# Regular README")
        
        guard = DirectoryGuard(temp_dir)
        
        # Check if files are identified as context files
        assert guard.is_context_file(temp_dir / "CLAUDE.md")[0]
        assert guard.is_context_file(temp_dir / "ai_context.md")[0]
        assert not guard.is_context_file(temp_dir / "README.md")[0]
    
    def test_context_file_with_metadata(self, temp_dir):
        """Test context file discovery with metadata extraction."""
        # Create .ai-attributes with context metadata
        attrs_content = """
# Context file definitions
CLAUDE.md @guard:ai:context[priority=high,scope=project]
docs/*.md @guard:ai:context[scope=module]
"""
        attrs_file = temp_dir / ".ai-attributes"
        with open(attrs_file, "w") as f:
            f.write(attrs_content)
        
        # Create the context file
        self.create_context_file(temp_dir, "CLAUDE.md", "# Project Context")
        (temp_dir / "docs").mkdir(exist_ok=True)
        self.create_context_file(temp_dir / "docs", "api.md", "# API Docs")
        
        guard = DirectoryGuard(temp_dir)
        
        # Check CLAUDE.md
        is_context, metadata = guard.is_context_file(temp_dir / "CLAUDE.md")
        assert is_context
        assert metadata is not None
        assert metadata.get("priority") == "high"
        assert metadata.get("scope") == "project"
        
        # Check docs/api.md
        is_context, metadata = guard.is_context_file(temp_dir / "docs" / "api.md")
        assert is_context
        assert metadata is not None
        assert metadata.get("scope") == "module"
    
    def test_get_context_files(self, temp_dir):
        """Test getting all context files in a directory tree."""
        # Create .ai-attributes to define context files
        attrs_content = """
CLAUDE.md @guard:ai:context
src/ai_context.md @guard:ai:context
docs/CLAUDE.md @guard:ai:context
"""
        attrs_file = temp_dir / ".ai-attributes"
        with open(attrs_file, "w") as f:
            f.write(attrs_content)
        
        # Create directory structure
        (temp_dir / "src").mkdir()
        (temp_dir / "docs").mkdir()
        (temp_dir / "tests").mkdir()
        
        # Create various files
        self.create_context_file(temp_dir, "CLAUDE.md", "# Root Context")
        self.create_context_file(temp_dir, "README.md", "# Regular README")
        self.create_context_file(temp_dir / "src", "ai_context.md", "# Source Context")
        self.create_context_file(temp_dir / "docs", "CLAUDE.md", "# Docs Context")
        self.create_context_file(temp_dir / "tests", "test_file.py", "# Test File")
        
        guard = DirectoryGuard(temp_dir)
        
        # Get context files
        context_files = guard.get_context_files(temp_dir)
        
        # Should find 3 context files
        assert len(context_files) == 3
        
        # Check that all discovered files are context files
        context_paths = [Path(cf["path"]) for cf in context_files]
        assert temp_dir / "CLAUDE.md" in context_paths
        assert temp_dir / "src" / "ai_context.md" in context_paths
        assert temp_dir / "docs" / "CLAUDE.md" in context_paths
    
    def test_context_files_with_metadata_filtering(self, temp_dir):
        """Test getting context files filters them correctly by metadata."""
        # Create .ai-attributes with different metadata
        attrs_content = """
high_priority.md @guard:ai:context[priority=high]
module_context.md @guard:ai:context[scope=module]
claude_specific.md @guard:ai[claude-3,claude-4]:context
general_context.md @guard:ai:context
"""
        attrs_file = temp_dir / ".ai-attributes"
        with open(attrs_file, "w") as f:
            f.write(attrs_content)
        
        # Create the files
        for filename in ["high_priority.md", "module_context.md", "claude_specific.md", "general_context.md"]:
            self.create_context_file(temp_dir, filename, f"# {filename}")
        
        guard = DirectoryGuard(temp_dir)
        
        # Get all context files
        context_files = guard.get_context_files(temp_dir)
        
        # Should find all 4 context files
        assert len(context_files) == 4
        
        # Check metadata is preserved
        metadata_by_file = {Path(cf["path"]).name: cf["metadata"] for cf in context_files}
        
        assert metadata_by_file["high_priority.md"].get("priority") == "high"
        assert metadata_by_file["module_context.md"].get("scope") == "module"
        # General context should have empty metadata
        assert metadata_by_file["general_context.md"] == {}
    
    def test_non_recursive_context_file_search(self, temp_dir):
        """Test non-recursive context file search."""
        # Create nested structure
        (temp_dir / "src").mkdir()
        
        # Create context files at different levels
        self.create_context_file(temp_dir, "root_context.md", "# Root")
        self.create_context_file(temp_dir / "src", "src_context.md", "# Src")
        
        # Create .ai-attributes
        attrs_content = """
*.md @guard:ai:context
"""
        with open(temp_dir / ".ai-attributes", "w") as f:
            f.write(attrs_content)
        
        guard = DirectoryGuard(temp_dir)
        
        # Non-recursive search should only find root level
        context_files = guard.get_context_files(temp_dir, recursive=False)
        assert len(context_files) == 1
        assert Path(context_files[0]["path"]).name == "root_context.md"
        
        # Recursive search should find both
        context_files = guard.get_context_files(temp_dir, recursive=True)
        assert len(context_files) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])