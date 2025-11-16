#!/bin/bash
#
# ⚙️ Utility: demolish-legacy-systems.sh
#
# (Version 2.0.0 - Part of the "Triage & Renovation" feature)
#
# This is a "House Service" for the "System Owner" (AI).
#
# PURPOSE:
# This "Utility" (the "demolition crew") executes the "Demolition"
# part of our "Renovation" plan. It removes the primary sources
# of "cognitive contamination" from the old `perplex` repository.
#
# It performs two actions:
# 1. ARCHIVE: Moves the `prompts/` (legacy process memory)
#    to the `archive/` folder, preserving its Git history.
# 2. DEMOLISH: Deletes the entire `.claude/` directory, which
#    contains all the "CDIR/CEXE" and hardcoded "Spec Kit"
#    "contamination."
#
# WARNING: This is a destructive (but necessary) action.
#
#=======================================================================

# --- Configuration ---
LEGACY_PROMPTS_DIR="prompts"
LEGACY_CLAUDE_DIR=".claude"
ARCHIVE_DIR="archive/perplex_legacy/prompts"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[DEMOLISH] $1${NC}"
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
log "Starting 'demolish-legacy-systems' Utility..."

# --- Guardrail: Check for `git` dependency ---
if ! command -v git &> /dev/null; then
    error "Dependency 'git' not found!"
    exit 1
fi

# --- Self-Provisioning: Create destination "Anchor" if it doesn't exist ---
mkdir -p "$ARCHIVE_DIR"

# ====================================================================
# STEP 1: Archive "Legacy Process Memory" (`prompts/`)
# ====================================================================
section "STEP 1: Archiving '$LEGACY_PROMPTS_DIR/'"

if [ -d "$LEGACY_PROMPTS_DIR" ]; then
    info "Archiving '$LEGACY_PROMPTS_DIR/' -> '$ARCHIVE_DIR/'..."
    # Use `git mv` to preserve Git history
    git mv "$LEGACY_PROMPTS_DIR"/* "$ARCHIVE_DIR/"
    git rm -rf "$LEGACY_PROMPTS_DIR"
    log "Successfully archived '$LEGACY_PROMPTS_DIR/'."
else
    log "'$LEGACY_PROMPTS_DIR/' not found. Already archived."
fi

# ====================================================================
# STEP 2: Demolish "Cognitive Contamination" (`.claude/`)
# ====================================================================
section "STEP 2: Demolishing '$LEGACY_CLAUDE_DIR/'"

if [ -d "$LEGACY_CLAUDE_DIR" ]; then
    info "Demolishing '$LEGACY_CLAUDE_DIR/' (CDIR/CEXE identities, hardcoded Spec Kit)..."
    # Use `git rm -rf` to completely remove it from the repository
    git rm -rf "$LEGACY_CLAUDE_DIR"
    log "Successfully demolished '$LEGACY_CLAUDE_DIR/'."
else
    log "'$LEGACY_CLAUDE_DIR/' not found. Already demolished."
fi

# ====================================================================
# FINAL NUDGE
# ====================================================================
log "✅ 'Demolition' Utility Complete."
info "${BLUE}Nudge: This 'Utility' has created a large 'git status' (many moved/deleted files).${NC}"
info "${BLUE}Your *next* step is to follow the 'guides/SYSTEM/assemblage-change-protocol.md'${NC}"
info "${BLUE}to *atomically commit* this 'renovation' and update the 'Assemblage' version.${NC}"

exit 0
