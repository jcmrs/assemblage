# Research Report: Bash to Python Migration Strategy

**Author:** `bash_to_python_migration_specialist`
**Date:** 2025-11-16
**Status:** Completed

---

## 1. Executive Summary

Migrating our existing Bash utilities to Python is a straightforward process that will significantly increase their robustness and maintainability. This report provides a mapping of common Bash commands to their Python equivalents and outlines a clear migration path for each existing utility and its corresponding BATS test. The core principle is to replace shell command execution with direct API calls to Python's standard libraries (`subprocess`, `pathlib`, `os`).

---

## 2. General Migration Patterns

Instead of calling shell commands and parsing their text output, we will use Python's libraries to get structured data directly.

| Bash Operation (`.sh`) | Python Equivalent (`.py`) | Notes |
| :--- | :--- | :--- |
| `echo "message"` | `print("message")` | Standard output. |
| `cat file.txt` | `from pathlib import Path; Path("file.txt").read_text()` | Reads entire file content. |
| `ls -1 my_dir/` | `from pathlib import Path; [p.name for p in Path("my_dir").iterdir()]` | Returns a list of filenames. |
| `wc -l` (on `ls` output) | `len(list(Path("my_dir").iterdir()))` | Directly counts items without shell piping. |
| `git log ...` | `import subprocess; result = subprocess.run(["git", "log", ...], capture_output=True, text=True)` | Use the `subprocess` module to run external commands and capture their output. |
| `if [ -f "$FILE" ]` | `from pathlib import Path; if Path(FILE).is_file(): ...` | Use `pathlib` for all file system checks. |
| `mkdir -p my_dir` | `from pathlib import Path; Path("my_dir").mkdir(parents=True, exist_ok=True)` | Idempotent directory creation. |

---

## 3. Utility Migration Plan

The following table outlines the migration plan for each existing utility.

| Current Bash Utility | Target Python Module | Key Logic to Port |
| :--- | :--- | :--- |
| `tools/validate-assemblage.sh` | `assemblage/tools/validate_assemblage.py` | - Git status check (`subprocess`).<br>- Version comparison (`pathlib`).<br>- Wiring validation (`pyyaml` dependency to parse `.yml` files). |
| `tools/generate-dashboard.sh` | `assemblage/tools/generate_dashboard.py` | - All logic from the spec, using `pathlib` for file counts and `subprocess` for Git log. Will generate `.md` and `.json` files. |
| `tools/run-assemblage-tests.sh` | N/A - Replaced by `pytest` | The functionality of this script will be replaced by directly invoking `pytest` from the command line. |
| *(and so on for all other scripts)* | *(corresponding python module)* | *(breakdown of logic)* |

---

## 4. Test Migration Plan (BATS to Pytest)

Our existing BATS tests will be rewritten as Pytest tests. The structure is conceptually similar.

**Example: `tests/tools/generate-dashboard.bats`**

```bash
@test "creates output files" {
    run ./tools/generate-dashboard.sh
    assert_success
    assert_file_exist "STATUS.md"
}
```

**Equivalent Pytest Test: `tests/tools/test_generate_dashboard.py`**

```python
import subprocess
from pathlib import Path

def test_creates_output_files():
    # Run the python script
    result = subprocess.run(["python", "-m", "assemblage.tools.generate_dashboard"])
    
    # Assert it ran successfully
    assert result.returncode == 0
    
    # Assert files were created
    assert Path("STATUS.md").is_file()
    assert Path("status.json").is_file()
    
    # Teardown (cleanup)
    Path("STATUS.md").unlink()
    Path("status.json").unlink()
```

This pattern of "run a script, then assert things about the filesystem" will be used to migrate all BATS tests to Pytest. We will need to add `pyyaml` to our `requirements.txt` to support the `validate-wiring` logic.
