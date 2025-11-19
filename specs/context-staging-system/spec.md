# Specification: Context Staging System

This document provides the detailed technical blueprint for `ITEM-017`, implementing the Context Staging System as defined in `ADR-010`.

## 1. High-Level Design

The system will be composed of three main parts:
1.  **A new `stager.py` module:** This will contain the core object-oriented logic for handling different types of document creation and context assembly.
2.  **A new `guides/TEMPLATES/` directory:** This will store the raw template files for each document type.
3.  **Modifications to `control_plane.py`:** To add the `new` command and orchestrate calls to the `stager` module.

## 2. New Module: `assemblage/stager.py`

This module is the heart of the system. It will be designed in an object-oriented, extensible way.

### 2.1. Base Class: `BaseStage`
An abstract base class to define the interface for all stage handlers.
- `__init__(self, title, from_id=None)`: Constructor to hold the title of the new document and the ID of the source document (e.g., the ADR number).
- `run()`: The main public method that orchestrates the entire process:
    1. `context = self.assemble_context()`
    2. `template = self.load_template()`
    3. `rendered_content = self.render(template, context)`
    4. `new_path = self.provision_file(rendered_content)`
    5. `briefing = self.generate_briefing(context, new_path)`
    6. `return briefing`
- `assemble_context()`: Abstract method. Responsible for reading source files and extracting key information into a context dictionary.
- `provision_file()`: Concrete method. Calculates the next sequential ID for the new file, creates the file name (e.g., `018-my-new-title.md`), and writes the content to the correct directory.
- `generate_briefing()`: Concrete method. Takes the context and new file path and formats the final "Task Briefing" string for the AI.

### 2.2. Concrete Class: `AdrToItemStage(BaseStage)`
A subclass for handling the creation of a Backlog Item from an ADR.
- `assemble_context()`:
    1. Finds the source ADR file (e.g., `decisions/ADR-010...md`) using the `from_id`.
    2. Reads the ADR content.
    3. Uses regex to extract the ADR's title.
    4. Returns a context dictionary: `{"adr_link": "[ADR-010](...)", "adr_title": "...", "date": "..."}`.

### 2.3. Factory Function
- `get_stage_handler(doc_type, title, from_adr=None, from_item=None)`: A factory function that inspects the arguments and returns the appropriate handler instance (e.g., `return AdrToItemStage(title, from_adr)`).

## 3. New Templates Directory: `guides/TEMPLATES/`

- **`item_template.md`**:
    ```markdown
    # ITEM-{ITEM_ID}: {TITLE}

    **Date Created:** {DATE}
    **Status:** Ready for Architect
    **Priority:** High
    **Owner:** Architect

    ## 1. Description

    ## 2. "Why" (The Source Material)

    * **Decision (The "Why"):**
        * {ADR_LINK}
    * **Product Definition (The "What"):**
        * (To be filled in)

    ## 3. "What" (Acceptance Criteria)

    - [ ]

    ## 4. "How" (Implementation Link)

    * **Blueprint (The "How"):**
        * `specs/{ITEM_ID_PADDED}-{SLUG}/spec.md`
    ```

## 4. Control Plane Modifications (`assemblage/control_plane.py`)

- **Imports:** Add `from assemblage import stager`.
- **New Handler:** `new_command(args)`:
    1. Calls `stager.get_stage_handler()` with the parsed arguments.
    2. Calls `handler.run()` on the returned object.
    3. Prints the resulting "Task Briefing" to the console.
- **`argparse` Setup:**
    - Add the `new` sub-parser.
    - Add arguments: `--type` (required), `--title` (required), `--from-adr` (optional), `--from-item` (optional).

## 5. Test Design (`tests/test_stager.py`)

- A new test file is required.
- It will use a `pytest.fixture` to create a temporary directory containing a mock `decisions/ADR-999-mock-title.md` and a mock `guides/TEMPLATES/item_template.md`.
- **`test_adr_to_item_creation`**:
    1. Calls the `stager` logic to create a new `item` from the mock `ADR-999`.
    2. Asserts that the new file (`backlog/items/001-my-new-item.md`) is created in the correct temporary location.
    3. Reads the content of the new file and asserts that the `{ADR_LINK}` placeholder has been replaced with a correct Markdown link to `ADR-999`.
    4. Asserts that the returned "Task Briefing" string is not empty and contains the title of the source ADR.

This blueprint provides a complete and extensible design for the Builder.
