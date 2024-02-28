import fitz

# Open the PDF document
doc = fitz.open("/tmp/Outline.pdf")

with open(
    "/home/jenny/Downloads/Noto_Sans_Tamil/static/NotoSansTamil-Regular.ttf", "rb"
) as font_file:
    font_buffer = font_file.read()


# Embed the font
page = doc[0]  # Select the first page
page.insert_font(fontname="latha", fontbuffer=font_buffer)

# Now you can use "MuktaMalar" as the font name when inserting text
page.insert_text((50, 50), "குரலின் தொனி", fontname="latha", fontsize=12)

# Save the modified PDF
doc.save("modified.pdf")
