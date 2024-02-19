import fitz

# Open the PDF document
doc = fitz.open("/tmp/Outline.pdf")

# Select the first page
page = doc[0]

# Get text blocks
text_blocks = page.get_text("blocks")

# Initialize TextWriter with the page rectangle
tw = fitz.TextWriter(page.rect)

# for page in doc:
#     # Get text blocks
#     text_blocks = page.get_text("blocks")
# Add text to each text block
for block in text_blocks:
    # Define the rectangle for the text block
    rect = fitz.Rect(block[0], block[1], block[2], block[3])
    page.add_redact_annot(rect)

    # Define the text and its properties
    text = "Your new text here"
    font = fitz.Font("helv")  # You can specify your own font
    fontsize = 11

    # Append the text to the TextWriter
    tw.append(rect.bl, text, font=font, fontsize=fontsize)

# page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
# Write the text to the page
tw.write_text(page)

# Save the modified PDF
doc.save("modified.pdf")
