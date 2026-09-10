# -*- coding: utf-8 -*-
import pymupdf, io

PDF = r"D:\note_for_paper\deepseek\DeepSeek_V41_Tech_Report.pdf"
doc = pymupdf.open(PDF)
PAGES = [15, 16, 29, 30, 32, 33, 34, 35, 47, 48]
out = []
for pno in PAGES:
    page = doc[pno]
    out.append("\n==== PAGE %d ====" % (pno + 1))
    rows = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            spans = l["spans"]
            txt = "".join(s["text"] for s in spans).strip()
            if not txt:
                continue
            mx = max(round(s["size"], 1) for s in spans)
            rows.append((l["bbox"][1], l["bbox"][0], l["bbox"][2],
                         "y=%6.1f x=%6.1f x1=%6.1f sz=%4.1f | %s"
                         % (l["bbox"][1], l["bbox"][0], l["bbox"][2], mx, txt[:78])))
    rows.sort()
    for r in rows:
        out.append(r[3])
io.open(r"D:\note_for_paper\_work3\smallys.txt", "w", encoding="utf-8").write("\n".join(out))
print("ok")
