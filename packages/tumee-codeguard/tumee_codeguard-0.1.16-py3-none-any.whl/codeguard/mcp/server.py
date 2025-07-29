"""
MCP Server for CodeGuard.

This module implements a Model-Controller-Presenter (MCP) server using FastAPI
for integration with IDEs and other tools.
"""

import os
import tempfile
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel, Field

from ..core.validator import CodeGuardValidator
from ..vcs.git_integration import GitError, GitIntegration


# Define API models
class ViolationResponse(BaseModel):
    """Response model for a violation."""

    model_config = {"extra": "forbid"}

    file: str
    line: int
    guard_type: str
    original_hash: str
    modified_hash: str
    message: str
    severity: str
    diff_summary: Optional[str] = None


class ValidationSummary(BaseModel):
    """Summary of validation results."""

    model_config = {"extra": "forbid"}

    files_checked: int
    violations_found: int
    critical_count: int
    warning_count: int
    info_count: int
    status: str


class ValidationResponse(BaseModel):
    """Response model for validation results."""

    model_config = {"extra": "forbid"}

    violations: List[ViolationResponse]
    summary: ValidationSummary


class ValidationRequest(BaseModel):
    """Request model for validation endpoint."""

    model_config = {"extra": "forbid"}

    original_content: str = Field(..., description="Original file content")
    modified_content: str = Field(..., description="Modified file content")
    file_path: str = Field(..., description="Path to the file")
    target: str = Field("AI", description="Target audience (AI, HU, ALL)")
    normalize_whitespace: bool = Field(True, description="Normalize whitespace in comparisons")
    normalize_line_endings: bool = Field(True, description="Normalize line endings in comparisons")
    ignore_blank_lines: bool = Field(True, description="Ignore blank lines in comparisons")
    ignore_indentation: bool = Field(False, description="Ignore indentation changes in comparisons")


class GitValidationRequest(BaseModel):
    """Request model for git validation endpoint."""

    model_config = {"extra": "forbid"}

    file_path: str = Field(..., description="Path to the file")
    modified_content: str = Field(..., description="Modified file content")
    revision: str = Field("HEAD", description="Git revision to compare against")
    repo_path: Optional[str] = Field(None, description="Path to git repository")
    target: str = Field("AI", description="Target audience (AI, HU, ALL)")
    normalize_whitespace: bool = Field(True, description="Normalize whitespace in comparisons")
    normalize_line_endings: bool = Field(True, description="Normalize line endings in comparisons")
    ignore_blank_lines: bool = Field(True, description="Ignore blank lines in comparisons")
    ignore_indentation: bool = Field(False, description="Ignore indentation changes in comparisons")


class RevisionCompareRequest(BaseModel):
    """Request model for revision comparison endpoint."""

    model_config = {"extra": "forbid"}

    file_path: str = Field(..., description="Path to the file")
    from_revision: str = Field(..., description="Base revision for comparison")
    to_revision: str = Field("HEAD", description="Target revision for comparison")
    repo_path: Optional[str] = Field(None, description="Path to git repository")
    target: str = Field("AI", description="Target audience (AI, HU, ALL)")
    normalize_whitespace: bool = Field(True, description="Normalize whitespace in comparisons")
    normalize_line_endings: bool = Field(True, description="Normalize line endings in comparisons")
    ignore_blank_lines: bool = Field(True, description="Ignore blank lines in comparisons")
    ignore_indentation: bool = Field(False, description="Ignore indentation changes in comparisons")


class ScanRequest(BaseModel):
    """Request model for scan endpoint."""

    model_config = {"extra": "forbid"}

    directory: str = Field(..., description="Directory to scan")
    include_pattern: Optional[str] = Field(None, description="Glob pattern to include files")
    exclude_pattern: Optional[str] = Field(None, description="Glob pattern to exclude files")
    target: str = Field("AI", description="Target audience (AI, HU, ALL)")
    normalize_whitespace: bool = Field(True, description="Normalize whitespace in comparisons")
    normalize_line_endings: bool = Field(True, description="Normalize line endings in comparisons")
    ignore_blank_lines: bool = Field(True, description="Ignore blank lines in comparisons")
    ignore_indentation: bool = Field(False, description="Ignore indentation changes in comparisons")


