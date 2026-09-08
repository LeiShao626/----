import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\pages"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)
# figure/table pages: fig1/fig2 on p7(idx6), fig3/fig4 on p8(idx7), fig5 on p16(idx15), table1 on p2(idx1)
for pno in [1,6,7,15]:
    page = doc[pno]
    pix = page.get_pixmap(dpi=200)
    pix.save(os.path.join(OUT, "page%02d.png" % (pno+1)))
    print("saved page%02d" % (pno+1))
