import pymupdf, os
PDF = r"D:\论文\2605.10938v2.pdf"
OUT = r"D:\论文\_work\tbl"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

items = [
    # tables
    (8,  "tab01",  95, 62, 516, 178),   # Table 1
    (17, "tab02",  95,100, 516, 472),   # Table 2 big survey
    (19, "tab03", 150, 66, 486, 150),   # Table 3
    (19, "tab04", 120,388, 500, 478),   # Table 4
    (20, "tab05", 118, 66, 500, 152),   # Table 5
    (29, "tab06", 118, 66, 500, 130),   # Table 6
    (29, "tab07", 118,158, 512, 404),   # Table 7 hyperparams
    (30, "tab08", 110, 66, 506, 188),   # Table 8
    (30, "tab09", 150,236, 470, 298),   # Table 9
    (31, "tab10", 120, 84, 500, 258),   # Table 10
    (31, "tab11", 110,330, 512, 644),   # Table 11 configs
    # algorithms
    (4, "alg12",  95, 90, 516, 310),    # Alg1 + Alg2
    (21,"alg03",  95, 88, 516, 438),    # Alg3
    (22,"alg04",  95, 88, 516, 238),    # Alg4
    (23,"alg05",  95, 88, 516, 312),    # Alg5
    (23,"alg06",  95,412, 516, 682),    # Alg6
]
for pno,name,x0,y0,x1,y1 in items:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=300)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
