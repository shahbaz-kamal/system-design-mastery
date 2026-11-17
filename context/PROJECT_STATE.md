# Project State — updated at the end of each agent session

## Study scope
- Book: *Designing Data-Intensive Applications*, **second edition (2026)**, Martin Kleppmann and Chris Riccomini.
- Supplement: Stack Learner System Design & Application Architecture Workshop.
- Prior learning: Chapter 1 integrated 75-question handbook was created and reviewed. The user has read Chapters 1 and 2; this does **not** automatically authorize authoring any specific chapter.
- **Current requested chapter:** Not selected in this local starter. Set when the user invokes `@start_here.md for Chapter X`.
- **Current active deliverable:** None until user request; fill after kickoff.

## Stable decisions
- Teaching-first handbook, interview preparation second.
- DDIA chapter and section order; verified course material integrated in the appropriate places.
- Elaborative, self-contained section explanations and worked examples; concise but complete Q&A without excessive repetition.
- Explain important terms, component responsibilities, data flow, real-world scenarios and trade-offs.
- Complete follow-up Q&A; do not enforce a fixed question count.
- Original Markdown and diagram sources retained, DOCX generated/validated/rendered.
- User normally adds source files before starting a chapter.

## Session log (agent fills)
- Requested chapter: ____
- Verified source files: ____
- User answers / material decisions: ____
- Sections completed: ____
- DOCX build / validation / visual review: ____
- Remaining gaps / next step: ____

## Chapter 2 implementation session ? 2026-11-17
- User approved complete Chapter 2 handbook with matching verified course topics.
- Question estimate: 25?35 main, including 10?15 interview-style, with answered follow-ups.
- Actual PDF and course files exist; inventory's NOT COPIED entries are stale.
- Extracted private book text locally to output/ddia-source-local.txt using Git pdftotext; no upload.
- Verified chapter opening, case-study opening, and TOC subsection order. Outline replaced with evidence-based draft.
- Full handbook, diagrams, DOCX, validation, and visual review remain unfinished.
- Python lacks pypdf/python-docx; pip network access denied. Installed Git pdftotext provides a working extraction fallback; extraction emitted stream warnings requiring page-specific checking.
- Resume with full Chapter 2 source reading and precise lecture mappings before authoring.

## Chapter 2 authored and exported ? 2026-11-17
- Full chapter draft: approximately 7,300 words; six teaching groups preserving book subsection order.
- 30 main questions, 12 explicitly interview-style; 30 answered follow-ups. Answers are compact and often shorter than preferred ranges; expand if greater practice depth is desired.
- Three original editable diagrams, styled DOCX, and LibreOffice review PDF generated.
- Distinct blue shaded question headings, teal follow-up labels, italic source notes, coordinated headings, and colored tables.
- Structural checks passed using Python standard-library OOXML inspection; original validate.py remains unavailable due to missing python-docx.
- Representative rendered pages inspected; first review revealed table sizing issues, addressed with explicit table and cell widths before rebuild.
- Rebuild: scripts/build.py then scripts/polish_chapter_docx.py OUTPUT.docx. Use discovered tool paths; PDF export needs isolated local LibreOffice profile.

Final layout revision: glossary and mistakes converted to labeled paragraphs after table rendering remained poor. Final PDF is 25 pages; final structural checks passed. Earlier table-layout completion note is superseded.
