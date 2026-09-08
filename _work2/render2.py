import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\pages"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)
for pno in [3,4,5,14,16,20,22,23]:
    page = doc[pno]
    pix = page.get_pixmap(dpi=200)
    pix.save(os.path.join(OUT, "page%02d.png" % (pno+1)))
    print("saved page%02d" % (pno+1))
