#!/bin/bash
#
# ⚙️ Utility: assemblage-setup.sh
#
# (Version 2.0.0 - This version "installs" dependencies,
#  including the external "spec-kit" via `uv`.)
#
# This is the "Master Setup" script for the Assemblage.
#
# PURPOSE:
# This is the "on-first-run" Utility that provisions the local
# environment. It makes the "house" livable for the System Owner (AI)
# and usable for the Vision Owner (Human).
#
# It performs two main actions:
# 1. DEPENDENCY INSTALL: It reads the `ASSEMBLAGE.dependencies` "Anchor"
#    and *attempts to install* any missing "How" (Platform) tools.
# 2. GUARDRAIL INSTALL: It installs the local Git Hooks (`.githooks/`)
#    to activate our "Guardrails" (like `pre-commit`).
#
#=======================================================================

# --- Configuration ---
# The "Anchor" (Bill of Materials) this Utility reads
DEPENDENCIES_FILE="ASSEMBLAGE.dependencies"
# The "Utility" this script calls to install hooks
INSTALL_HOOKS_UTILITY="tools/install-hooks.sh"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NC="\033[0m" # No Color

# --- Helper Functions ---
function log() {
    echo -e "${GREEN}[SETUP] $1${NC}"
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

# --- "How" (Platform) Installer Function ---
# This is a "best-effort" installer for our dependencies.
# It makes the "house" "AI-First" by *trying* to solve
# its own "How" (Platform) gaps.
function attempt_install() {
    local dep=$1
    
    info "Attempting 'best-effort' install for '$dep'..."
    
    # "How" (Platform) logic for specific dependencies
    
    # --- 1. `uv` (The "spec-kit" installer) ---
    if [ "$dep" == "uv" ]; then
        if command -v pip &> /dev/null; then
            log "Installing 'uv' via 'pip'..."
            pip install uv
            return $?
        elif command -v pip3 &> /dev/null; then
            log "Installing 'uv' via 'pip3'..."
            pip3 install uv
            return $?
        elif command -v curl &> /dev/null; then
             log "Installing 'uv' via 'curl' (Linux/macOS)..."
             curl -LsSf https://astral.sh/uv/install.sh | sh
             return $?
        else
            error "Could not install 'uv'. 'pip', 'pip3', or 'curl' not found."
            return 1
        fi
    fi

    # --- 2. `spec-kit` (Uses `uv`, as per Vision Owner research) ---
    if [ "$dep" == "spec-kit" ]; then
        if ! command -v uv &> /dev/null; then
            error "Cannot install 'spec-kit'. 'uv' (its installer) is missing."
            return 1
        fi
        log "Installing 'spec-kit' CLI via 'uv' (this may take a moment)..."
        # This is the "best practice" command from the `spec-kit` docs
        uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
        return $?
    fi

    # --- 3. "How" (Platform) logic for common package managers (yq, bats, etc) ---
    if command -v brew &> /dev/null; then
        log "Attempting install '$dep' via 'brew' (macOS)..."
        brew install "$dep"
    elif command -v apt-get &> /dev/null; then
        log "Attempting install '$dep' via 'apt-get' (Debian/Ubuntu)..."
        # We assume sudo is available or not needed (e.g., in a container)
        apt-get update && apt-get install -y "$dep"
    elif command -v yum &> /dev/null; then
        log "Attempting install '$dep' via 'yum' (RedHat/CentOS)..."
        yum install -y "$dep"
    else
        error "No recognized installer (brew, apt, yum) found for '$dep'."
        return 1
    fi
}

# --- Main Logic ---
log "Starting 'assemblage-setup' Utility (v2.0.0)..."
log "This will validate/install dependencies and install local Guardrails."
OVERALL_PASSED=true

# ====================================================================
# STEP 1: VALIDATE & INSTALL DEPENDENCIES ("Bill of Materials")
# ====================================================================
section "STEP 1: Checking Environment Dependencies"

if [ ! -f "$DEPENDENCIES_FILE" ]; then
    error "Dependency file '$DEPENDENCIES_FILE' not found!"
    error "Cannot validate environment. This is a critical 'How' (Platform) failure."
    exit 1
fi

MISSING_DEPS=()
# We read the file, filtering out comments and blank lines
while IFS= read -r dep; do
    if [ -z "$dep" ] || [[ "$dep" == \#* ]]; then
        continue # Skip empty lines and comments
    fi
    
    # We use `spec-kit` to check for `specify`, the *actual* command
    check_cmd=$dep
    if [ "$dep" == "spec-kit" ]; then
        check_cmd="specify"
    fi

    if ! command -v "$check_cmd" &> /dev/null; then
        # --- (NEW "HOW" LOGIC) ---
        info "Dependency '$dep' (command '$check_cmd') is NOT installed."
        if attempt_install "$dep"; then
            # Re-check after attempting install
            if ! command -v "$check_cmd" &> /dev/null; then
                error "Install attempt for '$dep' FAILED."
                MISSING_DEPS+=("$dep")
                OVERALL_PASSED=false
            else
                log "Successfully installed '$dep'."
            fi
        else
            error "Install attempt for '$dep' FAILED (no valid installer)."
            MISSING_DEPS+=("$dep")
            OVERALL_PASSED=false
        fi
        # --- (END NEW "HOW" LOGIC) ---
    else
        log "Dependency '$dep' (command '$check_cmd') is installed."
    fi
done < <(grep -vE '^(#|$)' "$DEPENDENCIES_FILE")


if [ "$OVERALL_PASSED" = false ]; then
    echo -e "\n${YELLOW}One or more 'How' (Platform) dependencies are *still* missing:${NC}"
    for dep in "${MISSING_DEPS[@]}"; do
        echo -e "${RED}- $dep${NC}"
    done
    echo -e "${YELLOW}As System Owner (or with Vision Owner help), please install these tools manually.${NC}"
else
    log "All environment dependencies are installed."
fi

# ====================================================================
# STEP 2: INSTALL GUARDRAILS (The "Git Hooks" Setup)
# ====================================================================
section "STEP 2: Installing Local Guardrails"

if [ ! -f "$INSTALL_HOOKS_UTILITY" ]; then
    # This utility (install-hooks.sh) is one *we* provide in this
    # bootstrap, so it *should* exist. But we must check.
    # The original `perplex` repo has this file, so we
    # must "seed" it in our Assemblage.
    #
    # ---
    # "How" (Platform) Self-Correction: The "install-hooks.sh"
    # script is *missing* from our "Package 8" list.
    # I (the System Owner) must add it to our "Modular Delivery"
    # checklist. For now, I will error out.
    # ---
    error "The 'install-hooks.sh' Utility was not found at '$INSTALL_HOOKS_UTILITY'!"
    error "This 'Utility' is a required 'Lego brick' for the Assemblage."
    error "Cannot install 'Guardrails'. The 'house' is insecure."
    OVERALL_PASSED=false
else
    info "Running the 'install-hooks' Utility..."
    # Execute the sub-script
    if ! ./"$INSTALL_HOOKS_UTILITY"; then
        error "The 'install-hooks' Utility failed."
        error "Guardrails are NOT active. This is a critical 'How' (Platform) failure."
        OVERALL_PASSED=false
    else
        log "Successfully installed 'Guardrails' (Git Hooks)."
    fi
fi

# ====================================================================
# FINAL RESULT
# ====================================================================
if [ "$OVERALL_PASSED" = true ]; then
    log "------------------------------------------------------"
    log "✅ Assemblage Setup PASSED."
    log "The 'house' is provisioned, secure, and ready for work."
    exit 0 # Return success code
else
    error "------------------------------------------------------"
    error "❌ Assemblage Setup FAILED."
    error "The 'house' is not ready. Please fix the errors above (e.g., install missing deps)."
    exit 1 # Return failure code
fi
