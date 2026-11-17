# System Design Mastery — Local Multi-Agent Learning Project

**A reusable, chapter-independent study workspace for DDIA 2nd edition (2026) + Stack Learner.** Open the same folder with Codex CLI, Claude Code, Cursor, Copilot or another coding agent. Your agents produce **learning-first, self-contained study guides** with interview-style practice, original diagrams and professionally formatted Word documents.

> **One README only:** This root `README.md` is the complete setup and daily-use manual. Other Markdown files (`AGENTS.md`, `start_here.md`, and `context/*.md`) are agent rules and project context—not duplicate setup guides.

**Start any chapter by saying:**

> `@start_here.md for Chapter 3`

Replace **3** with any chapter number **1–14**. You can also say: `Read start_here.md and start Chapter 3.` The `@` filename mention works only in agents that support file mentions; for others, the second instruction is reliable.

The agent must **check the source files you have already added, read shared rules, and ask only the important unanswered kickoff questions** before large-scale authoring. Nothing in this starter is hard-coded to Chapter 2.

---

## 1. What the output should look like

The objective is **to learn and remember system design**, not merely to memorize interview answers. Each book-ordered group should contain:

1. **Focused concept lesson:** definitions of important terms; why the problem exists; where components run; complete request/data flow; real-world example, advantages, disadvantages and failure modes.
2. **Diagram and worked example:** original Graphviz diagrams, SQL or Node.js/Express/TypeScript when useful. Explain each component and arrow.
3. **Questions immediately after the relevant lesson:** concept checks, practical design questions and interview questions. Answers should be complete but **shorter than a standalone tutorial** because the lesson already covers depth.
4. **Fully answered follow-ups:** test assumptions, constraints, and failure handling; no empty follow-ups.
5. **Mini-recap and revision prompts:** three to five points worth remembering, plus short practice exercises.

**Recommended depth, not a mandatory word count:** conceptual lessons ~300–1,200 words based on complexity; regular answers ~150–300 words; harder answers longer when needed. Avoid unexplained jargon and duplicated lengthy introductions in every Q&A. Follow `context/STUDY_RULES.md`.

---

## 2. Project folders and what they're for

```text
system-design-mastery/
├── README.md                          # Setup and everyday use (this file)
├── start_here.md                      # Any-chapter kickoff: @start_here.md for Chapter X
├── AGENTS.md                          # Primary rules shared by all agents
├── CLAUDE.md                          # Claude Code entry point; references AGENTS.md
├── requirements.txt                   # Python packages used by scripts
├── .gitignore                         # Prevents uploading private sources and builds
├── .cursor/rules/study-guide.mdc       # Cursor guidance
├── .github/copilot-instructions.md   # GitHub Copilot guidance
├── context/
│   ├── STUDY_RULES.md                 # How deeply to teach; question length
│   ├── SOURCE_POLICY.md               # Book/lecture verification and attribution
│   ├── SOURCE_INVENTORY.md            # Files actually present and inspected
│   ├── PROJECT_STATE.md               # Active chapter, progress, decisions
│   └── WORKFLOW.md                    # Draft, diagram, build, validate, review
├── sources/
│   ├── books/                          # Your own DDIA PDF
│   ├── lectures/                       # Your Stack Learner PPTX slides
│   ├── transcripts/                    # Optional lecture transcripts
│   └── references/                     # Optional previous Chapter 1 handbook
├── chapters/
│   ├── _template/                      # Reusable outline and handbook skeleton
│   ├── chapter-01/                     # Trade-Offs in Data Systems Architecture
│   ├── chapter-02/                     # Defining Nonfunctional Requirements
│   ├── chapter-03/                     # Data Models and Query Languages
│   ├── chapter-04/                     # Storage and Retrieval
│   ├── chapter-05/                     # Encoding and Evolution
│   ├── chapter-06/                     # Replication
│   ├── chapter-07/                     # Sharding
│   ├── chapter-08/                     # Transactions
│   ├── chapter-09/                     # The Trouble with Distributed Systems
│   ├── chapter-10/                     # Consistency and Consensus
│   ├── chapter-11/                     # Batch Processing
│   ├── chapter-12/                     # Stream Processing
│   ├── chapter-13/                     # A Philosophy of Streaming Systems
│   └── chapter-14/                     # Doing the Right Thing
│       # Each chapter-XX/ contains CHAPTER_INFO.md, outline.md, study-guide.md
├── diagrams/
│   ├── request_flow.dot                # Sample original editable diagram
│   ├── chapter-XX/                     # Per-chapter .dot diagram source
│   └── output/                         # Generated diagram PNG files
├── scripts/
│   ├── new_chapter.py                  # Creates chapter-XX without overwriting work
│   ├── create_reference.py             # Creates a Word design template
│   ├── build.py                        # Renders .dot images + converts MD to DOCX
│   ├── validate.py                     # Checks Q&A and DOCX structure
│   └── render_review.ps1               # Converts DOCX to PDF for visual review
├── prompts/START_HERE.md              # Backward-compatible pointer to root entry
├── templates/reference.docx            # Generated Word styling reference
└── output/                             # Final DOCX files and review PDFs
```

