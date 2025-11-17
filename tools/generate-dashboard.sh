#!/bin/bash
#
# ⚙️ Utility: generate-dashboard.sh
#
# This utility script gathers status information about the Assemblage framework
# and the project's progress and outputs it into two files:
# STATUS.md (human-readable) and status.json (machine-readable).
#
#=======================================================================

# --- Configuration ---
set -e
OUTPUT_MD="STATUS.md"
OUTPUT_JSON="status.json"

# --- Colors for AI Readability ---
BLUE="\033[0;34m"
GREEN="\033[0;32m"
NC="\033[0m" # No Color

function log() {
    echo -e "${GREEN}[DASHBOARD] $1${NC}"
}

log "Generating Project Dashboard..."

# --- Phase 1: Data Gathering ---
log "Gathering data..."
GENERATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if bash ./tools/validate-assemblage.sh > /dev/null 2>&1; then
    ASSEMBLAGE_STATUS="✅ STABLE"
    ASSEMBLAGE_STATUS_JSON="STABLE"
else
    ASSEMBLAGE_STATUS="❌ UNSTABLE"
    ASSEMBLAGE_STATUS_JSON="UNSTABLE"
fi

ASSEMBLAGE_VERSION=$(cat ASSEMBLAGE.version)
IDEAS_COUNT=$(ls -1 ideas/ | wc -l | tr -d ' ')
BACKLOG_COUNT=$(ls -1 backlog/items/ | wc -l | tr -d ' ')
SPECS_COUNT=$(ls -1 specs/ | wc -l | tr -d ' ')
GIT_LOG_RAW=$(git log -n 5 --pretty=format:'%h|%s')

# --- Phase 2: JSON Generation ---
log "Generating $OUTPUT_JSON..."
{
    echo "{"
    echo "  \"generated_at\": \"$GENERATED_AT\","
    echo "  \"assemblage_health\": {"
    echo "    \"integrity_status\": \"$ASSEMBLAGE_STATUS_JSON\","
    echo "    \"framework_version\": \"$ASSEMBLAGE_VERSION\""
    echo "  },"
    echo "  \"project_progress\": {"
    echo "    \"conveyor_belt\": {"
    echo "      \"ideas\": $IDEAS_COUNT,"
    echo "      \"backlog\": $BACKLOG_COUNT,"
    echo "      \"specs\": $SPECS_COUNT"
    echo "    },"
    echo "    \"recent_activity\": ["
    FIRST=true
    while IFS='|' read -r hash message; do
        if [ "$FIRST" = false ]; then
            echo ","
        fi
        echo "      {"
        echo "        \"hash\": \"$hash\","
        echo "        \"message\": \"$message\""
        echo -n "      }"
        FIRST=false
    done <<< "$GIT_LOG_RAW"
    echo
    echo "    ]"
    echo "  }"
    echo "}"
} > "$OUTPUT_JSON"

# --- Phase 3: Markdown Generation ---
log "Generating $OUTPUT_MD..."
{
    echo "# Assemblage Status Report"
    echo ""
    echo "*Generated: $GENERATED_AT*"
    echo ""
    echo "---"
    echo ""
    echo "## 🏛️ Assemblage Health (\"The House\")"
    echo ""
    echo "- **Integrity Status:** $ASSEMBLAGE_STATUS"
    echo "- **Framework Version:** $ASSEMBLAGE_VERSION"
    echo ""
    echo "---"
    echo ""
    echo "## 🛋️ Project Progress (\"The Furniture\")"
    echo ""
    echo "### \"Conveyor Belt\" Funnel"
    echo "- **💡 Ideas:** $IDEAS_COUNT"
    echo "- **📋 Backlog:** $BACKLOG_COUNT"
    echo "- **📐 Specs:** $SPECS_COUNT"
    echo ""
    echo "### Recent Activity"
    while IFS='|' read -r hash message; do
        echo "- \`$hash\`: $message"
    done <<< "$GIT_LOG_RAW"
    echo ""
} > "$OUTPUT_MD"

log "Dashboard generation complete."
echo -e "${BLUE}View the report: cat $OUTPUT_MD${NC}"