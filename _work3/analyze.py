# -*- coding: utf-8 -*-
import pymupdf, os, io, collections

PDF = r"D:\note_for_paper\deepseek\DeepSeek_V41_Tech_Report.pdf"
OUT = r"D:\note_for_paper\_work3"
os.makedirs(OUT, exist_ok=True)

doc = pymupdf.open(PDF)
log = []
size_counter = collections.Counter()

for pno in range(doc.page_count):
    page = doc[pno]
    log.append("\n" + "=" * 78)
    log.append("PAGE %d  (w=%.0f h=%.0f)" % (pno + 1, page.rect.width, page.rect.height))
    log.append("drawings=%d" % len(page.get_drawings()))
    for im in page.get_images(full=True):
        for r in page.get_image_rects(im[0]):
            log.append("  IMG xref=%s bbox=%s" % (im[0], tuple(round(v, 1) for v in r)))
    d = page.get_text("dict")
    blocks = []
    for b in d["blocks"]:
        if b["type"] == 0:
            txt = "".join(s["text"] for l in b["lines"] for s in l["spans"])
            if txt.strip():
                sizes = sorted({round(s["size"], 1) for l in b["lines"] for s in l["spans"]})
                fonts = sorted({s["font"] for l in b["lines"] for s in l["spans"]})
                for s in sizes:
                    size_counter[s] += 1
                blocks.append((b["bbox"], txt, sizes, fonts))
        else:
            blocks.append((b["bbox"], None, None, None))
    blocks.sort(key=lambda x: (round(x[0][1], 1), round(x[0][0], 1)))
    for bbox, txt, sizes, fonts in blocks:
        if txt is None:
            log.append("  [IMG-BLOCK bbox=%s]" % (tuple(round(v, 1) for v in bbox),))
        else:
            log.append("  [x=%.0f y=%.0f w=%.0f sz=%s] %s"
                       % (bbox[0], bbox[1], bbox[2] - bbox[0], sizes, txt))

with io.open(os.path.join(OUT, "structure.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))

with io.open(os.path.join(OUT, "font_sizes.txt"), "w", encoding="utf-8") as f:
    for s, c in sorted(size_counter.items()):
        f.write("%.1f : %d\n" % (s, c))

print("pages:", doc.page_count)
print("done")
