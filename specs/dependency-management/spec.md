# Specification: Autonomous Dependency Management

This document provides the detailed technical blueprint for `ITEM-023`, implementing the Autonomous Dependency Management capability as defined in `ADR-016`.

## 1. Command Definition

- **File:** `config/commands.yml`
- **Action:** Add the new `install_dependencies` command definition.

```yaml
  install_dependencies:
    entry_point: "assemblage.commands.install_dependencies.run"
    help: "Installs/updates dependencies from requirements.txt using pip."
```

## 2. `install_dependencies.py` Module Design

A new module, `assemblage/commands/install_dependencies.py`, will be created to house the command's logic.

### 2.1. Main `run(args)` function
This function will orchestrate the installation process:
1.  Print a header indicating the start of the process.
2.  Define the command to be executed: `cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]`. Using `sys.executable` is crucial as it guarantees that the `pip` corresponding to the currently running Python interpreter is used.
3.  Execute the command using `subprocess.run`.
    -   The output will be streamed live to the console so the user can see `pip`'s progress. This will be achieved by not capturing the output (`capture_output=False`) and letting it flow directly to the parent process's stdout/stderr.
    -   The return code will be checked (`check=False`).
4.  After the subprocess completes, check its `returncode`.
    -   If `0`, print a success message and exit with `sys.exit(0)`.
    -   If non-zero, print a failure message and exit with `sys.exit(1)`.

## 3. Test Plan

- **File:** `tests/commands/test_install_dependencies.py`
- **Strategy:** The tests will mock the `subprocess.run` call to avoid actually running `pip` during testing.

### 3.1. `test_install_success`
1.  **Arrange:** Patch `subprocess.run` to return a mock `CompletedProcess` object with `returncode=0`.
2.  **Act:** Call `install_dependencies.run(None)`.
3.  **Assert:**
    -   Verify that `subprocess.run` was called once with the correct command list (`[sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]`).
    -   Use `capsys` to assert that a "Success" message is printed to the console.
    -   Assert that the function attempts to exit with a status code of `0`. This can be tested by wrapping the call in `pytest.raises(SystemExit) as e` and checking `e.value.code == 0`.

### 3.2. `test_install_failure`
1.  **Arrange:** Patch `subprocess.run` to return a mock `CompletedProcess` object with `returncode=1`.
2.  **Act:** Call `install_dependencies.run(None)`.
3.  **Assert:**
    -   Verify that `subprocess.run` was called once with the correct command.
    -   Use `capsys` to assert that a "Failure" message is printed to the console.
    -   Assert that the function attempts to exit with a status code of `1` using `pytest.raises(SystemExit)`.

This blueprint provides a complete and actionable plan for the Builder.
