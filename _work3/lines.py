# -*- coding: utf-8 -*-
import pymupdf, os, io

PDF = r"D:\note_for_paper\deepseek\DeepSeek_V41_Tech_Report.pdf"
OUT = r"D:\note_for_paper\_work3\lines.txt"

doc = pymupdf.open(PDF)
out = []
for pno in range(doc.page_count):
    page = doc[pno]
    out.append("\n========== PAGE %d (draw=%d) ==========" % (pno + 1, len(page.get_drawings())))
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            out.append("IMG xref=%s %s" % (im[0], tuple(round(v, 1) for v in r)))
    d = page.get_text("dict")
    rows = []
    for b in d["blocks"]:
        if b["type"] != 0:
            rows.append((b["bbox"][1], b["bbox"][0], "[RASTER %.0f %.0f %.0f %.0f]"
                         % (b["bbox"][0], b["bbox"][1], b["bbox"][2], b["bbox"][3])))
            continue
        for l in b["lines"]:
            txt = "".join(s["text"] for s in l["spans"])
            if not txt.strip():
                continue
            fonts = sorted({s["font"] for s in l["spans"]})
            sz = sorted({round(s["size"], 1) for s in l["spans"]})
            rows.append((l["bbox"][1], l["bbox"][0],
                         "x=%6.1f y=%6.1f x1=%6.1f sz=%s %s | %s"
                         % (l["bbox"][0], l["bbox"][1], l["bbox"][2], sz, fonts, txt)))
    rows.sort(key=lambda r: (round(r[0], 1), round(r[1], 1)))
    for r in rows:
        out.append(r[2])

with io.open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("ok", len(out))
