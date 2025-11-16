#!/bin/bash
#
# ⚙️ Utility: triage-docs.sh
#
# (Version 2.0.0 - Part of the "Triage & Renovation" feature)
#
# This is a "House Service" for the "System Owner" (AI).
#
# PURPOSE:
# This "Utility" (the "hands") executes the "Triage" protocol
# defined in the "Guide" (`guides/SYSTEM/triage-docs-protocol.md`).
#
# It "cleans" the "junk drawer" (`docs/`) folder by "triaging"
# every file into one of three new "clean" locations:
# 1. "House" Guides -> `guides/SYSTEM/`
# 2. "Product" Anchors -> `product/`
# 3. "Legacy" Memory -> `archive/perplex_legacy/docs/`
#
# This script uses `git mv` to preserve our "Process Memory" (history).
#
#=======================================================================

# --- Configuration ---
SOURCE_DIR="docs"
GUIDES_DIR="guides/SYSTEM"
PRODUCT_DIR="product"
ARCHIVE_DIR="archive/perplex_legacy/docs"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[TRIAGE] $1${NC}"
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

# --- Main "Triage" Function ---
# This function implements the logic from the "Guide"
function triage_file() {
    local file_path=$1
    local filename=$(basename "$file_path")

    # --- Guardrail: Skip empty/invalid paths ---
    if [ -z "$file_path" ] || [ ! -f "$file_path" ]; then
        return
    fi

    # --- Rule 1: Is this a "House" (Assemblage) Guide? ---
    # These are files we've identified as "Assemblage" protocols
    # that we want to *keep* and *use*.
    case $filename in
        "COMPLETENESS_REVIEW.md" | \
        "BRANCH_MANAGEMENT.md" | \
        "AGENT_WORKSPACE_COORDINATION.md" | \
        "LOCAL_AUTOMATION_STRATEGY.md" | \
        "BASIC_MEMORY_QUICK_REFERENCE.md" | \
        "CONTINUITY_AND_RECOVERY.md" )
            log "Rule 1 (House Guide): Moving '$file_path' -> '$GUIDES_DIR/'"
            git mv "$file_path" "$GUIDES_DIR/"
            ;;
        
    # --- Rule 2: Is this a "Product" (Furniture) Anchor? ---
    # These are files that define the "Product" (the "furniture"),
    # not the "Assemblage" (the "house").
    "PRODUCT_VISION.md" )
            log "Rule 2 (Product Anchor): Moving '$file_path' -> '$PRODUCT_DIR/'"
            git mv "$file_path" "$PRODUCT_DIR/"
            ;;

    # --- Rule 3: Is this "Historical" (Legacy) Process Memory? ---
    # This is the "default" rule. If it's not Rule 1 or 2,
    # it's "legacy contamination" and must be "archived."
    # This includes the "README.md" and all old "Perplexity" logs.
    * )
        log "Rule 3 (Legacy/Archive): Moving '$file_path' -> '$ARCHIVE_DIR/'"
        git mv "$file_path" "$ARCHIVE_DIR/"
        ;;
    esac
}

# --- Main Logic ---
log "Starting 'triage-docs' Utility..."

# --- Guardrail: Check for `git` dependency ---
if ! command -v git &> /dev/null; then
    error "Dependency 'git' not found!"
    exit 1
fi

# --- Guardrail: Check if Triage is already done ---
if [ ! -d "$SOURCE_DIR" ]; then
    log "Source directory '$SOURCE_DIR/' not found. Triage is likely complete."
    exit 0
fi

# --- Self-Provisioning: Create destination "Anchors" if they don't exist ---
log "Ensuring destination 'Anchors' (directories) exist..."
mkdir -p "$GUIDES_DIR"
mkdir -p "$PRODUCT_DIR"
mkdir -p "$ARCHIVE_DIR"

section "STEP 1: Triaging all files in '$SOURCE_DIR/'..."

# Find all files in the source directory and "triage" them one by one.
# We use `find ... -print0 | while ...` to handle files with spaces.
find "$SOURCE_DIR" -type f -print0 | while IFS= read -r -d '' file; do
    triage_file "$file"
done

# --- Guardrail: Check if the folder is now empty ---
# If the `find` command (excluding .gitkeep) returns anything,
# the `triage_file` logic failed or missed a new file.
if [ -n "$(find "$SOURCE_DIR" -type f -not -name ".gitkeep")" ]; then
    error "Triage FAILED. The '$SOURCE_DIR/' folder is not empty."
    info "As System Owner, you must manually triage the remaining files or update this 'Utility'."
    exit 1
else
    # "Demolish" the now-empty "junk drawer"
    info "Source directory '$SOURCE_DIR/' is now empty."
    git rm -rf "$SOURCE_DIR"
    log "Successfully 'demolished' the '$SOURCE_DIR/' directory."
fi

section "STEP 2: Nudge for Next Steps"

log "✅ 'Triage Docs' Utility Complete."
info "${BLUE}Nudge: This 'Utility' has created a large 'git status' (many moved files).${NC}"
info "${BLUE}Your *next* step is to follow the 'guides/SYSTEM/assemblage-change-protocol.md'${NC}"
info "${BLUE}to *atomically commit* this 'renovation' and update the 'Assemblage' version.${NC}"

exit 0
