import fitz
from easygoogletranslate import EasyGoogleTranslate

# Open the PDF document
doc = fitz.open("/tmp/Outline.pdf")

# Select the first page
# page = doc[0]

for page in doc:
    text_blocks = page.get_text("words")

    min_gap = 5
    min_x_gap = 67

    # Process the blocks to separate them based on the minimum y_gap
    separated_blocks = []
    previous_block = None
    lines = []
    for block in text_blocks:
        x0, y0, x1, y1, text, line_no, *_ = block
        if previous_block:
            (
                prev_x0,
                prev_y0,
                prev_x1,
                prev_y1,
                prev_text,
                prev_line_no,
                *_,
            ) = previous_block
            y_gap = y0 - prev_y1
            x_gap = x0 - prev_x0
            print(f"{prev_text}   {text}   {y_gap}  {x_gap}")
            if y_gap > min_gap:
                separated_blocks.append(lines)
                lines = []
                lines.append(block)
                # print(f"y gap {block}")
            elif x_gap > min_x_gap:
                separated_blocks.append(lines)
                lines = []
                lines.append(block)
                # print(f"x gap {block}")
            else:
                lines.append(block)
        else:
            # This is the first block, so just add it to the list
            lines.append(block)
        previous_block = block

    separated_blocks.append(lines)
    # Now 'separated_blocks' contains blocks separated based on the minimum y_gap
    for i in separated_blocks:
        # Initialize the bounding box variables
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        # line = []
        for p in i:
            x0, y0, x1, y1, text, *_ = p
            # line.append(text)
            min_x = min(min_x, x0)
            min_y = min(min_y, y0)
            max_x = max(max_x, x1)
            max_y = max(max_y, y1)

        # full_text = " ".join(line)
        # print(full_text)
        # Create the bounding box
        bounding_box = fitz.Rect(min_x, min_y, max_x, max_y)
        page.add_redact_annot(bounding_box)

        # print("----------------------------------")
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    for i in separated_blocks:
        # Initialize the bounding box variables
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        line = []
        for p in i:
            x0, y0, x1, y1, text, *_ = p
            line.append(text)
            min_x = min(min_x, x0)
            min_y = min(min_y, y0)
            max_x = max(max_x, x1)
            max_y = max(max_y, y1)

        full_text = " ".join(line)
        print(full_text)
        # Create the bounding box
        bounding_box = fitz.Rect(min_x, min_y, max_x, max_y)
        translator = EasyGoogleTranslate(
            source_language="en", target_language="ta", timeout=10
        )
        result = translator.translate(full_text)

        tamil_text = result

        # Insert the Tamil text into the rectangle
        page.insert_htmlbox(
            bounding_box, tamil_text, css="* {font-family: sans-serif; font-size:11px;}"
        )


# Save the modified PDF
doc.save("modified.pdf")
