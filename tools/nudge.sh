#!/bin/bash
#
# ⚙️ Utility: nudge.sh
# (Version 1.7.0 - The "On-Demand Telephone")
#
# This is a "House Service" for the "System Owner" (AI).
#
# PURPOSE:
# This script is the "on-demand telephone" that the System Owner (AI)
# uses to "call" a "behavioural Nudge" (a "microprompt")
# from the "Nudge Library" (`config/nudges.yml`).
#
# This script is NOT triggered automatically. It is "pulled"
# (executed) by the AI when its "training" (from the
# "Onboarding Exam") tells it to "pause and reflect."
#
# This script also acts as a "Firewall" (a Guardrail),
# as requested by the Vision Owner, to prevent "interference."
# It reads the "master wiring" (`config/workbenches.yml`) and
# *blocks* a Nudge if it is not "wired" to the current Workbench
# (e.g., protecting the "Builder" from "thinking" Nudges).
#
# USAGE (As AI):
#   tools/nudge.sh <NUDGE_ID> <CURRENT_WORKBENCH>
#
# Example (as Architect):
#   tools/nudge.sh holistic_check architect
#
# Example (as Builder - this will be blocked):
#   tools/nudge.sh holistic_check builder
#
#=======================================================================

# --- Configuration ---
# The "Anchors" (the "phone book" and "wiring diagram")
NUDGE_LIBRARY="config/nudges.yml"
WORKBENCH_CONFIG="config/workbenches.yml"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function error() {
    echo -e "${RED}[NUDGE FAIL] $1${NC}" >&2
}
function log_nudge() {
    echo -e "\n${CYAN}💡 NUDGE ($1):${NC}"
    echo -e "${CYAN}---------------------------------${NC}"
    echo -e "$2"
    echo -e "${CYAN}---------------------------------${NC}\n"
}

# --- Guardrail: Check for `yq` dependency ---
if ! command -v yq &> /dev/null; then
    error "Dependency 'yq' not found!"
    echo -e "${YELLOW}Cannot run 'nudge' Utility. Run 'tools/assemblage-setup.sh'.${NC}"
    exit 1
fi

# --- Input Validation ---
if [ -z "$1" ] || [ -z "$2" ]; then
    error "Usage: $0 <NUDGE_ID> <CURRENT_WORKBENCH>"
    echo -e "${YELLOW}Example: $0 holistic_check architect${NC}"
    exit 1
fi

NUDGE_ID=$1
CURRENT_WORKBENCH=$2

# ====================================================================
# STEP 1: "The Firewall" (Check the "Wiring")
#
# Read the `config/workbenches.yml` "Anchor" to see if this
# <NUDGE_ID> is "wired" to this <CURRENT_WORKBENCH>.
#=======================================================================

# We use `yq` to:
# 1. Find the specific workbench (e.g., `workbenches.builder`)
# 2. Get its `available_nudges` list
# 3. Check if our `$NUDGE_ID` is in that list
#
IS_AUTHORIZED=$(yq e ".workbenches.$CURRENT_WORKBENCH.available_nudges[] | select(. == \"$NUDGE_ID\")" "$WORKBENCH_CONFIG")

if [ -z "$IS_AUTHORIZED" ]; then
    # --- This is the "Firewall" blocking the Nudge ---
    error "Nudge '$NUDGE_ID' is NOT available for the '$CURRENT_WORKBENCH' Workbench."
    echo -e "${YELLOW}This is a 'How' (Platform) Guardrail to prevent 'interference' (context contamination)."
    echo -e "${YELLOW}The '$CURRENT_WORKBENCH' Workbench must remain in 'deep focus' (doing), not 'thinking'.${NC}"
    exit 1
fi

# ====================================================================
# STEP 2: "The Telephone" (Deliver the "Whisper")
#
# If the "Firewall" passed, "dial" the "Nudge Library"
# and "whisper" the microprompt to the AI.
# ====================================================================

NUDGE_TEXT=$(yq e ".nudges.$NUDGE_ID" "$NUDGE_LIBRARY")

if [ -z "$NUDGE_TEXT" ] || [ "$NUDGE_TEXT" == "null" ]; then
    error "Nudge ID '$NUDGE_ID' does not exist in the 'Nudge Library' ($NUDGE_LIBRARY)."
    exit 1
fi

# Deliver the "whisper"
log_nudge "$NUDGE_ID" "$NUDGE_TEXT"
exit 0
