import pymupdf
import os, json

PDF = r"D:\论文\2605.10938v2.pdf"
OUTDIR = r"D:\论文\_work\extract"
os.makedirs(OUTDIR, exist_ok=True)
doc = pymupdf.open(PDF)

img_counter = 0
log = []
for pno in range(doc.page_count):
    page = doc[pno]
    log.append("\n" + "="*70)
    log.append("PAGE %d  (w=%.0f h=%.0f)" % (pno+1, page.rect.width, page.rect.height))
    imgs = page.get_images(full=True)
    img_rects = {}
    for im in imgs:
        xref = im[0]
        rects = page.get_image_rects(xref)
        img_rects[xref] = rects
        # save image asset
        for r in rects:
            # crop actual rendered region
            pix = page.get_pixmap(clip=r, dpi=220)
            img_counter += 1
            name = "page%02d_img%02d.png" % (pno+1, img_counter)
            pix.save(os.path.join(OUTDIR, name))
            log.append("  IMG xref=%s at %s saved=%s" % (xref, r, name))
    # text blocks in reading order (top to bottom, left to right)
    d = page.get_text("dict")
    blocks = []
    for b in d["blocks"]:
        if b["type"] == 0:
            txt = ""
            for l in b["lines"]:
                for s in l["spans"]:
                    txt += s["text"]
            blocks.append((b["bbox"], txt))
        else:
            blocks.append((b["bbox"], None))
    blocks.sort(key=lambda x: (round(x[0][1],1), round(x[0][0],1)))
    for bbox, txt in blocks:
        if txt is None:
            log.append("  [IMG-BLOCK bbox=%s]" % (tuple(round(v,1) for v in bbox),))
        else:
            log.append("  [%.0f,%.0f] %s" % (bbox[0], bbox[1], txt))
    log.append("  --- layout: %s" % ("single" if True else ""))

with open(os.path.join(OUTDIR, "structure.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("done. images extracted:", img_counter)
