#!/bin/bash
#
# ⚙️ Utility: create-new-specialist.sh
#
# This script is a "House Service" for the System Owner (AI).
#
# PURPOSE:
# This "Utility" (the "hands") executes the "Self-Provisioning"
# "Nudge" (from our "Identity Anchors"). It makes the "Assemblage"
# "Extensible" by allowing the System Owner (AI) to
# dynamically "provision" a new "Cognitive Specialist."
#
# It "writes" the new specialist's "schema" to the
# "config/specialists.yml" "Anchor" (the "registry").
#
# This "Utility" MUST be followed by the
# "guides/SYSTEM/assemblage-change-protocol.md" to
# commit this "How" (Platform) change.
#
#=======================================================================

# --- Configuration ---
# Anchors this Utility to the core configuration file
REGISTRY_FILE="config/specialists.yml"
TEMPLATE_FILE="guides/TEMPLATES/cognitive_specialist_template.md"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[UTILITY] $1${NC}"
}
function error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}
function prompt() {
    # We use stderr for prompts so they don't pollute stdout
    # if we try to pipe this script later.
    echo -e "\n${BLUE}[PROMPT] $1${NC}" >&2
}

# --- Main Logic ---
log "Starting 'create-new-specialist' Utility..."

# 1. Ensure the "wiring diagram" (registry) exists
if [ ! -f "$REGISTRY_FILE" ]; then
    error "Specialist Registry not found at '$REGISTRY_FILE'!"
    error "Cannot provision new specialist. This is a 'How' (Platform) failure."
    exit 1
fi

# 2. Get the new specialist's name (the ID)
prompt "Enter the unique ID for the new specialist (e.g., 'mcp_architect'):"
read -r specialist_id

if [ -z "$specialist_id" ]; then
    error "Specialist ID cannot be empty."
    exit 1
fi

# 3. Guardrail: Check if specialist already exists (using grep)
if grep -q "  $specialist_id:" "$REGISTRY_FILE"; then
    error "Specialist ID '$specialist_id' already exists in '$REGISTRY_FILE'."
    error "Aborting. Please use a unique ID."
    exit 1
fi

# 4. Get the human-readable description
prompt "Enter the one-sentence description for '$specialist_id':"
read -r specialist_desc

# 5. Get the output anchor (where it files reports)
prompt "Enter the output_anchor path (e.g., 'knowledge/research/mcp_report.md'):"
read -r specialist_output

# 6. Get the Guide Prompt (the "how-to" for the specialist)
prompt "Enter the multi-line 'guide_prompt' for this specialist."
prompt "(This is the 'how-to' based on '$TEMPLATE_FILE'.)"
prompt "(Type 'EOF' on a new line when you are finished)"

guide_prompt=""
while IFS= read -r line; do
    if [ "$line" == "EOF" ]; then
        break
    fi
    guide_prompt+="$line\n"
done

# 7. Provision the new specialist (append to YAML)
log "Registering new specialist '$specialist_id' in '$REGISTRY_FILE'..."

# Note: The indentation here is critical for YAML syntax.
# We are appending a new YAML object to the "specialists" map.
# The `|` character is for a multi-line string (the prompt).
# The `sed` command adds 4 spaces to indent the prompt correctly.
{
    echo ""
    echo "  # ===================================================================="
    echo "  # SPECIALIST: $specialist_id"
    echo "  # Purpose: $specialist_desc"
    echo "  # ===================================================================="
    echo "  $specialist_id:"
    echo "    description: \"$specialist_desc\""
    echo "    output_anchor: \"$specialist_output\""
    echo "    guide_prompt: |"
    echo -e "$guide_prompt" | sed 's/^/    /'
} >> "$REGISTRY_FILE"

log "Successfully provisioned new Cognitive Specialist: '$specialist_id'."
log "The 'Explorer' workbench can now delegate to this specialist."
info "${BLUE}Nudge: This is an 'Assemblage' (house) change. You MUST now follow the"
info "${BLUE}'guides/SYSTEM/assemblage-change-protocol.md' to validate, version, and commit this change.${NC}"
