# capstone_with_input.py
"""
Main entry point for MTO order processing.
This file acts as a public interface for the dashboard and scripts.
"""

from capstone_utils.runner import run_batch_mode, run_input_mode

# __all__ means when a file imports this file, 
# it can only see run_batch_mode and run_input_mode
# Prevents frontend from clashing with backend
__all__ = ["run_batch_mode", "run_input_mode"]