class MCPServer:
    """
    MCP Server for CodeGuard.

    This class implements a FastAPI-based MCP server for integration with
    IDEs and other tools.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize the MCP server.

        Args:
            host: Host to bind to (default: 127.0.0.1)
            port: Port to listen on (default: 8000)
        """
        self.host = host
        self.port = port
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        """
        Create the FastAPI application.

        Returns:
            Configured FastAPI application
        """
        app = FastAPI(
            title="CodeGuard MCP Server",
            description="MCP server for CodeGuard validation",
            version="0.1.0",
        )

        # Register routes
        self._register_routes(app)

        # Initialize MCP server
        mcp = FastApiMCP(
            app, name="CodeGuard MCP", description="MCP server for code guard validation"
        )
        mcp.mount()

        return app

    def _register_routes(self, app: "FastAPI"):
        """
        Register API routes.

        Args:
            app: FastAPI application to register routes on
        """

        @app.post("/validate", response_model=ValidationResponse, tags=["validation"])
        async def validate(request: ValidationRequest):
            """
            Validate changes between original and modified code.

            Args:
                request: Validation request

            Returns:
                Validation response with detected violations
            """
            # Create validator
            validator = CodeGuardValidator(
                normalize_whitespace=request.normalize_whitespace,
                normalize_line_endings=request.normalize_line_endings,
                ignore_blank_lines=request.ignore_blank_lines,
                ignore_indentation=request.ignore_indentation,
                target=request.target,
            )

            # Create temporary files for validation
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as original_file:
                original_file.write(request.original_content)
                original_path = original_file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as modified_file:
                modified_file.write(request.modified_content)
                modified_path = modified_file.name

            try:
                # Validate files
                result = validator.validate_files(original_path, modified_path)

                # Convert to API response
                return result.to_dict()

            finally:
                # Clean up temporary files
                os.unlink(original_path)
                os.unlink(modified_path)

        @app.post("/git-validate", response_model=ValidationResponse, tags=["validation"])
        async def git_validate(request: GitValidationRequest):
            """
            Validate changes against a git revision.

            Args:
                request: Git validation request

            Returns:
                Validation response with detected violations
            """
            # Create validator
            validator = CodeGuardValidator(
                normalize_whitespace=request.normalize_whitespace,
                normalize_line_endings=request.normalize_line_endings,
                ignore_blank_lines=request.ignore_blank_lines,
                ignore_indentation=request.ignore_indentation,
                target=request.target,
            )

            # Initialize git integration
            try:
                git = GitIntegration(request.repo_path)
            except GitError as e:
                raise HTTPException(status_code=400, detail=str(e))

            # Create temporary file for modified content
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as modified_file:
                modified_file.write(request.modified_content)
                modified_path = modified_file.name

            try:
                # Get file content from revision
                try:
                    revision_content = git.get_file_content(request.file_path, request.revision)
                except GitError as e:
                    # If file doesn't exist in the revision, it's a new file
                    if "does not exist" in str(e):
                        revision_content = ""
                    else:
                        raise HTTPException(status_code=400, detail=str(e))

                # Create temporary file for revision content
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", delete=False
                ) as original_file:
                    original_file.write(revision_content)
                    original_path = original_file.name

                try:
                    # Validate files
                    result = validator.validate_files(original_path, modified_path)

                    # Convert to API response
                    return result.to_dict()

                finally:
                    # Clean up temporary file for revision content
                    os.unlink(original_path)

            finally:
                # Clean up temporary file for modified content
                os.unlink(modified_path)

        @app.post("/revision-compare", response_model=ValidationResponse, tags=["validation"])
        async def revision_compare(request: RevisionCompareRequest):
            """
            Compare a file between two revisions.

            Args:
                request: Revision comparison request

            Returns:
                Validation response with detected violations
            """
            # Create validator
            validator = CodeGuardValidator(
                normalize_whitespace=request.normalize_whitespace,
                normalize_line_endings=request.normalize_line_endings,
                ignore_blank_lines=request.ignore_blank_lines,
                ignore_indentation=request.ignore_indentation,
                target=request.target,
            )

            # Initialize git integration
            try:
                git = GitIntegration(request.repo_path)
            except GitError as e:
                raise HTTPException(status_code=400, detail=str(e))

            # Compare file between revisions
            try:
                result = git.compare_file_between_revisions(
                    request.file_path, request.from_revision, request.to_revision, validator
                )

                # Convert to API response
                return result.to_dict()

            except GitError as e:
                raise HTTPException(status_code=400, detail=str(e))

        @app.post("/scan", response_model=ValidationResponse, tags=["validation"])
        async def scan(request: ScanRequest):
            """
            Scan a directory for guard violations.

            Args:
                request: Scan request

            Returns:
                Validation response with detected violations
            """
            directory = Path(request.directory)

            if not directory.is_dir():
                raise HTTPException(
                    status_code=400, detail=f"Directory does not exist: {directory}"
                )

            # Create validator
            validator = CodeGuardValidator(
                normalize_whitespace=request.normalize_whitespace,
                normalize_line_endings=request.normalize_line_endings,
                ignore_blank_lines=request.ignore_blank_lines,
                ignore_indentation=request.ignore_indentation,
                target=request.target,
            )

            # Scan directory
            result = validator.validate_directory(
                directory, request.include_pattern, request.exclude_pattern
            )

            # Convert to API response
            return result.to_dict()

        @app.get("/health", tags=["system"])
        async def health():
            """
            Health check endpoint.

            Returns:
                Health status
            """
            return {"status": "ok"}

    def run(self):
        """Run the MCP server."""
        try:
            import uvicorn

            uvicorn.run(self.app, host=self.host, port=self.port)
        except ImportError:
            raise ImportError(
                "FastAPI and its dependencies are required to run the MCP server. "
                "Install with: pip install fastapi fastapi-mcp uvicorn"
            )
