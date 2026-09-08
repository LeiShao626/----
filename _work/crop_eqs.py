import pymupdf, os
PDF = r"D:\论文\2605.10938v2.pdf"
OUT = r"D:\论文\_work\eqs"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

eqs = [
    (3, "eq01", 150,300, 470,362),   # Eq1 LMSE
    (3, "eq02", 150,552, 470,600),   # Eq2 LCE
    (18,"eq03", 150,238, 470,285),   # Eq3 xtilde
    (18,"eq04", 240,290, 460,325),   # Eq4 Ldistill
    (22,"eq05", 150,315, 470,360),   # Eq5 vtarget
]
for pno,name,x0,y0,x1,y1 in eqs:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=340)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
