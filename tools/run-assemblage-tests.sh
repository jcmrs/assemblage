#!/bin/bash
#
# ⚙️ Utility: run-assemblage-tests.sh
#
# This is a "House Service" for the "System Owner" (AI).
#
# PURPOSE:
# This script provides a simple, standardized command to run the
# "Utility Integrity Test" suite (the BATS tests).
#
# It acts as a stable "connect" (integration) to the core
# test runner (`tests/run-tests.sh`), ensuring that even if
# the underlying test runner changes, our "Assemblage" protocol
# (and the AI's "habit") remains the same.
#
# This script is called by the "System Owner" (AI) to fulfill
# Step 2 of the "Utility Test Protocol" Guide.
#
#=======================================================================

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# --- Main Logic ---
echo -e "${BLUE}[UTILITY] Running 'run-assemblage-tests' Utility...${NC}"
echo -e "${BLUE}This will now execute the core BATS test suite to validate all 'Utilities'.${NC}"
echo "---"

# Define the "Anchor" to the core test runner
# We are "adopting" this test runner "as-is" from the `perplex` repo.
CORE_TEST_RUNNER="tests/run-tests.sh"

# --- Guardrail: Check if the core test runner exists ---
if [ ! -f "$CORE_TEST_RUNNER" ]; then
    echo -e "${RED}[FAIL] Core test runner not found at '$CORE_TEST_RUNNER'!${NC}"
    echo -e "${RED}Cannot run "Utility Integrity Test". This is a 'How' (Platform) failure.${NC}"
    exit 1
fi

# --- Execute the core test runner ---
# We pass all arguments ($@) to the core runner, so we can
# pass flags like `--verbose` if needed.
"$CORE_TEST_RUNNER" "$@"
TEST_EXIT_CODE=$? # Capture the exit code of the test runner

# --- Report Final Status ---
echo "---"
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}[SUCCESS] All 'Utility' tests passed. The 'house' automation is stable.${NC}"
else
    echo -e "${RED}[FAIL] One or more 'Utility' tests failed.${NC}"
    echo -e "${RED}As System Owner, you MUST fix the failing tests before committing.${NC}"
fi

exit $TEST_EXIT_CODE