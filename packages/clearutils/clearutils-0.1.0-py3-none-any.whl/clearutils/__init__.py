"""
clearutils

A toolbox for clear, modular, script-friendly helpers—no advanced Python required.
"""

__version__ = "0.1.0"
__author__ = "Renya Wasson"
__license__ = "MIT"

# Optional: Import top-level helpers for easy access
from clearutils.src.clearutils.log import setup_logging, logw, logw_traceback, flush_logs
from clearutils.src.clearutils.format import currency, percentage
from .backup import backup_file
from .test import (
    assert_log, assert_log_label, assert_log_exception,
    run_test_safely, run_all_tests_randomized
)

# Assign aliases
curr = currency
per = percentage


# Optionally, set __all__ to control what gets imported with "from clearutils import *"
__all__ = [
    "setup_logging", "logw", "logw_traceback", "flush_logs",
    "currency", "percentage",
    "backup_file",
    "assert_log", "assert_log_label", "assert_log_exception",
    "run_test_safely", "run_all_tests_randomized",
]