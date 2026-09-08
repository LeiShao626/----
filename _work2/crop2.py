import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\media"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

items = [
    # figures WITHOUT their caption text
    (6,  "fig01",  300, 60, 545, 212),
    (6,  "fig02",  300,252, 545, 402),
    (7,  "fig03",   55, 60, 300, 222),
    (7,  "fig04",   55,310, 300, 436),
    (15, "fig05",   55, 60, 545, 322),
]
for pno,name,x0,y0,x1,y1 in items:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=320)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
