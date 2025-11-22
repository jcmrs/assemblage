# ADR-012: Test Coverage Reporting

**Date:** 2025-11-19
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
**Vision Owner Concurrence (Human Partner):** Yes
**System Owner Concurrence (AI Partner):** Yes

---

## 1. Context

The Assemblage relies on `pytest` for unit and integration testing. While we write tests for new features, we lack an objective, quantitative measure of their thoroughness. We are "flying blind" as to which parts of our codebase are exercised by the test suite and, more importantly, which parts are not. This is a significant gap in our quality assurance process and hinders the Auditor's ability to be data-driven.

## 2. Decision

We will integrate the `pytest-cov` library to generate code coverage reports.

1.  **New Dependency:** The `pytest-cov` package will be added to our project dependencies.
2.  **Control Plane Integration:** The `validate` command will be extended with a new `--coverage` flag. When invoked (`control_plane validate --coverage`), it will run the test suite with coverage enabled and display a summary report in the console. The `validate` command is the most logical home for this feature, as test coverage is a key metric for validating the overall health and quality of the codebase.
3.  **Default Test Runner Update:** The main test runner script, `run-assemblage-tests.sh`, will also be updated to generate a coverage report by default, making this metric a standard part of our continuous quality checks.

## 3. Rationale

*   **Data-Driven Quality:** Provides a concrete metric for test quality, moving us away from subjective assessments.
*   **Improved Auditing:** Empowers the Auditor workbench with a tool to quickly identify high-risk, untested code.
*   **Risk Reduction:** Highlighting untested code paths allows us to focus testing efforts where they are most needed, reducing the likelihood of regressions.
*   **Enhanced Discipline:** The constant visibility of the coverage metric encourages a more rigorous testing discipline for all new code.

## 4. Consequences

- A new dependency (`pytest-cov`) will be added to the project.
- The `validate` command's logic and definition in `config/commands.yml` will be modified.
- The `run-assemblage-tests.sh` script will be modified.
- This will slightly increase the time required to run the test suite, but the value of the generated report far outweighs this minor cost.
