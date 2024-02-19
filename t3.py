import fitz

# Open the PDF document
doc = fitz.open("/tmp/Outline.pdf")

# Select the first page
page = doc[0]

# Get text blocks
text_blocks = page.get_text("blocks")

# for page in doc:
#     # Get text blocks
#     text_blocks = page.get_text("blocks")
# Add text to each text block
for block in text_blocks:
    # Define the rectangle for the text block
    rect = fitz.Rect(block[0], block[1], block[2], block[3])

    # Add redaction annotation
    page.add_redact_annot(rect)

# Apply redactions
page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

# Insert new text after applying redactions
for block in text_blocks:
    # Define the rectangle for the text block
    rect = fitz.Rect(block[0], block[1], block[2], block[3])
    # Tamil text
    tamil_text = "வணக்கம், உலகம்!வணக்கம், உலகம்!வணக்கம், உலகம்!வணக்கம், உலகம்!"

    # Insert the Tamil text into the rectangle
    page.insert_htmlbox(
        rect, tamil_text, css="* {font-family: sans-serif; font-size:11px;}"
    )

# Save the modified PDF
doc.save("modified.pdf")
