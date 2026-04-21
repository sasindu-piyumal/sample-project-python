import sys
import os

# Ensure the src/ directory is on sys.path so pytest can import
# llm_benchmark without requiring a full package installation.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
