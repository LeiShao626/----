import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\media"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

# Key display equations (pageIdx, name, x0,y0,x1,y1)
eqs = [
    (2, "eq_cot",   54, 385, 300, 420),   # p_theta(S|x)=prod
    (2, "eq_lat",   54, 528, 300, 545),   # h_k=f_theta(h_{k-1})
    (2, "eq_coco",  54, 655, 300, 685),   # L_coconut
    (2, "eq_primal",306, 638, 545, 685),  # primal problem CIB
    (2, "eq_dual",  306, 688, 545, 705),  # dual
    (5, "eq_dkl53", 306, 370, 545, 400),  # Thm4.3 DKL
    (5, "eq_dkl45", 306, 370, 545, 400),
]
for pno,name,x0,y0,x1,y1 in eqs:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=340)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
