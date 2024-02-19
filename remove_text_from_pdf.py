import fitz

# Open the PDF document
doc = fitz.open("/tmp/Outline.pdf")

# Select the first page
# page = doc[0]

for page in doc:
    # Get text blocks
    text_blocks = page.get_text("blocks")

    # Add redaction annotations for each text block
    for block in text_blocks:
        rect = fitz.Rect(block[0], block[1], block[2], block[3])
        page.add_redact_annot(rect)

    # Apply redactions to remove text
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

# Save the modified PDF
doc.save("redacted.pdf")
