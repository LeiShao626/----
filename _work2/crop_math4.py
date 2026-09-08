import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\math"
doc = pymupdf.open(PDF)
blocks = [
    # Theorem 4.12 formula: page idx4 (page5), right column bottom
    (4, "eq_thm412", 305, 655, 545, 700),
    # Definition 4.6 (argmax): page idx3 (page4), right column bottom
    (3, "eq_def46", 305, 695, 545, 712),
]
for pno,name,x0,y0,x1,y1 in blocks:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=340)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
