# -*- coding: utf-8 -*-
from docx import Document
import io
p = r"D:\论文\zh_cn\ELF_嵌入式语言流_中文翻译.docx"
d = Document(p)
out = []
for para in d.paragraphs:
    if para.text.strip():
        out.append(para.text)
with io.open(r"D:\论文\_work\dump.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("written", len(out))
