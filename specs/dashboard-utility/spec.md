# Specification: `generate-dashboard.sh` Utility

This document specifies the design for the `tools/generate-dashboard.sh` utility.

## 1. Objective

The script will gather status information about the Assemblage framework and the project's progress and output it into two files: `STATUS.md` (human-readable) and `status.json` (machine-readable).

## 2. Component Design

The script will be a Bash script, designed to be run from the root of the project. It will be structured into the following logical phases:

### Phase 1: Data Gathering

The script will collect the following pieces of data and store them in shell variables:

1.  **Timestamp:**
    *   **Command:** `date -u +"%Y-%m-%dT%H:%M:%SZ"`
    *   **Variable:** `GENERATED_AT`

2.  **Assemblage Integrity & Version:**
    *   **Command:** `tools/validate-assemblage.sh`
    *   **Logic:** Capture the exit code. If `0`, status is "STABLE". Otherwise, "UNSTABLE".
    *   **Variable:** `ASSEMBLAGE_STATUS`
    *   **Command:** `cat ASSEMBLAGE.version`
    *   **Variable:** `ASSEMBLAGE_VERSION`

3.  **Conveyor Belt Metrics:**
    *   **Command:** `ls -1 ideas/ | wc -l`
    *   **Variable:** `IDEAS_COUNT`
    *   **Command:** `ls -1 backlog/items/ | wc -l`
    *   **Variable:** `BACKLOG_COUNT`
    *   **Command:** `ls -1 specs/ | wc -l` (Assuming one directory per spec)
    *   **Variable:** `SPECS_COUNT`

4.  **Recent Activity:**
    *   **Command:** `git log -n 5 --pretty=format:'%h|%s'` (Using a pipe `|` as a separator for easy parsing).
    *   **Variable:** `GIT_LOG_RAW`

### Phase 2: JSON Generation

The script will use the gathered variables to construct the `status.json` file. It will use a series of `echo` statements and here-document syntax to build the JSON structure, ensuring proper quoting and comma placement.

**Structure:**
```json
{
  "generated_at": "$GENERATED_AT",
  "assemblage_health": {
    "integrity_status": "$ASSEMBLAGE_STATUS",
    "framework_version": "$ASSEMBLAGE_VERSION"
  },
  "project_progress": {
    "conveyor_belt": {
      "ideas": $IDEAS_COUNT,
      "backlog": $BACKLOG_COUNT,
      "specs": $SPECS_COUNT
    },
    "recent_activity": [
      // Loop through GIT_LOG_RAW to generate these entries
    ]
  }
}
```

### Phase 3: Markdown Generation

The script will use the same variables to construct the `STATUS.md` file, using `echo` statements to write Markdown formatted text.

**Structure:**
```markdown
# Assemblage Status Report

*Generated: $GENERATED_AT*

---

## 🏛️ Assemblage Health ("The House")

- **Integrity Status:** ...
- **Framework Version:** ...

---
... etc ...
```

### Phase 4: File Permissions

*   **Command:** `chmod +x tools/generate-dashboard.sh`
*   **Logic:** This will be done once upon file creation.

### Phase 5: .gitignore

*   **Command:** `echo "STATUS.md" >> .gitignore` and `echo "status.json" >> .gitignore`
*   **Logic:** This will be done once upon file creation.

## 3. BATS Test (`tests/tools/generate-dashboard.bats`)

A corresponding BATS test will be created to validate the script's functionality. The test will:
1.  Run the `tools/generate-dashboard.sh` script.
2.  Check that `STATUS.md` and `status.json` are created.
3.  Check that `STATUS.md` contains key expected strings (e.g., "Assemblage Health", "Framework Version").
4.  Use a tool like `jq` (which will be a dev dependency) to validate the structure of `status.json` and check a value (e.g., `jq -e '.assemblage_health.framework_version' status.json`).
5.  Clean up the generated files.
