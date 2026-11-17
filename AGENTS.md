# System Design Mastery — Shared Agent Instructions

## 1. Starting any session
1. Read `README.md`, `context/PROJECT_STATE.md`, `context/STUDY_RULES.md`, `context/SOURCE_POLICY.md`, `context/SOURCE_INVENTORY.md`, and `context/WORKFLOW.md`.
2. When the user writes `@start_here.md for Chapter X` (or equivalent), read **root `start_here.md`** and follow its chapter-independent startup protocol. Treat X as the requested chapter number; never assume Chapter 2.
3. Inspect actual source files before citing them. Book and lecture contents must come from accessible originals, not filenames or previous guesses.
4. **Ask the user concise, genuinely necessary questions** at startup: scope, optional course sources or coverage, preferred outputs/changes, and any blockers. Don't repeatedly ask for preferences already settled in context. Do not begin bulk chapter writing before resolving material ambiguities.
5. Work only on the chapter/task requested. Do not automatically produce future chapters.

## 2. Pedagogy (highest priority)
- Goal: **learn system design and retain it**. Interview preparation is a useful reinforcement, not the sole deliverable.
- Write detailed **section-first concept lessons**, not a long encyclopedic answer for each interview question.
- In each lesson, define relevant prerequisites and important terms; explain what problem exists, why each component is needed, how it works, where it runs, who calls whom, and how data moves, using a tangible scenario.
- Cover realistic alternatives, assumptions, failure cases and trade-offs. Provide original diagrams/code/SQL when they genuinely clarify the flow.
- Then give a well-chosen set of conceptual, practical and interview questions, each with complete but concise non-repetitive answers. Answer every follow-up.
- Reintroduce needed concepts briefly because the learner may forget them. Be clear and professional, not patronizing.
- Use Node.js/Express/TypeScript, PostgreSQL, Redis and AWS as familiar examples when suitable; do not force these technologies into book concepts.
- See `context/STUDY_RULES.md` for preferred lengths and complete lesson shape.

## 3. Source-grounded coverage
- Primary: user's DDIA **2nd edition (2026)**, verified against actual book text and printed pages.
- Secondary: actual available Stack Learner workshop slides/transcripts, integrated within their matching DDIA sections.
- Supplementary: original implementation examples, clearly identified as such and technically checked.
- Preserve chapter subsection order. Do not invent page references, lecture topics, quotations, or claims that missing files were read.
- Use attribution near claims/lessons: `[DDIA Ch.X, section, printed pp.]`, `[Course lecture, inspected slide]`, or `[Supplementary example]`.
- Never impose an arbitrary question count. Avoid copying copyrighted book passages; paraphrase accurately.

## 4. File organization and completion
- Canonical content: `chapters/chapter-XX/outline.md` and `chapters/chapter-XX/study-guide.md`.
- Editable diagram source: `diagrams/chapter-XX/*.dot` (build script renders recursively to `diagrams/output/chapter-XX/*.png`).
- Final exports: `output/DDIA-Chapter-XX.docx` (and optional review PDF).
- Initialize a requested chapter using `python scripts/new_chapter.py X`, then read and replace templates.
- Use `python scripts/build.py chapters/chapter-XX/study-guide.md output/DDIA-Chapter-XX.docx` and `python scripts/validate.py chapters/chapter-XX/study-guide.md output/DDIA-Chapter-XX.docx`.
- Visually review rendered pages; verify tables, diagrams, headings, numbering and complete follow-ups. **A successful script run does not imply a good handbook.**
- Never label a placeholder draft complete. Update `context/PROJECT_STATE.md` with verified progress after each session.
- Don't upload local private source files or install new network services without user approval.
