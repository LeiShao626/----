import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\math"
doc = pymupdf.open(PDF)
page = doc[3]
pix = page.get_pixmap(clip=pymupdf.Rect(305,700,545,730), dpi=340)
pix.save(os.path.join(OUT,"eq_def46.png"))
print("saved", pix.width, pix.height)
