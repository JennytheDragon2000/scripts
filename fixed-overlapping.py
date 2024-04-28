import fitz

# Open the PDF document
doc = fitz.open("/tmp/Outline.pdf")

# Select the first page
page = doc[0]

details = page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)  # skips images!
for block in details["blocks"]:  # delivers the block level
    for line in block["lines"]:  # the lines in this block
        bbox = fitz.Rect(line["bbox"])  # wraps this line
        line_text = "".join([span["text"] for span in line["spans"]])
        page.add_redact_annot(bbox)

        print(line_text)

doc.save("modified.pdf")