**Keep each type of file in its designated place:** sources are the evidence; `chapters/` and `.dot` files are editable originals; `output/` is generated; `context/` preserves learning rules and progress between sessions.

---

## 3. One-time setup on Windows PowerShell

### 3.1 Extract the ZIP

Extract the downloaded ZIP and move its **entire project folder** to a location you choose, for example:

```text
D:\Projects\system-design-mastery
```

Open **PowerShell** in the project root:

```powershell
cd "D:\Projects\system-design-mastery"
Get-ChildItem -Force
```

You should see `README.md`, `AGENTS.md`, `start_here.md`, `scripts`, `chapters`, and `sources`.

### 3.2 Install the three document tools

Open PowerShell and run:

```powershell
winget install --id JohnMacFarlane.Pandoc -e
winget install --id Graphviz.Graphviz -e
winget install --id TheDocumentFoundation.LibreOffice -e
```

**What does each program do?**

| Program | What it is | What it does in this project | Example |
|---|---|---|---|
| **Pandoc** | A document format converter | Converts the chapter's Markdown (`.md`) into a formatted Word file (`.docx`), carrying headings, tables, code and embedded images | `study-guide.md` → `DDIA-Chapter-03.docx` |
| **Graphviz** | A diagram engine for graph/flow descriptions | Converts editable `.dot` text diagrams into PNG images that Pandoc can embed in Word | `replication.dot` → `replication.png` |
| **LibreOffice** | An office suite (alternative to MS Word) | Opens DOCX and exports it to PDF **without manually opening Word**, allowing page-by-page layout review | `DDIA-Chapter-03.docx` → review PDF |

**Which are needed?** Pandoc and Graphviz are needed for the included build pipeline; LibreOffice is highly recommended for PDF review but is not needed to create a DOCX. LibreOffice is not used as your primary writing tool.

**Restart PowerShell after installation**, then verify:

```powershell
pandoc --version
dot -V
soffice --version
```

If `soffice` is not found but LibreOffice installed successfully, try:

```powershell
& "C:\Program Files\LibreOffice\program\soffice.exe" --version
```

If `winget` is missing, install/update **App Installer** in Windows, or use the official program installers. If a command is missing after install, verify Windows `PATH` and reopen PowerShell. If you have Microsoft Word, you can use its PDF export instead of LibreOffice for review.

### 3.3 Install Python

Check:

```powershell
python --version
```

If not installed, you can install a recent Python version (3.11+ recommended) using:

```powershell
winget install --id Python.Python.3.13 -e
```

Restart PowerShell and check again. Some Windows installations use `py --version` and `py -3 -m venv .venv` instead of `python`.

**What does Python do here?** Python runs the project scripts that create chapter folders, apply Word styles, render diagrams, and validate completed documents. Python is separate from the three installer programs above.

### 3.4 Create a Python virtual environment and install libraries

Run the following **from the project root**:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

A **virtual environment** (`.venv`) is an isolated copy of Python's package environment for this project. It prevents conflicts with Python libraries used by your other projects.

`requirements.txt` installs **python-docx**, a Python library that creates/styles Word files and checks their structure. Pandoc generates the main document; python-docx supplies reference styling and programmatic inspection.

Verify:

```powershell
.\.venv\Scripts\python.exe -c "import docx; print('python-docx ready')"
```

