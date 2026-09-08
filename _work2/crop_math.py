import pymupdf, os, io, json
PDF = r"D:\论文\2602.01148v1.pdf"
OUT = r"D:\论文\_work2\math"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

# Main-body theorem/lemma/definition/equation blocks.
# (pageIdx, name, x0,y0,x1,y1) in PDF points; x0/x1 chosen to span just the column containing the block.
# left column ~55-295, right column ~305-545.
blocks = [
    # ---- Page 3 (idx2) ----
    (2, "eq_cotp",      54, 388, 300, 424),   # p_theta(S|x)=prod
    (2, "eq_latent",    54, 527, 300, 548),   # h_k=f_theta(h_{k-1})
    (2, "eq_coconut",   54, 654, 300, 686),   # L_coconut
    (2, "eq_primal",   300, 636, 545, 688),   # primal CIB
    (2, "eq_dual",     300, 688, 545, 712),   # dual CIB
    # ---- Page 4 (idx3) ----
    (3, "eq_dkl4_2",    54, 664, 300, 712),   # DKL (Thm 4.3) + argmax
    # ---- Page 5 (idx4) ----
    (4, "eq_thm47",     54, 108, 300, 160),   # Thm4.7 P[..]=0
    (4, "eq_def49",    300, 108, 545, 135),   # IS = max p
    (4, "eq_def410",   300, 305, 545, 345),   # \Delta l = li* - lj*
    (4, "eq_thm411",   300, 405, 545, 445),   # \Delta l >= log(IS/(1-IS))
    (4, "eq_thm48",     54, 415, 300, 448),   # E[||E_M||^2] = ...
    # ---- Page 6 (idx5) ----
    (5, "eq_R",        300, 82, 545, 108),    # R(theta)
    (5, "eq_thm51",    300, 298, 545, 330),   # R(hat theta_MLE) <= ...
    (5, "eq_thm412",   300, 655, 545, 700),   # DKL >= ...
    # ---- Page 7 (idx6) ----
    (6, "eq_thm52",     54, 96, 300, 148),    # R(hat theta) >= ...
    # ---- Page 16 (idx15) ----
    (15,"eq_A4",        54, 425, 545, 470),   # Lemma A.4 sup max <= 1-delta
    # ---- Page 19 (idx18) ----
    (18,"eq_Acc",      290, 300, 545, 350),   # A(sigma)=Phi(...)
]
for pno,name,x0,y0,x1,y1 in blocks:
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0,y0,x1,y1), dpi=340)
    pix.save(os.path.join(OUT,name+".png"))
    print("saved",name,pix.width,pix.height)
