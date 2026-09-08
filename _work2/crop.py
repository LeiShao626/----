import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\media"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

items = [
    # figures (pageIdx, name, x0,y0,x1,y1)
    (1,  "table1",  55, 60, 545, 200),   # Table1 (top of p2)
    (6,  "fig01",  305, 60, 545, 250),   # Figure1 (top-right p7)
    (6,  "fig02",  305,255, 545, 410),   # Figure2 (mid-right p7)
    (7,  "fig03",   55, 60, 300, 260),   # Figure3 (top-left p8)
    (7,  "fig04",   55,310, 300, 480),   # Figure4 (below-left p8)
    (15, "fig05",   55, 60, 545, 340),   # Figure5 (top of p16)
]
for pno,name,x0,y0,x1,y1 in items:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=320)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
