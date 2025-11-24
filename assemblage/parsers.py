"""
assemblage.parsers

Provides reusable parsing functions for Assemblage's Markdown-based documents.
"""

import re


def parse_adr(adr_content: str) -> dict:
    """
    Parses the content of an ADR Markdown file to extract key sections.
    """
    parsed_data = {"title": "", "context": "", "decision": "", "consequences": ""}

    # Extract Title (assumes the first H1 is the title)
    title_match = re.search(r"^#\s*(.*)", adr_content, re.MULTILINE)
    if title_match:
        parsed_data["title"] = title_match.group(1).strip()

    def extract_section(section_name: str, content: str) -> str:
        """A generic function to extract content between two H2 headings."""
        # This pattern looks for a section heading and captures everything
        # until the next H2 heading or the end of the string.
        pattern = re.compile(
            rf"##\s*{re.escape(section_name)}.*?\n(.*?)(?=\n##|\Z)", re.DOTALL
        )
        match = pattern.search(content)
        if match:
            return match.group(1).strip()
        return ""

    parsed_data["context"] = extract_section("1. Context", adr_content)
    parsed_data["decision"] = extract_section("2. Decision", adr_content)
    parsed_data["consequences"] = extract_section("4. Consequences", adr_content)

    return parsed_data
