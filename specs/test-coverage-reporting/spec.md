# Specification: Test Coverage Reporting

This document provides the detailed technical blueprint for `ITEM-019`, implementing test coverage reporting as defined in `ADR-012`.

## 1. Dependency Management

- **File:** `requirements.txt`
- **Action:** Add the following line to the file:
    ```
    pytest-cov
    ```

## 2. Command Definition Update

- **File:** `config/commands.yml`
- **Action:** Locate the `validate` command and add a new argument to its `arguments` list.

```yaml
  validate:
    entry_point: "assemblage.commands.validate.run"
    help: "Run a full integrity check of the Assemblage."
    arguments:
      - name: "--coverage"
        action: "store_true"
        help: "Run tests with coverage reporting."
```

## 3. `validate` Command Logic Modification

- **File:** `assemblage/commands/validate.py`
- **Action:** The `run(args)` function will be modified to handle the new `--coverage` flag. A new private function will be added to handle the coverage execution.

```python
# Add this new private function
def _run_coverage_report():
    """Runs pytest with coverage and streams the output."""
    print("INFO: Generating test coverage report...")
    cmd = ["pytest", "--cov=assemblage", "--cov-report=term-missing"]
    # Use Popen to stream output in real-time
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    return process.poll() == 0

# Modify the existing run(args) function
def run(args):
    """Runs all validation checks or a coverage report."""
    if args.coverage:
        print(f"{BLUE}--- Running Test Suite with Coverage ---{NC}")
        if _run_coverage_report():
            sys.exit(0)
        else:
            sys.exit(1)

    # Existing validation logic follows
    print(f"{BLUE}--- Running MASTER Assemblage Integrity Validation ---{NC}")
    checks = [_check_git_integrity, _check_version_alignment, _check_wiring_integrity]
    # ... rest of the function
```

## 4. Default Test Runner Update

- **File:** `run-assemblage-tests.sh`
- **Action:** Modify the `pytest` execution line.
- **From:** `pytest`
- **To:** `pytest --cov=assemblage --cov-report=term-missing`

## 5. Test Plan

- **File:** `tests/commands/test_validate.py`
- **Action:** Add a new test function to validate the new flag.

```python
@patch("assemblage.commands.validate.subprocess.Popen")
def test_validate_coverage_flag(mock_popen):
    """Tests that the --coverage flag triggers the correct command."""
    # Mock the Popen process
    mock_process = MagicMock()
    mock_process.poll.return_value = 0 # Simulate success
    mock_process.stdout.readline.side_effect = ["--- report ---", ""]
    mock_popen.return_value = mock_process

    # Mock the args
    args = MagicMock()
    args.coverage = True

    with patch.object(validate.sys, "exit") as mock_exit:
        validate.run(args)

        # Assert that Popen was called with the correct coverage command
        mock_popen.assert_called_once_with(
            ["pytest", "--cov=assemblage", "--cov-report=term-missing"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        # Assert that the command exits successfully
        mock_exit.assert_called_once_with(0)
```

This blueprint provides a complete and actionable plan for the Builder.
