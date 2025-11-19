# Idea: Self-Correction Loop for Guardrails

## 1. Concept

To evolve our Guardrails (specifically `pre-commit` hooks) from simple blockers into a self-correcting system, in alignment with the AI-First imperative.

## 2. Problem

When a pre-commit hook fails due to a fixable linting or formatting error, the AI's workflow is halted, requiring manual intervention from the Vision Owner. This is inefficient and not truly AI-First.

## 3. Proposed Solution

Enhance the pre-commit process with a simple retry mechanism.

1.  When `git commit` is run, the `pre-commit` hooks are triggered.
2.  If a hook fails but reports that it has fixed the files (e.g., `ruff --fix` or `ruff-format`), the system should not immediately fail.
3.  Instead, it should automatically run `git add .` on the modified files.
4.  It should then re-attempt the `git commit` command *one time*.
5.  If the commit succeeds on the second try, the workflow continues seamlessly.
6.  If it fails a second time, *then* the process should halt and report the error, requiring manual intervention.

## 4. Value Proposition

- **Reduces Friction:** Automates away a common class of low-level, trivial failures.
- **Increases AI Autonomy:** Allows the System Owner to solve its own simple problems without human intervention.
- **Improves Velocity:** Prevents the development cycle from being stopped for easily correctable issues.
