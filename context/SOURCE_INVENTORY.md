# Source inventory — verify actual files for each requested chapter

> The user normally adds PDFs, PPTX slides and transcripts before invoking `@start_here.md for Chapter X`. This table is a log, **not evidence** that any file was actually inspected. Update entries to match filesystem contents and source usage.

| Source | Local path | Availability | Verified details / applicable chapters |
|---|---|---|---|
| DDIA 2e (2026) | `sources/books/` | NOT COPIED | Confirm book edition and printed pages |
| Stack Learner lecture slide decks | `sources/lectures/` | NOT COPIED | Confirm lecture number and slide topics before mapping |
| Optional lecture transcripts | `sources/transcripts/` | OPTIONAL | Verify contents before referencing |
| Prior completed handbook / style sample | `sources/references/` | OPTIONAL | Reference for visual design, not authority for DDIA quotations |

## On each chapter kickoff
- List the actual files and select verified sources for chapter X.
- Check exact edition and chapter in the PDF; confirm printed page number separately from PDF viewer page number.
- Open slide deck(s) and map only the topics actually present.
- Flag missing sources or unreadable files without inventing coverage.
- Don't ask for files already present in the local project.

## Verified Chapter 2 sources ? 2026-11-17
- Book PDF present under sources/books; inspected Chapter 2 opening and body text, printed pp. 33?56 via local Git pdftotext extraction. Extraction emitted warnings elsewhere; no claim of complete whole-book extraction.
- Lecture 2 Application Performance: physical slides 6, 14?21, 27?34 inspected and integrated selectively.
- Lecture 5 System Reliability: physical slides 7?14, 22?24, 30, 34?44 inspected and integrated selectively.
- Prior Chapter 1 DOCX opening and contents inspected as presentation reference.
- Other decks are present; security images are present but not used or claimed inspected for this handbook. No transcripts discovered.
- Earlier NOT COPIED availability entries above are superseded by this inspection log.
