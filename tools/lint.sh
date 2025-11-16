#!/bin/bash
#
# ⚙️ Utility: lint.sh
#
# This is a "House Service" for the "System Owner" (AI) and
# is also used by the "Guardrails" (`.githooks/pre-commit`).
#
# PURPOSE:
# This script performs "static analysis" (Linting) on our "house"
# files. It is the automated "code quality" check for our "Assemblage."
#
# It ensures that our "How" (Platform) files are free from syntax
# errors, bugs, and stylistic issues.
#
# It checks:
# 1. Shell Scripts (`.sh`): Uses `shellcheck`
# 2. YAML Files (`.yml`): Uses `yamllint`
#
# This script reads our `ASSEMBLAGE.dependencies` "Anchor" to
# confirm the linters are installed.
#
#=======================================================================

# --- Configuration ---
# The "Anchors" (config files) for our linters
SHELLCHECK_CONFIG=".shellcheckrc"
YAMLLINT_CONFIG=".yamllint.yml"

# The "Assemblage" (house) paths to scan
SHELL_PATHS_TO_LINT=("tools/" ".githooks/")
YAML_PATHS_TO_LINT=("config/" ".github/workflows/")

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[LINT] $1${NC}"
}
function error() {
    echo -e "${RED}[FAIL] $1${NC}" >&2
}
function info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}
function section() {
    echo -e "\n${CYAN}--- $1 ---${NC}"
}

# --- Main Logic ---
log "Starting 'lint' Utility (Code Quality Check)..."
OVERALL_PASSED=true

# ====================================================================
# CHECK 1: SHELLCHECK (for Shell script quality)
# ====================================================================
section "CHECK 1: Running 'shellcheck' on Shell files"

# --- Guardrail: Check for `shellcheck` dependency ---
if ! command -v shellcheck &> /dev/null; then
    error "Dependency 'shellcheck' not found (defined in 'ASSEMBLAGE.dependencies')."
    error "Run 'tools/assemblage-setup.sh' to validate."
    OVERALL_PASSED=false
else
    # --- Guardrail: Check for config file ---
    if [ ! -f "$SHELLCHECK_CONFIG" ]; then
        error "'$SHELLCHECK_CONFIG' not found. Cannot lint shell files."
        OVERALL_PASSED=false
    else
        info "Finding all '.sh' files in: ${SHELL_PATHS_TO_LINT[*]} ..."
        # Use `find` to get all files, then pass to `shellcheck`
        find "${SHELL_PATHS_TO_LINT[@]}" -type f -name "*.sh" -exec \
            shellcheck --config="$SHELLCHECK_CONFIG" {} +
        
        if [ $? -ne 0 ]; then
            error "'shellcheck' found errors. See output above."
            OVERALL_PASSED=false
        else
            log "'shellcheck' PASSED. All 'Utility' scripts are clean."
        fi
    fi
fi

# ====================================================================
# CHECK 2: YAMLLINT (for YAML schema quality)
# ====================================================================
section "CHECK 2: Running 'yamllint' on YAML files"

# --- Guardrail: Check for `yamllint` dependency ---
if ! command -v yamllint &> /dev/null; then
    error "Dependency 'yamllint' not found (defined in 'ASSEMBLAGE.dependencies')."
    error "Run 'tools/assemblage-setup.sh' to validate."
    OVERALL_PASSED=false
else
    # --- Guardrail: Check for config file ---
    if [ ! -f "$YAMLLINT_CONFIG" ]; then
        error "'$YAMLLINT_CONFIG' not found. Cannot lint YAML files."
        OVERALL_PASSED=false
    else
        info "Scanning all '.yml' files in: ${YAML_PATHS_TO_LINT[*]} ..."
        # `yamllint` can scan directories recursively, which is simpler.
        yamllint --config-file "$YAMLLINT_CONFIG" "${YAML_PATHS_TO_LINT[@]}"

        if [ $? -ne 0 ]; then
            error "'yamllint' found errors. See output above."
            OVERALL_PASSED=false
        else
            log "'yamllint' PASSED. All 'Config' schemas are clean."
        fi
    fi
fi

# ====================================================================
# FINAL RESULT
# ====================================================================
if [ "$OVERALL_PASSED" = true ]; then
    log "------------------------------------------------------"
    log "✅ Lint Check PASSED."
    log "The 'house' foundation (code and config) is stable and clean."
    exit 0 # Return success code
else
    error "------------------------------------------------------"
    error "❌ Lint Check FAILED."
    error "Errors found in 'house' files. The foundation is 'wobbly'."
    error "As System Owner, you MUST fix these errors before committing."
    exit 1 # Return failure code
fi
