"""
stager.py

The core logic for the Context Staging System. This module handles the
creation of new process documents by assembling context from parent documents
and generating a "Task Briefing" for the AI.
"""

import re
from datetime import date
from pathlib import Path

from assemblage import parsers


class BaseStage:
    """Abstract base class for a stage in the document workflow."""

    def __init__(self, title, from_id=None):
        if not title:
            raise ValueError("Title cannot be empty.")
        self.title = title
        self.from_id = from_id
        self.context = {}

    def run(self):
        """Orchestrates the staging process."""
        self.context = self.assemble_context()
        template = self._load_template()
        rendered_content = self._render(template, self.context)
        new_path = self._provision_file(rendered_content)
        briefing = self._generate_briefing(new_path)
        return briefing

    def assemble_context(self):
        """Abstract method to gather context from source documents."""
        raise NotImplementedError

    def _get_template_path(self):
        """Abstract method to define the path to the template file."""
        raise NotImplementedError

    def _get_target_dir(self):
        """Abstract method to define the output directory."""
        raise NotImplementedError

    def _load_template(self):
        """Loads the raw template file."""
        return self._get_template_path().read_text(encoding="utf-8")

    def _render(self, template, context):
        """Replaces placeholders in the template with context values."""
        content = template
        for key, value in context.items():
            content = content.replace(f"{{{key}}}", str(value))
        return content

    def _get_next_id(self):
        """Finds the next sequential ID in the target directory."""
        target_dir = self._get_target_dir()
        target_dir.mkdir(exist_ok=True)
        existing_ids = [
            int(f.name.split("-")[0])
            for f in target_dir.glob("*-*")
            if f.name.split("-")[0].isdigit()
        ]
        return max(existing_ids) + 1 if existing_ids else 1

    def _provision_file(self, content):
        """Saves the rendered content to a new file with the correct name."""
        next_id = self._get_next_id()
        # Update the instance context directly
        self.context["ITEM_ID"] = next_id
        self.context["ITEM_ID_PADDED"] = f"{next_id:03d}"

        slug = self.title.lower().replace(" ", "-")
        self.context["SLUG"] = slug

        # Re-render to include the new ID-based context
        content = self._render(content, self.context)

        file_name = f"{self.context['ITEM_ID_PADDED']}-{slug}.md"
        new_path = self._get_target_dir() / file_name

        print(f"INFO: Provisioning new file at '{new_path}'...")
        new_path.write_text(content, encoding="utf-8")
        return new_path

    def _generate_briefing(self, new_path):
        """Generates the final "Task Briefing" for the AI."""
        briefing = f"""
## CONTEXT STAGE: Complete

**Objective:** {self.title}

**Synthesized Context:**
"""
        for key, value in self.context.items():
            briefing += f"- **{key.upper()}:** {value}\n"

        briefing += f"""

**Your Task:**
A new document has been provisioned for you. Please review the synthesized
context above and begin your work in the new file:
`{new_path}`
"""
        return briefing


class AdrToItemStage(BaseStage):
    """Stage handler for creating a Backlog Item from an ADR."""

    def _get_template_path(self):
        # We now use the main template, not a separate one
        return Path("backlog/items/TEMPLATE.md")

    def _get_target_dir(self):
        return Path("backlog/items")

    def _render(self, template, context):
        """Overrides base render to handle multiline content better."""
        content = template
        # Basic placeholders
        content = content.replace("{{NUMBER}}", context.get("ITEM_ID_PADDED", "XXX"))
        content = content.replace("{{DATE}}", context.get("DATE", ""))
        content = content.replace("[Short Title]", self.title)
        content = content.replace("ADR-{{ADR_NUMBER}}", f"ADR-{self.from_id:03d}")
        content = content.replace("{{SPEC_NAME}}", context.get("SLUG", "XXX-spec-name"))

        # Injected content
        content = content.replace("{{WHY_SUMMARY}}", context.get("WHY_SUMMARY", ""))
        content = content.replace(
            "{{SUGGESTED_ACCEPTANCE_CRITERIA}}",
            context.get("SUGGESTED_ACCEPTANCE_CRITERIA", ""),
        )

        return content

    def assemble_context(self):
        """Gathers and synthesizes context from the source ADR."""
        if not self.from_id:
            raise ValueError(
                "Creating an 'item' requires a source ADR ID via --from-adr."
            )

        # Find the ADR file
        adr_dir = Path("decisions")
        adr_files = list(adr_dir.glob(f"{self.from_id:03d}-*.md"))
        if not adr_files:
            raise FileNotFoundError(f"Could not find ADR with ID '{self.from_id:03d}'.")

        adr_path = adr_files[0]
        adr_content = adr_path.read_text(encoding="utf-8")

        # Use the new parser
        parsed_adr = parsers.parse_adr(adr_content)

        # Create the "Why" summary
        why_summary = (
            f"This item implements the decision from **{parsed_adr['title']}**.\n\n"
            f"**Context:** {parsed_adr['context'][:250]}...\n\n"
            f"**Decision:** {parsed_adr['decision'][:350]}..."
        )

        # Suggest acceptance criteria from decision and consequences
        suggestions = []
        decision_lines = parsed_adr["decision"].split("\n")
        consequences_lines = parsed_adr["consequences"].split("\n")

        for line in decision_lines + consequences_lines:
            line = line.strip()
            if line.startswith(("- ", "* ", "1. ", "2. ", "3. ")):
                # Clean up the line
                cleaned_line = re.sub(r"^[*-]\s*|^(\d+\.)\s*", "", line)
                suggestions.append(f"- [ ] {cleaned_line}")

        suggested_criteria = "\n".join(suggestions) if suggestions else "- [ ] TBD"

        return {
            "TITLE": self.title,
            "DATE": date.today().isoformat(),
            "WHY_SUMMARY": why_summary,
            "SUGGESTED_ACCEPTANCE_CRITERIA": suggested_criteria,
        }


def get_stage_handler(doc_type, title, from_adr=None, from_item=None):
    """Factory function to get the correct stage handler."""
    if doc_type == "item":
        if from_adr:
            return AdrToItemStage(title, from_id=int(from_adr))
        else:
            raise ValueError("Creating an 'item' requires a source ADR via --from-adr.")
    # Add other types like 'spec' here in the future
    # elif doc_type == "spec":
    #     if from_item:
    #         return ItemToSpecStage(title, from_id=int(from_item))
    #     ...
    else:
        raise ValueError(f"Unknown document type '{doc_type}'.")
