# START HERE — Chapter-independent agent entry point

**User invocation:** `@start_here.md for Chapter X` (replace X with any DDIA chapter number from 1 to 14). This file is a reusable instruction, **not a chapter-specific prompt**.

## Phase 1 — Inspect and ask the user
1. Read `AGENTS.md`, `README.md`, and all `context/*.md` files.
2. Parse the requested chapter number X. If unspecified, ask for the number. Do not silently assume Chapter 2.
3. Inspect `sources/books/`, `sources/lectures/`, `sources/transcripts/`, `sources/references/`. Record which files are accessible and actually relevant to chapter X. The user normally adds files before invocation; **verify rather than ask them to re-upload existing files**.
4. Inspect any existing `chapters/chapter-XX/` files. Don't overwrite authored material.
5. Confirm actual printed chapter heading/section order from the provided DDIA edition, and course slide matches from inspected evidence. Note unavailable evidence without guessing.
6. **Ask a short set of relevant questions before bulk authoring**, only where not already resolved: e.g. whether to create the complete chapter or a few sections, whether to include only available verified lectures, whether to preserve/modify existing work, or any important uncertainty. Offer sensible defaults and avoid an unnecessary questionnaire. If sources are complete and all preferences are known, say what you'll do and proceed.

## Phase 2 — Plan
7. Chapter folders 1–14 are already included with title files and draft templates. Verify the selected chapter's `CHAPTER_INFO.md`; initialize any missing files or diagram directory without overwriting work: `python scripts/new_chapter.py X` (or `py scripts/new_chapter.py X` on Windows). This copies templates without overwriting files.
8. Draft/update `chapters/chapter-XX/outline.md` in actual book order, mapping verified course content to corresponding sections; summarize the plan briefly to the user.
9. Choose a question count based on **learning coverage**, not an arbitrary target. Include conceptual checks, practical cases, trade-offs and interview follow-ups.

## Phase 3 — Write the educational handbook
10. Write each section in `chapters/chapter-XX/study-guide.md`: glossary/prerequisites → substantial but focused concept lesson → components and full data flow → worked real-life example/diagram → trade-offs/recap → grouped questions with complete, shorter model answers and fully answered follow-ups.
11. Use source references carefully. Explain needed technical terms, but avoid repeating long tutorials inside each answer. Create diagrams as source-controlled `.dot` files under `diagrams/chapter-XX/` and reference rendered PNGs in Markdown.
12. Finish with a chapter glossary, mistakes-to-avoid section, recap and revision exercises.

## Phase 4 — Produce and check
13. Create the Word reference style if missing: `.\.venv\Scripts\python.exe scripts/create_reference.py` (PowerShell) or `python scripts/create_reference.py`.
14. Build: `python scripts/build.py chapters/chapter-XX/study-guide.md output/DDIA-Chapter-XX.docx`.
15. Validate: `python scripts/validate.py chapters/chapter-XX/study-guide.md output/DDIA-Chapter-XX.docx`.
16. Render to PDF using LibreOffice when available; **visually inspect** representative pages and fix broken diagrams, overflowing tables, code blocks, navigation and whitespace. Do not describe untested work as tested.
17. Update `context/PROJECT_STATE.md` with what was completed, what needs further work and any source gaps.
18. Give the user the resulting file path and a brief account of coverage and verification.

**Memory aid:** Revisit the source, teach first, ask targeted questions, author one chapter at a time, validate before delivery.
