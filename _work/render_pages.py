import pymupdf, os
PDF = r"D:\论文\2605.10938v2.pdf"
OUT = r"D:\论文\_work\pages"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)
# pages containing figures and tables/algorithms
pages = [0,1,2,6,7,8,19,20,25,26,27,32]
for pno in pages:
    page = doc[pno]
    pix = page.get_pixmap(dpi=200)
    name = os.path.join(OUT, "page%02d.png" % (pno+1))
    pix.save(name)
    print("saved", name, pix.width, pix.height)