You do **not** need to activate the virtual environment. Calling `.\.venv\Scripts\python.exe` directly also avoids PowerShell script-execution-policy errors.

---

## 4. Add your sources **before** starting a chapter

Use File Explorer to copy your own materials into:

- `sources/books/`: DDIA **2nd edition (2026)** PDF.
- `sources/lectures/`: Stack Learner PowerPoint decks; include lecture number in filename where possible.
- `sources/transcripts/`: Optional transcripts or lecture notes.
- `sources/references/`: Optional completed Chapter 1 DOCX for design consistency.

You can name files sensibly; the agent must **list and read actual files**, not assume specific names. When using a new agent, ask it to update `context/SOURCE_INVENTORY.md` after inspection.

**Do not publish copyrighted PDFs, private lecture decks, secrets, or personal documents in a public Git repository.** The provided `.gitignore` excludes the source folders and generated outputs by default.

---

## 5. Start a chapter with any agent

### Codex CLI

```powershell
cd "D:\Projects\system-design-mastery"
codex
```

### Claude Code

```powershell
cd "D:\Projects\system-design-mastery"
claude
```

### Cursor, OpenCode, or another agent

Open the same project folder. If the tool supports file mentions, use `@start_here.md for Chapter X`. Otherwise type:

```text
Read root start_here.md and AGENTS.md. Begin Chapter X following the rules.
```

**Example kickoff:**

```text
@start_here.md for Chapter 7
```

The agent should:

1. Read the shared rules and current progress.
2. Inspect your already-added PDF, slides, transcripts and any existing chapter files.
3. Verify Chapter 7's real section headings and source coverage.
4. **Ask only unresolved, relevant questions**, such as whether you want a complete chapter or a targeted section, or whether to integrate a particular verified lecture. Existing preferences should be reused.
5. Produce a book-ordered outline and then the learning guide once essential choices are settled.
6. Create diagrams, build a Word document, validate, visually inspect, and update progress.

**Don't re-upload files when switching agents:** As long as you open the same local folder, all project files remain available to the next agent. Agent-specific conversation history may *not* carry over; `context/PROJECT_STATE.md` exists to bridge that gap.

---

## 6. Day-to-day usage

### A. First day working on a new chapter

1. Put new source files into `sources/`.
2. Open the project folder with Codex or Claude.
3. Send `@start_here.md for Chapter X` (or the plain-text alternative).
4. Answer the agent's short kickoff questions **once**.
5. Review the proposed section outline and ensure the verified course integration makes sense.
6. Let the agent author lessons **section by section**, including Q&A, definitions, examples and diagrams.
7. Ask it to generate the DOCX, run validation, and review the rendered pages.

### B. Continue an unfinished chapter tomorrow

Open the same folder with either agent and say:

```text
Read AGENTS.md and context/PROJECT_STATE.md. Continue Chapter 7
from the last verified completed section. Check existing source and
Markdown files, preserve previous work, and update the state when done.
```

All 14 chapter workspaces are already present. The agent should reuse existing `chapters/chapter-07/` files rather than starting from scratch.

### C. Revise a section you didn't understand

```text
Read the Chapter 7 study guide. Expand the lesson on [topic] with
clear definitions, a complete Node.js/Express data-flow example and
one original diagram. Keep the Q&A concise and avoid repeating the
whole explanation under every question. Rebuild and validate DOCX.
```

### D. Add lecture slides later

```text
I added a new lecture to sources/lectures/. Inspect its actual content,
identify which Chapter 7 sections it supports, and integrate only
verified relevant concepts without disturbing the book order.
Update SOURCE_INVENTORY.md and rebuild the handbook.
```

### E. Generate only the Word document after Markdown revisions

For Chapter **7** (use a different two-digit chapter number for other chapters):

```powershell
.\.venv\Scripts\python.exe scripts/create_reference.py
.\.venv\Scripts\python.exe scripts/build.py chapters/chapter-07/study-guide.md output/DDIA-Chapter-07.docx
.\.venv\Scripts\python.exe scripts/validate.py chapters/chapter-07/study-guide.md output/DDIA-Chapter-07.docx
.\scripts\render_review.ps1 -Docx output/DDIA-Chapter-07.docx
```

**Note:** The initial chapter template is **not** a completed guide. Do not expect it to pass final validation until the agent replaces all placeholders and writes real lessons and answers.

