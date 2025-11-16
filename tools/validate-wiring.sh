#!/bin/bash
#
# ⚙️ Utility: validate-wiring.sh
#
# This is a "House Service" for the "Auditor" Workbench.
#
# PURPOSE:
# This script performs the "Dead-Wire Check." It validates the integrity
# of our "Architecture as Code" by parsing our configuration "Anchors"
# (`config/workbenches.yml`, `config/specialists.yml`) and ensuring
# every file path defined in them actually exists.
#
# This prevents a "Holistic System" failure where a "Workbench"
# (like the "Builder") tries to use a "Guide" or "Utility" that
# has been moved or deleted.
#
# This script is a "Nudge" that is run by our master "Utility,"
# `tools/validate-assemblage.sh`.
#
# DEPENDENCY:
# This script requires `yq`, a command-line YAML parser.
# This is a "How" (Platform) dependency. As System Owner,
# you must ensure `yq` is installed. (e.g., `pip install yq`)
#
#=======================================================================

# --- Configuration ---
# The "Anchors" (wiring diagrams) to validate
WORKBENCH_CONFIG="config/workbenches.yml"
SPECIALIST_CONFIG="config/specialists.yml"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[WIRING] $1${NC}"
}
function error() {
    echo -e "${RED}[FAIL] $1${NC}" >&2
}
function info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# --- Main Logic ---
log "Starting 'validate-wiring' Utility..."
PASSED=true

# --- Guardrail: Check for `yq` dependency ---
if ! command -v yq &> /dev/null; then
    error "Dependency 'yq' (YAML Parser) not found."
    echo -e "${YELLOW}As System Owner, you MUST install this 'How' (Platform) dependency.${NC}"
    echo -e "${YELLOW}e.g., 'pip install yq' or 'brew install yq'${NC}"
    exit 1
fi

info "Scanning '$WORKBENCH_CONFIG' for all defined file paths..."

# This `yq` command extracts *all* string values from the workbench config.
# `.. | select(type == "string")` recursively finds all strings.
# `grep -E '(\.md|\.sh|\.yml|\.json)$'` filters for strings that *look like* file paths.
# We also grep for `FOUNDATION.md` and `README.md` explicitly.
CONFIG_PATHS=$(yq e '.. | select(type == "string")' "$WORKBENCH_CONFIG" | \
    grep -E '(\.md|\.sh|\.yml|\.json|FOUNDATION\.md|README\.md|CLAUDE\.md|GEMINI\.md)$')

info "Scanning '$SPECIALIST_CONFIG' for all defined file paths..."
# We only care about the `output_anchor` paths here.
SPECIALIST_PATHS=$(yq e '.. | .output_anchor? // empty' "$SPECIALIST_CONFIG")

# Combine all paths into one list
ALL_PATHS="$CONFIG_PATHS\n$SPECIALIST_PATHS"

if [ -z "$ALL_PATHS" ]; then
    error "Could not find any paths to validate. Check 'yq' command."
    exit 1
fi

log "Found $(echo "$ALL_PATHS" | wc -l | xargs) 'wires' to check. Validating..."

# --- Loop and Check ---
# We use `while read` to safely iterate over paths, even if they
# are empty or contain spaces (though our paths shouldn't).
echo "$ALL_PATHS" | while IFS= read -r path; do
    if [ -z "$path" ]; then
        continue
    fi

    # --- Guardrail: Ignore "template" strings ---
    if [[ "$path" == *"{{"* ]]; then
        info "Ignoring template path: $path"
        continue
    fi

    # --- The Check: `[ -e ]` checks if the path (file or dir) exists ---
    if [ ! -e "$path" ]; then
        error "DEAD WIRE DETECTED! The path '$path' is defined in your config,"
        echo -e "${RED}  but the file/directory does not exist on disk.${NC}"
        PASSED=false
    fi
done

# ====================================================================
# FINAL RESULT
# ====================================================================
if [ "$PASSED" = true ]; then
    log "------------------------------------------------------"
    log "✅ 'Dead-Wire Check' PASSED."
    log "All 'house' configuration is correctly wired."
    exit 0 # Return success code
else
    error "------------------------------------------------------"
    error "❌ 'Dead-Wire Check' FAILED."
    error "One or more 'wires' (file paths) in your 'config/' are broken."
    error "As System Owner, you MUST fix these 'How' (Platform) integrity errors."
    exit 1 # Return failure code
fi
