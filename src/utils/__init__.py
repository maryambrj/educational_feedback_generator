"""
Utility functions and helper scripts for the AI Notebook Grading System.
"""

# Import only safe modules that don't have circular dependencies
from .file_checker import check_files
from .rename_notebooks import rename_notebooks

# Note: solution_cli and solution_generator have import issues when imported at package level
# Import them directly when needed to avoid circular dependency problems

__all__ = [
    'check_files',
    'rename_notebooks'
]
