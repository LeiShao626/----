# -*- coding: utf-8 -*-
import io, re

src = io.open(r"D:\note_for_paper\_work3\lines.txt", encoding="utf-8").read().split("\n")
page = 0
cur = []
out = []
for ln in src:
    m = re.match(r"^=+ PAGE (\d+) \(draw=(\d+)\)", ln)
    if m:
        page = int(m.group(1))
        out.append("\n### PAGE %d  draw=%s" % (page, m.group(2)))
        continue
    if ln.startswith("IMG "):
        out.append("    " + ln)
        continue
    if re.search(r"\|\s*(Figure|Table|Algorithm|Listing)\s*\d", ln):
        txt = ln.split("|", 1)[1].strip()
        out.append("    CAPTION p%d: %s" % (page, txt))

io.open(r"D:\note_for_paper\_work3\pagemap.txt", "w", encoding="utf-8").write("\n".join(out))
print("ok")
