#!/bin/bash
#
# ⚙️ Utility: validate-assemblage.sh
#
# (Version 1.1.0 - This version integrates the "Dead-Wire Check")
#
# This is the MASTER "House Service" for the "Auditor" Workbench.
#
# PURPOSE:
# This script is the single, primary "integrity check" for the Assemblage.
# It validates that the "house" is clean, version-aligned, and correctly wired.
#
# This script MUST pass before the Assemblage is considered stable.
#
# It performs THREE main checks:
# 1. GIT-INTEGRITY: Are all "house" files 100% committed?
# 2. VERSION-ALIGNMENT: Does `ASSEMBLAGE.version` match the `CHANGELOG.md`?
# 3. WIRING-INTEGRITY: Are all "config/" file paths valid (no "dead wires")?
#
#=======================================================================

# --- Configuration ---
# Define the "Anchors" (files) for versioning
VERSION_FILE="ASSEMBLAGE.version"
CHANGELOG_FILE="CHANGELOG.md"

# Define the "Assemblage" (house) directories and files to check
ASSEMBLAGE_PATHS=(
    "config/"
    "guides/"
    "tools/"
    ".githooks/"
    "ASSEMBLAGE.version"
    "CHANGELOG.md"
    "FOUNDATION.md"
    "README.md"
    "GEMINI.md"
    "CLAUDE.md"
    "decisions/"
)

# Define the "Utility" (sub-check) to run
WIRING_VALIDATOR_UTILITY="tools/validate-wiring.sh"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[VALIDATE] $1${NC}"
}
function error() {
    echo -e "${RED}[FAIL] $1${NC}" >&2
}
function info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}
function section() {
    echo -e "\n${CYAN}--- CHECK $1: $2 ---${NC}"
}

# --- Main Logic ---
log "Running MASTER Assemblage Integrity Validation (v1.1.0)..."
OVERALL_PASSED=true

# ====================================================================
# CHECK 1: GIT-INTEGRITY (The "Clean" Check)
# ====================================================================
section "1" "GIT-INTEGRITY"
info "Checking Git integrity for Assemblage ('house') files..."
GIT_CHANGES=$(git status --porcelain -- ${ASSEMBLAGE_PATHS[*]})

if [ -n "$GIT_CHANGES" ]; then
    error "Git Integrity Check FAILED."
    echo -e "${YELLOW}The following 'house' files are modified, untracked, or uncommitted:${NC}"
    echo "$GIT_CHANGES"
    echo -e "${YELLOW}The 'Assemblage' framework is in an unstable, uncommitted state.${NC}"
    OVERALL_PASSED=false
else
    log "Git Integrity Check PASSED. All 'house' files are clean and committed."
fi

# ====================================================================
# CHECK 2: VERSION-ALIGNMENT (The "Versioned" Check)
# ====================================================================
section "2" "VERSION-ALIGNMENT"
info "Checking Version alignment..."

if [ ! -f "$VERSION_FILE" ]; then
    error "Version Alignment Check FAILED. The '$VERSION_FILE' Anchor does not exist!"
    OVERALL_PASSED=false
elif [ ! -f "$CHANGELOG_FILE" ]; then
    error "Version Alignment Check FAILED. The '$CHANGELOG_FILE' Anchor does not exist!"
    OVERALL_PASSED=false
else
    CURRENT_VERSION=$(cat "$VERSION_FILE")
    # This command (`grep`, `head`, `sed`) extracts the first version number
    # (like "1.0.1") from the changelog.
    LATEST_CHANGELOG_VERSION=$(grep -E '## \[' "$CHANGELOG_FILE" | head -n 1 | sed -E 's/## \[([0-9]+\.[0-9]+\.[0-9]+)\].*/\1/')

    if [ "$CURRENT_VERSION" != "$LATEST_CHANGELOG_VERSION" ]; then
        error "Version Alignment Check FAILED."
        echo -e "${YELLOW}Version mismatch detected!${NC}"
        echo -e "${YELLOW}  '$VERSION_FILE' reports:   $CURRENT_VERSION${NC}"
        echo -e "${YELLOW}  '$CHANGELOG_FILE' reports: $LATEST_CHANGELOG_VERSION${NC}"
        OVERALL_PASSED=false
    else
        log "Version Alignment Check PASSED. Version '$CURRENT_VERSION' is aligned."
    fi
fi

# ====================================================================
# CHECK 3: WIRING-INTEGRITY (The "Dead-Wire" Check)
# ====================================================================
section "3" "WIRING-INTEGRITY"
info "Running 'Dead-Wire Check' Utility..."

if [ ! -f "$WIRING_VALIDATOR_UTILITY" ]; then
    error "Wiring Integrity Check FAILED."
    error "The 'Dead-Wire' Utility ('$WIRING_VALIDATOR_UTILITY') does not exist!"
    OVERALL_PASSED=false
else
    # Run the sub-script. It will output its own formatted logs.
    if ! ./"$WIRING_VALIDATOR_UTILITY"; then
        error "Wiring Integrity Check FAILED. See sub-utility output above."
        OVERALL_PASSED=false
    else
        log "Wiring Integrity Check PASSED. All config 'wires' are valid."
    fi
fi

# ====================================================================
# FINAL RESULT
# ====================================================================
if [ "$OVERALL_PASSED" = true ]; then
    log "------------------------------------------------------"
    log "✅ MASTER Assemblage Integrity Protocol PASSED."
    log "The 'house' is stable, clean, version-aligned, and correctly wired."
    exit 0 # Return success code
else
    error "------------------------------------------------------"
    error "❌ MASTER Assemblage Integrity Protocol FAILED."
    error "The 'house' is in an unstable state."
    error "As System Owner, you MUST fix the failed checks above."
    exit 1 # Return failure code
fi
