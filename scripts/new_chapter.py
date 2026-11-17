#!/usr/bin/env python3
"""Create a chapter workspace from templates without overwriting existing work."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="Initialize a DDIA chapter without overwriting files")
    parser.add_argument("chapter", type=int, help="DDIA chapter number (1–14)")
    args = parser.parse_args()
    if not 1 <= args.chapter <= 14:
        parser.error("Chapter must be between 1 and 14")
    chapter = f"{args.chapter:02d}"
    output = ROOT / "chapters" / f"chapter-{chapter}"
    output.mkdir(parents=True, exist_ok=True)
    for name in ("outline.md", "study-guide.md"):
        src = ROOT / "chapters" / "_template" / name
        dst = output / name
        if dst.exists():
            print(f"Preserved existing {dst.relative_to(ROOT)}")
            continue
        dst.write_text(src.read_text(encoding="utf-8").replace("{CHAPTER}", str(args.chapter)), encoding="utf-8")
        print(f"Created {dst.relative_to(ROOT)}")
    (ROOT / "diagrams" / f"chapter-{chapter}").mkdir(parents=True, exist_ok=True)
    print(f"Workspace ready: chapters/chapter-{chapter}/")

if __name__ == "__main__":
    main()
