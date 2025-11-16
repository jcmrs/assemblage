#!/bin/bash
#
# ⚙️ Utility: validate-workspace.sh
#
# (Version 1.4.0 - Assemblage "Bifurcated Ownership" Model)
#
# This is a "House Service" for the "Guardrails" (`.githooks/pre-commit`).
#
# PURPOSE:
# This script enforces our "Clean Separation" and "Bifurcated Ownership"
# model. It validates that a single commit does not contain changes to
# *both* the "Assemblage" (the "house") and the "Product" (the "furniture").
#
# This enforces our "Assemblage Change Protocol": changes to the "house"
# are a big deal and must be in their own atomic commit.
#
# This "smart" Utility reads its rules from our "master wiring diagram,"
# `config/workbenches.yml`.
#
# DEPENDENCY:
# Requires `yq` (defined in `ASSEMBLAGE.dependencies`).
#
#=======================================================================

# --- Configuration ---
# The "Anchor" (wiring diagram) this Utility reads
WORKBENCH_CONFIG="config/workbenches.yml"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[WORKSPACE] $1${NC}"
}
function error() {
    echo -e "${RED}[FAIL] $1${NC}" >&2
}
function info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# --- Guardrail: Check for `yq` dependency ---
if ! command -v yq &> /dev/null; then
    error "Dependency 'yq' not found!"
    echo -e "${YELLOW}Cannot validate workspace. Run 'tools/assemblage-setup.sh'.${NC}"
    exit 1
fi

# --- Guardrail: Check for `config` file ---
if [ ! -f "$WORKBENCH_CONFIG" ]; then
    error "Config file '$WORKBENCH_CONFIG' not found!"
    echo -e "${YELLOW}Cannot validate workspace. 'House' is missing its 'wiring diagram.'${NC}"
    exit 1
fi

# --- Main Logic ---
info "Validating workspace 'clean separation' (v1.4.0)..."

# 1. Read the "Assemblage" (house) paths from the config.
# These are the "read_only" files for the "Builder" workbench.
# We use `yq` to read the 'read_only' list from the 'builder' workbench.
ASSEMBLAGE_PATHS=($(yq e '.workbenches.builder.guardrail_workspace.read_only[]' "$WORKBENCH_CONFIG"))

# 2. Read the "Product" (furniture) paths from the config.
# These are the "read_write" files for the "Builder" workbench.
PRODUCT_PATHS=($(yq e '.workbenches.builder.guardrail_workspace.read_write[]' "$WORKBENCH_CONFIG"))

# 3. Check all staged files (passed as arguments $@ from the pre-commit hook)
FOUND_ASSEMBLAGE_CHANGE=false
FOUND_PRODUCT_CHANGE=false

for file in "$@"; do
    IS_ASSEMBLAGE_FILE=false
    IS_PRODUCT_FILE=false

    # Check if this file matches any "Assemblage" path
    for path in "${ASSEMBLAGE_PATHS[@]}"; do
        if [[ "$file" == "$path"* ]]; then
            FOUND_ASSEMBLAGE_CHANGE=true
            IS_ASSEMBLAGE_FILE=true
            break
        fi
    done

    # Check if this file matches any "Product" path
    for path in "${PRODUCT_PATHS[@]}"; do
        # We ignore '{{current_spec}}' templates here
        if [[ "$path" == *"{{"* ]]; then continue; fi
        
        if [[ "$file" == "$path"* ]]; then
            FOUND_PRODUCT_CHANGE=true
            IS_PRODUCT_FILE=true
            break
        fi
    done

    # --- Guardrail: Check for "un-categorized" files ---
    if [ "$IS_ASSEMBLAGE_FILE" = false ] && [ "$IS_PRODUCT_FILE" = false ]; then
        # Ignore files we explicitly don't track (like .gitignore)
        if [[ "$file" == ".gitignore" ]]; then
            continue
        fi
        
        error "Un-categorized file detected: '$file'"
        echo -e "${YELLOW}This file is not defined in the 'guardrail_workspace:' section"
        echo -e "${YELLOW}of '$WORKBENCH_CONFIG'. This is a 'How' (Platform) gap.${NC}"
        echo -e "${YELLOW}As System Owner, you MUST update the 'wiring diagram' to categorize this file.${NC}"
        exit 1
    fi
done

# ====================================================================
# FINAL RESULT (The "Guardrail" Enforcement)
# ====================================================================

if [ "$FOUND_ASSEMBLAGE_CHANGE" = true ] && [ "$FOUND_PRODUCT_CHANGE" = true ]; then
    # --- This is the FAILURE condition ---
    error "Workspace Boundary VIOLATION!"
    echo -e "${YELLOW}This commit contains changes to *both* the 'Assemblage' (the 'house' files)"
    echo -e "and the 'Product' (the 'furniture' files). This is not allowed.${NC}"
    echo -e "\n${BLUE}Nudge: This 'Nudge' comes from 'config/nudges.yml' (house_vs_furniture_check).${NC}"
    echo -e "${BLUE}As System Owner, you MUST separate these changes:${NC}"
    echo -e "  1. First, commit the 'Product' files (e.g., 'src/', 'specs/')."
    echo -e "  2. THEN, in a *separate* atomic commit, follow the"
    echo -e "     'guides/SYSTEM/assemblage-change-protocol.md' to commit"
    echo -e "     the 'Assemblage' files (e.g., 'config/', 'tools/')."
    exit 1
fi

if [ "$FOUND_ASSEMBLAGE_CHANGE" = true ]; then
    log "This is an 'Assemblage' (house) change."
    info "${BLUE}Nudge: Ensure you are following the 'assemblage-change-protocol.md' Guide.${NC}"
fi

if [ "$FOUND_PRODUCT_CHANGE" = true ]; then
    log "This is a 'Product' (furniture) change. Proceeding."
fi

log "Workspace 'clean separation' is valid."
exit 0
