import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\media"
doc = pymupdf.open(PDF)
page = doc[6]
pix = page.get_pixmap(clip=pymupdf.Rect(300,258,545,405), dpi=320)
pix.save(os.path.join(OUT,"fig02.png"))
print("saved", pix.width, pix.height)
