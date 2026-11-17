#!/usr/bin/env python3
"""Render Graphviz diagrams, then convert learning Markdown to DOCX using Pandoc."""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(args):
    print('+', ' '.join(map(str, args)))
    subprocess.run(args, check=True, cwd=ROOT)


def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: python scripts/build.py INPUT.md OUTPUT.docx')
    source = (ROOT / sys.argv[1]).resolve()
    target = (ROOT / sys.argv[2]).resolve()
    if not source.is_file():
        sys.exit(f'Missing Markdown: {source}')
    for binary in ('dot', 'pandoc'):
        if not shutil.which(binary):
            sys.exit(f'Missing {binary}. Install Graphviz and Pandoc and put them on PATH.')
    diagrams = ROOT / 'diagrams'
    dest = diagrams / 'output'
    dest.mkdir(parents=True, exist_ok=True)
    for dot in sorted(diagrams.rglob('*.dot')):
        if 'output' in dot.relative_to(diagrams).parts:
            continue
        relative = dot.relative_to(diagrams).with_suffix('.png')
        output_image = dest / relative
        output_image.parent.mkdir(parents=True, exist_ok=True)
        run(['dot', '-Tpng', str(dot), '-o', str(output_image)])
    target.parent.mkdir(parents=True, exist_ok=True)
    args = ['pandoc', str(source), '--from=gfm', '--to=docx', '--standalone', '--toc', '--toc-depth=2', '--resource-path', str(ROOT) + __import__('os').pathsep + str(source.parent), '-o', str(target)]
    ref = ROOT / 'templates/reference.docx'
    if ref.is_file():
        args += ['--reference-doc', str(ref)]
    run(args)
    print(f'Created {target}')

if __name__ == '__main__':
    main()
