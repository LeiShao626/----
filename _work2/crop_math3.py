import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\math"
doc = pymupdf.open(PDF)
blocks = [
    (3, "eq_thm45", 300, 366, 545, 396),   # Thm 4.5 DKL <= -(1/2)log delta - c  (page4 idx3)
    (5, "eq_thm412",300, 655, 545, 692),   # Thm 4.12 DKL >= log B + ... (page6 idx5)
    (3, "eq_def46", 300, 655, 545, 712),   # Def 4.6 argmax (page4 idx3)
]
for pno,name,x0,y0,x1,y1 in blocks:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=340)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
