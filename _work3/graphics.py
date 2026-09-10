# -*- coding: utf-8 -*-
"""Detect non-text graphic bands (figures / tables / algorithm boxes) per page."""
import pymupdf, os, io

PDF = r"D:\note_for_paper\deepseek\DeepSeek_V41_Tech_Report.pdf"
OUT = r"D:\note_for_paper\_work3"

doc = pymupdf.open(PDF)
report = []

for pno in range(doc.page_count):
    page = doc[pno]
    rects = []
    for d in page.get_drawings():
        r = pymupdf.Rect(d["rect"])
        rects.append(r)
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            rects.append(pymupdf.Rect(r))

    # discard hairline rules and tiny marks
    rects = [r for r in rects if (r.height > 2.0 and r.width > 12.0)]

    text_bands = []
    td = page.get_text("dict")
    for b in td["blocks"]:
        if b["type"] == 0:
            for l in b["lines"]:
                if "".join(s["text"] for s in l["spans"]).strip():
                    text_bands.append(pymupdf.Rect(l["bbox"]))

    rects.sort(key=lambda r: (r.y0, r.x0))
    bands = []
    for r in rects:
        if bands and r.y0 <= bands[-1].y1 + 4:
            bands[-1] |= r
        else:
            bands.append(pymupdf.Rect(r))

    keep = []
    for b in bands:
        if b.height < 24 or b.width < 40:
            continue
        # how much text sits inside this band?
        covered = 0.0
        for t in text_bands:
            ix = t & b
            if not ix.is_empty:
                covered += ix.get_area()
        keep.append((b, covered / max(b.get_area(), 1.0)))

    report.append("PAGE %d" % (pno + 1))
    for b, frac in keep:
        report.append("   band (%.1f, %.1f, %.1f, %.1f) h=%.1f textcover=%.2f"
                      % (b.x0, b.y0, b.x1, b.y1, b.height, frac))

with io.open(os.path.join(OUT, "graphics.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print("ok")
