#!/usr/bin/env python3
"""Basic Q&A completeness, unresolved markers, and DOCX integrity checks."""
import re
import sys
from pathlib import Path
from docx import Document

ROOT=Path(__file__).resolve().parents[1]
def main():
    if len(sys.argv)!=3: sys.exit('Usage: python scripts/validate.py INPUT.md OUTPUT.docx')
    md=(ROOT/sys.argv[1]).read_text(encoding='utf-8')
    docpath=ROOT/sys.argv[2]
    errors=[]
    questions=list(re.finditer(r'^### Q(\d+)\.\s+.+$',md,re.M))
    for i,m in enumerate(questions):
        segment=md[m.end():questions[i+1].start() if i+1<len(questions) else len(md)]
        segment=segment.split('## Section ',1)[0].split('## Chapter glossary',1)[0].split('## Revision checklist',1)[0]
        if '**Model answer:**' not in segment: errors.append(f'Q{m.group(1)} missing model answer')
        if segment.count('**Follow-up:**')!=segment.count('**Follow-up answer:**'):
            errors.append(f'Q{m.group(1)} follow-up count mismatch')
    if not questions: errors.append('No numbered questions found')
    nums=[int(m.group(1)) for m in questions]
    if nums and nums!=list(range(1,len(nums)+1)):
        errors.append(f'Question numbers are not sequential: {nums}')
    markers=['[Exact DDIA Section Title]', '[Next book section]', '[Complete answer]', '[Actual answer', '[What will I be able to explain?', '[Teach in coherent paragraphs', '[Core idea 1]', '[Book section heading]', 'DRAFT TEMPLATE. NOT A FINISHED HANDBOOK.', '[Repeat the same structure.', '[Define key terms in one place.]']
    for marker in markers:
        if marker in md: errors.append(f'Unresolved placeholder: {marker}')
    if not docpath.exists(): errors.append('DOCX missing')
    else:
        doc=Document(str(docpath))
        if len(doc.paragraphs)<20: errors.append('DOCX appears very short')
        print('DOCX paragraphs:',len(doc.paragraphs),'inline shapes:',len(doc.inline_shapes))
    print('Questions:',len(questions),'Follow-ups:',md.count('**Follow-up:**'))
    if errors:
        for e in errors: print('FAIL:',e)
        sys.exit(1)
    print('PASS: Basic validation checks. Still inspect rendered pages and source fidelity manually.')
if __name__=='__main__':main()
