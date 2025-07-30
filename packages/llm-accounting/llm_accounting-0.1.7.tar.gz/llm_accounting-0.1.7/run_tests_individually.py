import subprocess
import os
import sys
import time
from datetime import datetime

# Define the base directory for tests
TESTS_DIR = "tests"
# Timeout for each test in seconds
TEST_TIMEOUT = 15


def get_test_functions():
    """
    Dynamically discovers test functions from specified directories.
    This is a placeholder for the actual discovery logic.
    In a real scenario, this would parse the output of `pytest --collect-only`.
    For now, we'll hardcode based on the previous `list_code_definition_names` output.
    """
    test_functions = []

    # From tests/backends/
    test_functions.extend([
        "tests/backends/test_base.py::test_backend_interface",
        "tests/backends/test_base.py::test_backend_abstract_methods",
        "tests/backends/test_sqlite.py::test_initialize",
        "tests/backends/test_sqlite.py::test_insert_usage",
        "tests/backends/test_sqlite.py::test_get_period_stats",
        "tests/backends/test_sqlite.py::test_get_model_stats",
        "tests/backends/test_sqlite.py::test_get_model_rankings",
        "tests/backends/test_sqlite.py::test_purge",
        "tests/backends/test_sqlite.py::test_purge_empty_database",
        "tests/backends/test_usage_models.py::test_usage_entry_creation",
        "tests/backends/test_usage_models.py::test_usage_stats_creation",
    ])

    # From tests/cli/
    test_functions.extend([
        "tests/cli/test_cli_purge.py::test_purge_with_confirmation",
        "tests/cli/test_cli_purge.py::test_purge_without_confirmation",
        "tests/cli/test_cli_purge.py::test_purge_with_yes_flag",
        "tests/cli/test_cli_purge.py::test_purge_with_yes_flag_long",
        "tests/cli/test_cli_stats.py::test_stats_no_period",
        "tests/cli/test_cli_stats.py::test_stats_periods",
        "tests/cli/test_cli_stats.py::test_stats_custom_period",
        "tests/cli/test_cli_stats.py::test_custom_db_file_usage",
        "tests/cli/test_cli_stats.py::test_default_db_file_usage",
        "tests/cli/test_cli_stats.py::test_db_file_validation_error",
        "tests/cli/test_cli_stats.py::test_db_file_permission_error",
        "tests/cli/test_cli_tail.py::test_tail_default",
        "tests/cli/test_cli_tail.py::test_tail_custom_number",
        "tests/cli/test_cli_tail.py::test_tail_empty",
        "tests/cli/test_cli_track.py::test_track_usage_with_protected_db_file",
        "tests/cli/test_cli_track.py::test_track_usage",
        "tests/cli/test_cli_track.py::test_track_usage_with_timestamp",
        "tests/cli/test_cli_track.py::test_track_usage_with_caller_name",
        "tests/cli/test_cli_track.py::test_track_usage_with_username",
        "tests/cli/test_cli_track.py::test_track_usage_with_cached_tokens",
        "tests/cli/test_cli_track.py::test_track_usage_with_reasoning_tokens",
    ])

    # From tests/core/
    test_functions.extend([
        "tests/core/test_accounting_purge.py::test_purge",
        "tests/core/test_accounting_stats.py::test_get_period_stats",
        "tests/core/test_accounting_stats.py::test_get_model_stats",
        "tests/core/test_accounting_stats.py::test_get_model_rankings",
        "tests/core/test_accounting_tracking.py::test_track_usage",
        "tests/core/test_accounting_tracking.py::test_tail",
        "tests/core/test_accounting_tracking.py::test_tail_empty",
        "tests/core/test_accounting_tracking.py::test_tail_default_limit",
        "tests/core/test_accounting_tracking.py::test_track_usage_with_caller_and_user",
        "tests/core/test_accounting_tracking.py::test_tail_with_caller_and_user",
        "tests/core/test_accounting_validation.py::test_track_usage_empty_model",
        "tests/core/test_accounting_validation.py::test_track_usage_none_model",
        "tests/core/test_accounting_validation.py::test_usage_entry_empty_model",
        "tests/core/test_accounting_validation.py::test_usage_entry_none_model",
        "tests/core/test_accounting_validation.py::test_track_usage_without_timestamp",
        "tests/core/test_accounting_validation.py::test_track_usage_with_timestamp",
        "tests/core/test_accounting_validation.py::test_track_usage_with_token_details",
        "tests/core/test_accounting_validation.py::test_track_usage_default_token_details",
    ])

    return test_functions


