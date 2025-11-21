"""
assemblage.commands.observe

Logic for the 'observe' command.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _get_assemblage_status():
    """Gets the current version."""
    print("INFO: Getting Assemblage version...")
    version_file = Path("ASSEMBLAGE.version")
    status = "✅ STABLE"
    status_json = "STABLE"
    version = version_file.read_text().strip()
    return {"status": status, "status_json": status_json, "version": version}


def _get_conveyor_belt_metrics():
    """Counts items in the ideas, backlog, and specs directories."""
    print("INFO: Gathering conveyor belt metrics...")
    ideas_count = len(list(Path("ideas").glob("*.md")))
    backlog_count = len(list(Path("backlog/items").glob("*.md")))
    specs_count = len(list(Path("specs").glob("* ")))
    return {"ideas": ideas_count, "backlog": backlog_count, "specs": specs_count}


def _get_recent_activity(limit=5):
    """Gets the most recent Git log entries."""
    print("INFO: Fetching recent activity from Git...")
    command = ["git", "log", f"-n{limit}", "--pretty=format:%h|%s"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    log_entries = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        hash_val, message = line.split("|", 1)
        log_entries.append({"hash": hash_val, "message": message})
    return log_entries


def run(args):
    """Main function to orchestrate the dashboard generation."""
    print("--- Control Plane: Executing 'observe' ---")
    output_md = Path("STATUS.md")
    output_json = Path("status.json")

    try:
        assemblage_health = _get_assemblage_status()
        conveyor_belt = _get_conveyor_belt_metrics()
        recent_activity = _get_recent_activity()

        final_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assemblage_health": assemblage_health,
            "project_progress": {
                "conveyor_belt": conveyor_belt,
                "recent_activity": recent_activity,
            },
        }

        print(f"INFO: Generating {output_json}...")
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2)

        print(f"INFO: Generating {output_md}...")
        md_content = f"""# Assemblage Status Report

*Generated: {final_data['generated_at']}*

---

## 🏛️ Assemblage Health ("The House")

- **Integrity Status:** {final_data['assemblage_health']['status']}
- **Framework Version:** {final_data['assemblage_health']['version']}

---

## 🛋️ Project Progress ("The Furniture")

### "Conveyor Belt" Funnel
- **💡 Ideas:** {final_data['project_progress']['conveyor_belt']['ideas']}
- **📋 Backlog:** {final_data['project_progress']['conveyor_belt']['backlog']}
- **📐 Specs:** {final_data['project_progress']['conveyor_belt']['specs']}

### Recent Activity
"""
        for entry in final_data["project_progress"]["recent_activity"]:
            md_content += f"- `{entry['hash']}`: {entry['message']}\n"
        output_md.write_text(md_content, encoding="utf-8")

        print("INFO: Dashboard generation complete.")
        print(f"INFO: View the report: {output_md}")
        sys.exit(0)

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"ERROR: A required file or command failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
