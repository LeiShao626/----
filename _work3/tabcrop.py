# -*- coding: utf-8 -*-
"""Locate table / algorithm / figure regions and export crops."""
import pymupdf, os, io, json

PDF = r"D:\note_for_paper\deepseek\DeepSeek_V41_Tech_Report.pdf"
OUT = r"D:\note_for_paper\_work3\blocks"
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

CROPS = {
    # name: (page_index, x0, y0, x1, y1)
    "fig01": (0, 68, 505, 528, 675),
    "fig02": (4, 155, 80, 440, 234),
    "fig03": (6, 62, 78, 532, 322),
    "fig04": (9, 62, 78, 534, 233),
    "fig05": (10, 62, 78, 532, 293),
    "tab01": (23, 62, 142, 542, 470),
    "fig06": (24, 145, 80, 450, 244),
    "fig07": (26, 85, 78, 508, 357),
    "fig08": (27, 85, 78, 508, 242),
    "tab02": (29, 62, 248, 542, 356),
    "tab03": (32, 62, 218, 542, 470),
    "fig09": (34, 62, 78, 534, 202),
    "tab04": (34, 62, 312, 542, 445),
    "fig10": (35, 86, 78, 510, 242),
    "tab05": (47, 140, 100, 455, 168),
    "fig11": (48, 86, 78, 510, 317),
    "fig12": (49, 62, 78, 534, 273),
    "alg01": (15, 62, 92, 534, 352),
}

for name, (pno, x0, y0, x1, y1) in CROPS.items():
    page = doc[pno]
    pix = page.get_pixmap(clip=pymupdf.Rect(x0, y0, x1, y1), dpi=300)
    pix.save(os.path.join(OUT, name + ".png"))
    print(name, pix.width, pix.height)
