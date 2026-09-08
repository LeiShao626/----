import pymupdf
import os, io

PDF = r"D:\论文\2602.01148v1.pdf"
OUTDIR = r"D:\论文\_work2"
os.makedirs(OUTDIR, exist_ok=True)
doc = pymupdf.open(PDF)
print("PAGES:", doc.page_count)
print("METADATA:", doc.metadata)

log = []
for pno in range(doc.page_count):
    page = doc[pno]
    log.append("\n" + "="*70)
    log.append("PAGE %d  (w=%.0f h=%.0f)" % (pno+1, page.rect.width, page.rect.height))
    imgs = page.get_images(full=True)
    if imgs:
        log.append("--- images (%d):" % len(imgs))
    for im in imgs:
        xref = im[0]
        rects = page.get_image_rects(xref)
        for r in rects:
            log.append("  IMG xref=%s at %s" % (xref, r))
    d = page.get_text("dict")
    blocks = []
    for b in d["blocks"]:
        if b["type"] == 0:
            txt = "".join(s["text"] for l in b["lines"] for s in l["spans"])
            if txt.strip():
                blocks.append((b["bbox"], txt))
        else:
            blocks.append((b["bbox"], None))
    blocks.sort(key=lambda x: (round(x[0][1],1), round(x[0][0],1)))
    for bbox, txt in blocks:
        if txt is None:
            log.append("  [IMG-BLOCK bbox=%s]" % (tuple(round(v,1) for v in bbox),))
        else:
            log.append("  [%.0f,%.0f] %s" % (bbox[0], bbox[1], txt))

with io.open(os.path.join(OUTDIR, "structure.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("done")
