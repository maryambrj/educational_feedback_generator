#!/usr/bin/env python3
"""
Main entry point for the AI-Enhanced Notebook Grading System
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.main_ai_grader import main

if __name__ == "__main__":
    main()
