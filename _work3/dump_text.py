# -*- coding: utf-8 -*-
import pymupdf, os, io, unicodedata, collections

PDF = r"D:\note_for_paper\deepseek\DeepSeek_V41_Tech_Report.pdf"
OUT = r"D:\note_for_paper\_work3\src"
os.makedirs(OUT, exist_ok=True)

doc = pymupdf.open(PDF)
bad = collections.Counter()
for pno in range(doc.page_count):
    page = doc[pno]
    txt = page.get_text("text")
    with io.open(os.path.join(OUT, "page%02d.txt" % (pno + 1)), "w", encoding="utf-8") as f:
        f.write(txt)
    for ch in txt:
        o = ord(ch)
        if o > 0x2000 and ch not in "\u2018\u2019\u201c\u201d\u2013\u2014\u2026\u2212":
            bad[ch] += 1

with io.open(os.path.join(OUT, "_suspect_chars.txt"), "w", encoding="utf-8") as f:
    for ch, c in bad.most_common():
        f.write("U+%04X %s %s x%d\n" % (ord(ch), ch, unicodedata.name(ch, "?"), c))

allt = "\n".join(doc[p].get_text("text") for p in range(doc.page_count))
print("words:", len(allt.split()))
print("chars:", len(allt))
print("done")
