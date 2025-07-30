"""
Main entry point for CodeGuard when run as a module.
"""

import sys

# Check for required dependencies at startup
try:
    import tree_sitter
except ImportError:
    print("ERROR: tree-sitter is not installed.", file=sys.stderr)
    print("Please install it with: pip install tree-sitter", file=sys.stderr)
    sys.exit(1)

# Check for tree-sitter language modules
required_modules = [
    "tree_sitter_python",
    "tree_sitter_javascript",
    "tree_sitter_typescript",
    "tree_sitter_java",
    "tree_sitter_c_sharp",
    "tree_sitter_cpp",
    "tree_sitter_go",
    "tree_sitter_rust",
    "tree_sitter_ruby",
    "tree_sitter_php",
    "tree_sitter_html",
    "tree_sitter_css",
]

missing_modules = []
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print("ERROR: Missing tree-sitter language modules:", file=sys.stderr)
    for module in missing_modules:
        print(f"  - {module}", file=sys.stderr)
    print("\nPlease install them with:", file=sys.stderr)
    print(f"  pip install {' '.join(missing_modules)}", file=sys.stderr)
    sys.exit(1)

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
