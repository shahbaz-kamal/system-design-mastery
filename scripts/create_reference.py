#!/usr/bin/env python3
"""Create a reusable Pandoc reference Word document with headings and body styles."""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Inches
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'templates/reference.docx'
path.parent.mkdir(parents=True,exist_ok=True)
doc=Document()
sec=doc.sections[0]
sec.top_margin=Inches(.8);sec.bottom_margin=Inches(.75)
sec.left_margin=Inches(.85);sec.right_margin=Inches(.85)
styles=doc.styles
normal=styles['Normal'];normal.font.name='Aptos';normal.font.size=Pt(10.5);normal.paragraph_format.space_after=Pt(7)
for name,size,color in [('Title',22,RGBColor(25,57,101)),('Heading 1',17,RGBColor(25,57,101)),('Heading 2',14,RGBColor(19,98,147)),('Heading 3',11.5,RGBColor(57,82,113))]:
    s=styles[name];s.font.name='Aptos Display';s.font.size=Pt(size);s.font.color.rgb=color;s.font.bold=True
footer=sec.footer.paragraphs[0]
footer.text='System Design Mastery • DDIA Study Guide'
footer.style=styles['Caption']
doc.add_paragraph('Reference styles for Pandoc. This content is not included in outputs.')
doc.save(path)
print(path)
