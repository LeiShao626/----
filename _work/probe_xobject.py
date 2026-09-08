import pymupdf
PDF = r"D:\论文\2605.10938v2.pdf"
doc = pymupdf.open(PDF)
for pno in [0,1,2,6,7,8,19,20,25,26,27,32]:
    page = doc[pno]
    print("="*50, "PAGE", pno+1)
    try:
        xo = page.get_xobjects()
        print(" xobjects:", len(xo))
        for x in xo:
            print("   ", x)
    except Exception as e:
        print(" xobjects err", e)
    print(" drawings count:", len(page.get_drawings()))
    # all image / forms rects
    info = page.get_image_info(xrefs=True)
    print(" image_info:", len(info))
    for i in info:
        print("   ", round(i["bbox"][0]),round(i["bbox"][1]),round(i["bbox"][2]),round(i["bbox"][3]), "xref",i.get("xref"))
