"""Apply restrained handbook typography using standard-library OOXML tools."""
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as E

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
E.register_namespace('w', W)
def tag(n): return '{'+W+'}'+n
def child(parent, name, attrs=None):
    obj=parent.find(tag(name))
    if obj is None:
        obj=E.Element(tag(name))
        if name.endswith('Pr'): parent.insert(0,obj)
        else: parent.append(obj)
    for k,v in (attrs or {}).items(): obj.set(tag(k),str(v))
    return obj

def main():
    path=Path(sys.argv[1])
    with zipfile.ZipFile(path) as z: files={n:z.read(n) for n in z.namelist()}
    styles=E.fromstring(files['word/styles.xml'])
    for st in styles.findall(tag('style')):
        sid=st.get(tag('styleId'),'')
        rp=child(st,'rPr'); pp=child(st,'pPr')
        if sid in ('Normal','BodyText','FirstParagraph'):
            child(rp,'rFonts',{'ascii':'Calibri','hAnsi':'Calibri'})
            child(rp,'sz',{'val':22}); child(rp,'color',{'val':'243746'})
            child(pp,'spacing',{'after':120,'line':285,'lineRule':'auto'})
        if sid.startswith('Heading'):
            child(rp,'rFonts',{'ascii':'Calibri','hAnsi':'Calibri'})
            child(rp,'color',{'val':'174A65'}); child(pp,'keepNext')
        if sid=='Heading1':
            child(rp,'sz',{'val':34}); child(pp,'pageBreakBefore')
        if sid=='Heading2': child(rp,'sz',{'val':26})
        if sid=='Title':
            child(rp,'sz',{'val':56}); child(rp,'color',{'val':'174A65'})
    doc=E.fromstring(files['word/document.xml'])
    q=0
    for p in doc.iter(tag('p')):
        text=''.join(t.text or '' for t in p.iter(tag('t')))
        pp=child(p,'pPr')
        if text.startswith('Q') and len(text)>3 and text[1:3].isdigit() and text[3]=='.':
            q+=1
            child(pp,'keepNext'); child(pp,'shd',{'fill':'EAF2F8'})
            child(pp,'spacing',{'before':220,'after':100})
            for r in p.findall(tag('r')):
                rp=child(r,'rPr'); child(rp,'color',{'val':'1E6591'}); child(rp,'b'); child(rp,'sz',{'val':25})
        if text.startswith('Source:'):
            for r in p.findall(tag('r')):
                rp=child(r,'rPr'); child(rp,'i'); child(rp,'color',{'val':'596B77'}); child(rp,'sz',{'val':19})
        if text.startswith('Follow-up:'):
            child(pp,'keepNext')
        for r in p.findall(tag('r')):
            rt=''.join(t.text or '' for t in r.iter(tag('t')))
            if rt.startswith('Follow-up:'):
                child(child(r,'rPr'),'color',{'val':'287567'})
    for table in doc.iter(tag('tbl')):
        child(child(table,'tblPr'),'tblW',{'w':5000,'type':'pct'})
        child(child(table,'tblPr'),'tblLayout',{'type':'fixed'})
        grid=child(table,'tblGrid')
        for item in list(grid): grid.remove(item)
        for width in (2400,6600): child_col=E.SubElement(grid,tag('gridCol')); child_col.set(tag('w'),str(width))
        rows=table.findall(tag('tr'))
        if rows:
            child(child(rows[0],'trPr'),'tblHeader')
        for i,row in enumerate(rows):
            child(child(row,'trPr'),'cantSplit')
            for ci,cell in enumerate(row.findall(tag('tc'))):
                child(child(cell,'tcPr'),'tcW',{'w':2400 if ci==0 else 6600,'type':'dxa'})
                child(child(cell,'tcPr'),'shd',{'fill':'174A65' if i==0 else ('F0F5F8' if i%2 else 'FFFFFF')})
                for r in cell.iter(tag('r')):
                    rp=child(r,'rPr'); child(rp,'sz',{'val':20})
                    if i==0: child(rp,'color',{'val':'FFFFFF'}); child(rp,'b')
    files['word/styles.xml']=E.tostring(styles,encoding='utf-8',xml_declaration=True)
    files['word/document.xml']=E.tostring(doc,encoding='utf-8',xml_declaration=True)
    tmp=path.with_suffix('.polished.docx')
    with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
        for n,b in files.items(): z.writestr(n,b)
    tmp.replace(path)
    print('Applied handbook styles; colored questions:',q)
if __name__=='__main__': main()