### F. Start Chapter X without an AI agent (optional)

You can create empty working files with:

```powershell
.\.venv\Scripts\python.exe scripts/new_chapter.py 7
```

All 14 chapter folders (Chapter 1 through Chapter 14) are **pre-created** in this ZIP. Each contains `CHAPTER_INFO.md` with the chapter title plus `outline.md` and `study-guide.md` draft templates. The script makes any missing files or diagram directories and **does not overwrite existing work**. These draft files are not completed study material.

### G. Switch between Codex and Claude

1. Finish or save current changes.
2. Have the current agent update `context/PROJECT_STATE.md` with completed sections and unresolved questions.
3. Close that agent (avoid both modifying the same file simultaneously).
4. Launch the next agent from the same project root.
5. Ask it to read `AGENTS.md` and `PROJECT_STATE.md` before resuming.

You can optionally initialize Git for version history:

```powershell
git init
git add .
git commit -m "Initial reusable study workspace"
```

Inspect `git status` before committing. The provided `.gitignore` is designed to exclude source PDFs/slides and generated outputs; maintain those files locally or in your own private backup.

---

## 7. How the DOCX pipeline works

```text
Your PDF/PPTX sources
        ↓  agent verifies and studies
chapters/chapter-XX/study-guide.md     diagrams/chapter-XX/*.dot
        │                                  │
        │                                  ↓ Graphviz
        │                          diagrams/output/chapter-XX/*.png
        └──────────────┬───────────────────┘
                       ↓ Pandoc + reference.docx
             output/DDIA-Chapter-XX.docx
                       ↓ python-docx checks
                validation results
                       ↓ LibreOffice (or Word)
                  PDF layout review
```

The agent is responsible for both **technical correctness** and **teaching quality**. Automated validation checks only basic completeness and structure; it cannot verify the book's claims or whether an explanation is easy to understand. Visual review must catch missing images, overlapping tables, unreadable code and bad page breaks.

---

## 8. Troubleshooting

| Problem | What to check |
|---|---|
| `winget` not recognized | Windows App Installer or official installers |
| `pandoc` not recognized | Install Pandoc; restart shell; verify PATH |
| `dot` not recognized | Graphviz installed and its `bin` folder on PATH |
| `soffice` not recognized | LibreOffice installed; try full executable path or export PDF in Word |
| `python` not recognized | Try `py --version`; reinstall Python with PATH integration |
| PowerShell blocks Activate.ps1 | Skip activation; use `.\.venv\Scripts\python.exe` directly |
| Missing diagrams | Ensure `.dot` exists under `diagrams/`; link PNG as `diagrams/output/...` from Markdown; rebuild |
| DOCX build succeeds but looks poor | Render PDF; review pages and adjust Markdown/styles/diagram sizes |
| Validation fails on draft | Replace template placeholders and complete all model and follow-up answers |
| Agent ignores rules | Explicitly request `Read AGENTS.md, start_here.md and context/*.md`; auto-loading varies |
| Agent claims a lecture detail without evidence | Request slide/page verification from the actual local source |
| Agent starts wrong chapter | Explicitly say `@start_here.md for Chapter X`; check `PROJECT_STATE.md` |

---

## 9. File ownership and maintenance

| File | When to edit it |
|---|---|
| `AGENTS.md` | When permanent cross-agent rules change |
| `context/STUDY_RULES.md` | When explanation depth, question style or review method changes |
| `context/SOURCE_POLICY.md` | When attribution or source-verification policy changes |
| `context/SOURCE_INVENTORY.md` | Whenever source files are added, renamed or inspected |
| `context/PROJECT_STATE.md` | Every session: requested chapter, completed sections, remaining work |
| `chapters/chapter-XX/outline.md` | Planning and coverage mapping for that chapter |
| `chapters/chapter-XX/study-guide.md` | Main editable educational content |
| `diagrams/chapter-XX/*.dot` | Architecture and data-flow figure changes |
| `output/DDIA-Chapter-XX.docx` | Generated output; rebuild instead of hand-editing where possible |

**Remember:** To begin any chapter, supply the files first, then say **`@start_here.md for Chapter X`**. It should inspect what is present, ask targeted questions only when needed, teach section by section, and leave you with a validated, editable, agent-independent learning project.
