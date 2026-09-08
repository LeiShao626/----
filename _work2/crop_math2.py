import pymupdf, os
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\math"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

blocks = [
    (2, "eq_cotp",      54, 392, 300, 420),
    (2, "eq_latent",    54, 528, 300, 545),
    (2, "eq_coconut",   54, 656, 300, 684),
    (2, "eq_primal",   300, 632, 545, 690),   # primal + dual CIB
    (2, "eq_dual",     300, 688, 545, 710),
    (3, "eq_dkl4_2",    54, 666, 300, 712),   # DKL Thm4.3 + argmax
    (4, "eq_thm47",     54, 108, 300, 158),   # P[..]=0
    (4, "eq_def49",    300, 110, 545, 132),   # IS=max
    (4, "eq_def410",   300, 310, 545, 340),   # \Delta l
    (4, "eq_thm411",   300, 410, 545, 436),   # margin lower bound
    (4, "eq_thm48",     54, 418, 300, 444),   # E norm
    (5, "eq_R",        300, 84, 545, 104),    # R(theta)
    (5, "eq_thm51",    300, 300, 545, 326),   # R(hat) <=
    (5, "eq_thm412",   300, 660, 545, 688),   # DKL >=
    (6, "eq_thm52",     54, 98, 300, 142),    # R(hat) >=
    (15,"eq_A4",        54, 428, 545, 462),   # Lemma A.4
    (18,"eq_Acc",      290, 302, 545, 344),   # A(sigma)=Phi
]
for pno,name,x0,y0,x1,y1 in blocks:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=340)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
