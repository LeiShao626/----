import pymupdf, os
PDF = r"D:\论文\2605.10938v2.pdf"
OUT = r"D:\论文\_work\figs"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

# figure: (pageIndex, name, x0,y0,x1,y1) in page point coords
figures = [
    (0,  "fig01", 100,436, 310,526),
    (1,  "fig02", 100, 66, 512,154),
    (2,  "fig03", 100, 52, 512,171),
    (6,  "fig04", 342,128, 500,233),
    (6,  "fig05", 100,288, 506,382),
    (7,  "fig06", 350,173, 500,292),
    (7,  "fig07", 100,352, 508,462),
    (8,  "fig08", 112,252, 504,404),
    (19, "fig09", 100,176, 508,292),
    (20, "fig10", 100,444, 514,638),
    (25, "fig11", 100, 62, 508,184),
    (25, "fig12", 140,288, 430,412),
    (26, "fig13", 140, 62, 438,188),
    (26, "fig14", 140,248, 310,370),
    (26, "fig15", 335,248, 480,370),
    (27, "fig16", 140, 62, 438,186),
    (27, "fig17", 140,240, 438,352),
    (32, "fig18", 100, 66, 512,134),
]
os.makedirs(OUT, exist_ok=True)
for pno, name, x0,y0,x1,y1 in figures:
    page = doc[pno]
    clip = pymupdf.Rect(x0,y0,x1,y1)
    pix = page.get_pixmap(clip=clip, dpi=320)
    path = os.path.join(OUT, name + ".png")
    pix.save(path)
    print("saved", name, pix.width, pix.height)
