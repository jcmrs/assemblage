# ADR-004: BLOCKER - Unresolvable Line Ending Conflict

**Date:** 2025-11-16
**Status:** Blocker

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**

**Vision Owner Concurrence (Human Partner):** N/A
**System Owner Concurrence (AI Partner):** Yes

---

## Context

The System Owner (AI) is attempting to create and test a new Bash-based "Utility" (`tools/generate-dashboard.sh`). The development environment consists of a Windows 11 host, where an AI agent creates files, and a `Git Bash` execution environment, which requires Unix-style (LF) line endings for its scripts.

## The Problem: A Fundamental Environmental Conflict

1.  **File Creation:** The AI's `write_file` tool creates files with Windows-style CRLF line endings native to the host OS.
2.  **Execution Failure:** The `Git Bash` interpreter cannot execute these scripts, failing with errors like `/usr/bin/env: ‘bash\r’: No such file or directory`.
3.  **Architectural Solution Failure:** An architectural solution using a `.gitattributes` file was implemented (`ADR-003`). This was insufficient on its own.
4.  **Expert Workflow Failure:** A subsequent expert consultation recommended a `git checkout -- .` workflow to force normalization on the working directory. This workflow was executed but **also failed to resolve the issue**, with the `bash\r` error persisting. This proves the problem is not with the Git repository state, but with the local file system interaction.
5.  **Programmatic Remediation Failure:** All direct attempts by the AI to programmatically convert the line endings *before execution* have failed, leading to file corruption or no change.

**The project is in a HARD BLOCKED state.** The System Owner cannot create or test any Bash-based automation.

## Rationale for Blocker Status

The AI has exhausted all known methods to resolve this conflict. The core tools (`write_file`, `run_shell_command` with `bash`) are in a fundamental, irreconcilable conflict on the current host OS. The AI lacks a reliable tool to manipulate file encodings in the working directory. Continuing to attempt solutions without new information or tools would be an unproductive loop.

## Consequences

### Negative
- **All Bash-based automation is halted.** No new "Utilities" or test scripts can be created or validated.
- The `generate-dashboard.sh` feature is blocked.
- The integrity of the "Assemblage Change Protocol" is compromised, as the testing phase cannot be completed.

## Alternatives Considered

-   **Git `core.autocrlf`:** Rejected as it's a local configuration and not a repository-level solution.
-   **`.editorconfig`:** Rejected as it only applies to supporting editors, not programmatic file creation.
-   **`.gitattributes`:** Implemented, but proven insufficient as it does not affect the working directory in the required manner for immediate script execution.
-   **Programmatic Conversion (PowerShell):** Multiple attempts have failed, leading to file corruption or no change.

## Next Steps

**This issue requires external intervention from the Vision Owner.**

The System Owner requires a new capability or a definitive, working command that can be executed within the `run_shell_command` tool to reliably convert a text file's line endings from CRLF to LF on the Windows host. Without this, the "How" of the Assemblage is broken.
