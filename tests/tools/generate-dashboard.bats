#!/usr/bin/env bats
#
# BATS Test for tools/generate-dashboard.sh
#

# --- Setup ---
# BATS requires a setup function to load helpers.
setup() {
    # Load test helpers
    load '../libs/bats-assert/load.bash'
    load '../libs/bats-support/load'
}

# --- Teardown ---
# This function runs after each test.
teardown() {
    # Clean up generated files
    rm -f STATUS.md status.json
}

@test "generate-dashboard.sh creates output files" {
    run bash ../../tools/generate-dashboard.sh
    assert_success
    assert_file_exist "STATUS.md"
    assert_file_exist "status.json"
}

@test "STATUS.md contains expected content" {
    run bash ../../tools/generate-dashboard.sh
    assert_success
    assert_output --partial "Generating Project Dashboard..."
    
    run cat STATUS.md
    assert_output --partial "Assemblage Status Report"
    assert_output --partial "Assemblage Health"
    assert_output --partial "Framework Version"
    assert_output --partial "Recent Activity"
}

@test "status.json is valid JSON and contains expected content" {
    # This test requires 'jq' to be installed
    if ! command -v jq &> /dev/null; then
        skip "'jq' is not installed, skipping JSON validation test."
    fi

    run bash ../../tools/generate-dashboard.sh
    assert_success

    # Check if the file is valid JSON
    run jq -e . status.json
    assert_success

    # Check for a specific key-value pair
    run jq -e '.assemblage_health.framework_version == "1.0.0"' status.json
    assert_success
}