def run_single_test(test_path):
    """Runs a single pytest and returns its status."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Running: {test_path}")
    sys.stdout.flush()

    # Determine the correct python executable for the venv
    if sys.platform == "win32":
        python_executable = os.path.join(".venv", "Scripts", "python.exe")
    else:
        python_executable = os.path.join(".venv", "bin", "python")

    if not os.path.exists(python_executable):
        print(f"Error: Virtual environment not found at {python_executable}. Please activate or create it.")
        return "ERROR_VENV_NOT_FOUND"

    command = [
        python_executable,
        "-m",
        "pytest",
        "--maxfail=1",  # As per .clinerules
        "--verbose",
        "--cov=llm_accounting",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--no-cov-on-fail",
        test_path
    ]

    try:
        start_time = time.time()
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=TEST_TIMEOUT,
            check=False  # Do not raise CalledProcessError for non-zero exit codes
        )
        end_time = time.time()
        duration = end_time - start_time

        if process.returncode != 0:
            if "failed" in process.stdout.lower() or "error" in process.stderr.lower():
                print(f"  -> FAILED (Exit Code: {process.returncode}, Duration: {duration:.2f}s)")
                sys.stdout.flush()
                print("--- STDOUT ---")
                sys.stdout.flush()
                print(process.stdout)
                sys.stdout.flush()
                print("--- STDERR ---")
                sys.stdout.flush()
                print(process.stderr)
                sys.stdout.flush()
                return "FAILED"
            else:
                print(f"  -> COMPLETED (Exit Code: {process.returncode}, Duration: {duration:.2f}s)")
                sys.stdout.flush()
                print("--- STDOUT ---")
                sys.stdout.flush()
                print(process.stdout)
                sys.stdout.flush()
                print("--- STDERR ---")
                sys.stdout.flush()
                print(process.stderr)
                sys.stdout.flush()
                return "COMPLETED"
        else:
            print(f"  -> PASSED (Duration: {duration:.2f}s)")
            sys.stdout.flush()
            return "PASSED"

    except subprocess.TimeoutExpired:
        print(f"  -> HUNG (Timeout after {TEST_TIMEOUT}s)")
        sys.stdout.flush()
        return "HUNG"
    except Exception as e:
        print(f"  -> ERROR: {e}")
        sys.stdout.flush()
        return "ERROR"


def main():
    all_tests = get_test_functions()
    total_tests = len(all_tests)
    print(f"Discovered {total_tests} individual tests.")
    sys.stdout.flush()
    print("-" * 50)
    sys.stdout.flush()

    results = {
        "PASSED": [],
        "FAILED": [],
        "HUNG": [],
        "ERROR": [],
        "COMPLETED": [],  # For tests that don't pass but also don't explicitly fail or hang
        "ERROR_VENV_NOT_FOUND": []
    }

    for i, test in enumerate(all_tests):
        print(f"Processing test {i + 1}/{total_tests}: {test}")
        sys.stdout.flush()
        status = run_single_test(test)
        results[status].append(test)
        print("-" * 50)
        sys.stdout.flush()

    print("\n--- Summary ---")
    sys.stdout.flush()
    print(f"Total Tests: {total_tests}")
    sys.stdout.flush()
    print(f"Passed: {len(results['PASSED'])}")
    sys.stdout.flush()
    print(f"Failed: {len(results['FAILED'])}")
    sys.stdout.flush()
    print(f"Hung (Timeout): {len(results['HUNG'])}")
    sys.stdout.flush()
    print(f"Completed (Non-zero exit, not failed): {len(results['COMPLETED'])}")
    sys.stdout.flush()
    print(f"Errors: {len(results['ERROR'])}")
    sys.stdout.flush()
    print(f"Venv Not Found Errors: {len(results['ERROR_VENV_NOT_FOUND'])}")
    sys.stdout.flush()

    if results['HUNG']:
        print("\n--- Tests that HUNG ---")
        sys.stdout.flush()
        for test in results['HUNG']:
            print(f"- {test}")
            sys.stdout.flush()

    if results['FAILED']:
        print("\n--- Tests that FAILED ---")
        sys.stdout.flush()
        for test in results['FAILED']:
            print(f"- {test}")
            sys.stdout.flush()

    if results['ERROR'] or results['ERROR_VENV_NOT_FOUND']:
        print("\n--- Tests with ERRORS ---")
        sys.stdout.flush()
        for test in results['ERROR']:
            print(f"- {test}")
            sys.stdout.flush()
        for test in results['ERROR_VENV_NOT_FOUND']:
            print(f"- {test} (Venv Error)")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
