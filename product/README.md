# 📦 product/ (The "Source Material")

This directory is a core "Anchor" in our "Assemblage." It contains the "Source Material" that defines the "Product" (the "furniture") we are building.

This folder is **NOT** for "Assemblage" (the "house") files. It exists to enforce our "clean separation."

## Purpose & Workflow

This directory is the "output" of the **"Explorer" Workbench** and the "input" for the **"Architect" Workbench**.

It represents the formal "translation" of the strategic "Why" (defined in `decisions/`) into the tangible "What" (the "Product" definition).

The "conveyor belt" workflow is:
1.  **Explorer:** Has a "conversation" (from `ideas/`) and formalizes a "Why" (in `decisions/`).
2.  **Explorer:** Creates the "Source Material" here (in `product/`) to define the "What" that fulfills the "Why."
3.  **Architect:** Reads the "Source Material" from this folder (as tasked by a `backlog/` item) to create the technical "How" (the "Blueprint" in `specs/`).

## Contents

This directory contains the formal definition of the "Product," broken down into key "Anchor" files:

* **`PRODUCT_VISION.md`**: The high-level strategic vision for the "Product." (This file will be created by the "Explorer" workbench, informed by the Vision Owner).
* **`FEATURES.md`**: A list of high-level features the "Product" must have.
* **`USER_STORIES.md`**: Specific "As a user..." stories that define behavior.
* **`NON_FUNCTIONAL.md`**: Definitions for performance, security, etc.
* **`TEMPLATE.md`**: The template for creating new "Product" definition files.

---
**System Owner (AI):** You (as the "Explorer") write to this folder. You (as the "Architect") read from this folder.
**Vision Owner (Human):** You review the files in this folder to ensure the "What" (the "Source Material") aligns with your "Why" (your Vision).
