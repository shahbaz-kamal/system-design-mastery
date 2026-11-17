# Reproducible chapter-independent workflow

## Start
1. User places owned source materials in `sources/` and invokes `@start_here.md for Chapter X`.
2. Agent follows root `start_here.md`: reads shared context, checks actual sources and existing chapter progress, asks only missing consequential questions, and verifies book/chapter structure.
3. Run `python scripts/new_chapter.py X` if `chapters/chapter-XX/` does not exist. Do **not** overwrite existing authored files.

## Author
1. Draft `chapters/chapter-XX/outline.md` in verified DDIA topic order with course mappings and references.
2. Write `chapters/chapter-XX/study-guide.md`: grouped lessons first; practical examples and source references; questions/follow-ups after each group.
3. Use headings `### Q01. ...`, `**Model answer:**`, `**Follow-up:**` and `**Follow-up answer:**` for machine checks. Adjust numbers sequentially across the chapter.
4. Create editable diagrams as `diagrams/chapter-XX/*.dot`. Link rendered images as `![Example](diagrams/output/chapter-XX/figure.png)`; build script resolves paths relative to project root.
5. Add recap, glossary, mistakes and self-test at chapter end.

## Build/verify (replace XX with 2-digit number)
```powershell
.\.venv\Scripts\python.exe scripts/create_reference.py
.\.venv\Scripts\python.exe scripts/build.py chapters/chapter-XX/study-guide.md output/DDIA-Chapter-XX.docx
.\.venv\Scripts\python.exe scripts/validate.py chapters/chapter-XX/study-guide.md output/DDIA-Chapter-XX.docx
.\scripts\render_review.ps1 -Docx output/DDIA-Chapter-XX.docx
```
The initial template **must fail** final content validation until finished. The validator checks some mechanical issues only; the agent must visually inspect pages and check source fidelity and teaching clarity.

## Completion and handoff
- Update `context/PROJECT_STATE.md` with accurate chapter progress.
- Keep canonical Markdown and `.dot` files; generated DOCX is output only.
- Never claim inspection, execution or successful validation without actually doing it.
- Keep user's copyrighted/private source materials local and out of public version control.
