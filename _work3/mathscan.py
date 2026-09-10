# -*- coding: utf-8 -*-
"""Find display-equation lines (centered math) and their bounding boxes."""
import pymupdf, io, os, re

PDF = r"D:\note_for_paper\deepseek\DeepSeek_V41_Tech_Report.pdf"
doc = pymupdf.open(PDF)

MATHFONT = re.compile(r"(Math|txmia|txsys|txexs|txsym|CMSY|CMEX|msam|msbm|rsfs)")
out = []
for pno in range(doc.page_count):
    page = doc[pno]
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            spans = l["spans"]
            txt = "".join(s["text"] for s in spans)
            if not txt.strip():
                continue
            fonts = {s["font"] for s in spans}
            if not any(MATHFONT.search(f) for f in fonts):
                continue
            x0, y0, x1, y1 = l["bbox"]
            # centered display math: starts well right of the column edge
            if x0 > 95:
                out.append("p%-3d %.1f %.1f %.1f %.1f  %s | %s"
                           % (pno + 1, x0, y0, x1, y1, sorted(fonts), txt[:70]))

io.open(r"D:\note_for_paper\_work3\mathlines.txt", "w", encoding="utf-8").write("\n".join(out))
print("candidates:", len(out))
