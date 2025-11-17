#!/bin/bash
#
# Core Test Runner
#
# This script finds and executes all BATS tests (`.bats` files)
# located in the `tests/` directory and its subdirectories.
#
# It uses the `bats` executable provided by our Git submodule.
#
#=======================================================================

set -e

# --- Configuration ---
# The "Anchor" to our self-contained BATS executable
BATS_EXECUTABLE="tests/libs/bats-core/bin/bats"

# The directory where tool-specific tests are located
TEST_DIR="tests/tools"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# --- Guardrails ---
if [ ! -f "$BATS_EXECUTABLE" ]; then
    echo -e "${RED}[FAIL] BATS executable not found at '$BATS_EXECUTABLE'!${NC}"
    echo -e "${BLUE}Nudge: You may need to initialize the Git submodules.${NC}"
    echo -e "${BLUE}Run: git submodule update --init --recursive${NC}"
    exit 1
fi

if [ ! -d "$TEST_DIR" ]; then
    echo -e "${RED}[FAIL] Test directory not found at '$TEST_DIR'!${NC}"
    exit 1
fi

# --- Main Logic ---
echo -e "${BLUE}Starting Core Test Runner...${NC}"
echo -e "${BLUE}Searching for '.bats' files in '$TEST_DIR'...${NC}"

# Find all .bats files and run them
# The `find` command is robust and handles spaces in filenames.
# The `+` at the end of `-exec` is more efficient than `;` as it
# passes multiple files to a single `bats` command.
find "$TEST_DIR" -name "*.bats" -exec "$BATS_EXECUTABLE" {} +