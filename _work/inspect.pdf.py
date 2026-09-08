import fitz
import json, os

PDF = r"D:\论文\2605.10938v2.pdf"
doc = fitz.open(PDF)
print("PAGES:", doc.page_count)
print("METADATA:", doc.metadata)
for pno in range(doc.page_count):
    page = doc[pno]
    print("="*60)
    print("PAGE", pno+1, "rect", page.rect)
    # images on page
    imgs = page.get_images(full=True)
    print("--- images (%d):" % len(imgs))
    for im in imgs:
        xref, sm, w, h, bpc, cs, alt, name, filt = im
        print("  xref=%s sw=%s sh=%s cs=%s filt=%s" % (xref, w, h, cs, filt))
        rects = page.get_image_rects(xref)
        for r in rects:
            print("    rect", r)
    print("--- text blocks:")
    d = page.get_text("dict")
    for b in d["blocks"]:
        if b["type"] == 0:
            txt = "".join(s["text"] for l in b["lines"] for s in l["spans"])
            if txt.strip():
                print("  TEXT[%.0f,%.0f,%.0f,%.0f]: %s" % (b["bbox"][0], b["bbox"][1], b["bbox"][2], b["bbox"][3], txt[:120]))
        else:
            print("  IMGBLOCK bbox", b["bbox"], "size", b.get("width"), b.get("height"))
