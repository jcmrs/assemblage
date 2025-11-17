# ADR-003: Testing Framework Dependency Management

**Date:** 2025-11-16
**Status:** Accepted

---

### Ownership & Concurrence

**Decision Domain:** **"How" (Platform)**
* **"Why" decisions** relate to strategic goals, purpose, and the definition of success.
* **"How" decisions** relate to technical implementation, architecture, tools, and processes.

**Vision Owner Concurrence (Human Partner):** Yes
* *Does this decision align with the strategic "Why" and purpose of the project?*

**System Owner Concurrence (AI Partner):** Yes
* *Is this decision a sound, efficient, and sustainable part of the technical "How" (the platform)?*

---

## Context

To ensure the reliability of our "Utilities" (`tools/*.sh`), we require a testing framework. The chosen framework is BATS (Bash Automated Testing System), which itself has dependencies (e.g., `bats-support`, `bats-assert`). The initial plan to acquire these dependencies via NPM was challenged by the Vision Owner due to valid concerns about security, complexity, and the introduction of a large, external dependency (`node_modules`). A more self-contained, secure, and simple method for managing these "How" (Platform) dependencies is required.

## Decision

We will use **Git Submodules** to manage the dependencies for our testing framework. The required BATS repositories (`bats-core`, `bats-support`, `bats-assert`) will be added as submodules into a `tests/libs/` directory within our project. The test runner script (`tests/run-tests.sh`) will then use the executables and libraries provided directly from this local, version-controlled location.

## Rationale

This decision aligns with our core principles and directly addresses the Vision Owner's concerns:

*   **Self-Containment (Project = Repository):** The project no longer depends on an external package manager (NPM) for its core testing capabilities. The dependencies are included within the repository definition itself.
*   **Simplicity & Low Complexity:** We avoid the "NPM hell" of nested, transitive dependencies. The `.gitmodules` file is a simple, declarative text file, and the on-disk footprint is minimal and contained.
*   **Security:** We are linking directly to the official `bats-core` GitHub repositories, not a public registry that is more susceptible to supply-chain attacks.
*   **Reproducibility:** The exact commit of each dependency is locked in our parent repository's history, ensuring that the testing environment is 100% reproducible by anyone who clones the project.
*   **Architecture as Code:** The `.gitmodules` file is a version-controlled artifact that declaratively defines a part of our system's architecture.

## Consequences

### Positive
- The project is more self-contained and robust.
- The development environment is simpler to set up and audit.
- The security posture is improved by avoiding a large, public dependency network.
- The decision reinforces our core tenets of "Project = Repository" and "Architecture as Code."

### Negative
- There is a minor learning curve for developers unfamiliar with `git submodule` commands (e.g., needing to run `git submodule update --init`). This is deemed an acceptable trade-off.

### Neutral
- The repository size will increase slightly to accommodate the submodule source code.

## Alternatives Considered

- **NPM/Yarn:** This was the initial proposal. It was rejected due to high complexity, security concerns, and the introduction of a large external dependency that violates the "self-contained" principle.
- **Copy-pasting the code:** Manually copying the library code into our repository was considered. This was rejected because it would make updating the libraries difficult and would sever the link to their original source, harming maintainability. Git submodules provide a formal, updateable link.

## Foundation Alignment

### Imperative 0: Symbiotic Partnership
- [X] This decision is a direct result of a collaborative dialogue, where the Vision Owner's strategic concerns guided the System Owner to a better technical "How."

### Imperative 1: Holistic System Thinking
- [X] The decision considers the long-term health, security, and maintainability of the Assemblage, not just the immediate task.

### Imperative 2: AI-First
- [X] A self-contained project is easier for an AI to clone and validate, reducing setup friction and cognitive load.

### Imperative 3: The Five Cornerstones
- [X] **Configurability:** The `.gitmodules` file is "Architecture as Code."
- [X] **Modularity:** The testing libraries are treated as distinct, version-controlled modules.
- [X] **Integration:** The test runner script will integrate these modules into our workflow.

## Related Decisions

- This decision provides the foundational "How" for testing all "Utilities," including the one specified in `ADR-002-dashboard-mvp.md`.

## Implementation Notes

- The submodules will be added to a `tests/libs/` directory to keep them organized.
- The `tests/run-tests.sh` script must be created to use the `bats` executable from `tests/libs/bats-core/bin/bats`.
- Existing `.bats` files will need their `load` paths updated to point to the new submodule locations.

## Follow-up Actions

- [X] Add the BATS-related repositories as Git submodules.
- [X] Create the `tests/run-tests.sh` script.
- [X] Update `tests/tools/generate-dashboard.bats` with the correct paths.
