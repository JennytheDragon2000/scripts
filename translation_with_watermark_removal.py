import io
import os
import tempfile
from flask import Response

import fitz  # PyMuPDF
from easygoogletranslate import EasyGoogleTranslate
from flask import Flask, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

app = Flask(__name__)
CORS(app)

translator = EasyGoogleTranslate(source_language="en", target_language="ta", timeout=10)

model = MBartForConditionalGeneration.from_pretrained(
    "facebook/mbart-large-50-one-to-many-mmt"
)

tokenizer = MBart50TokenizerFast.from_pretrained(
    "facebook/mbart-large-50-one-to-many-mmt", src_lang="en_XX"
)

def remove_watermark(pdf_path, output_path):
    doc = fitz.open(pdf_path)

    for page in doc:
        # Standardize the page's content stream
        page.clean_contents()
        xref = page.get_contents()[0]  # Get the xref of the resulting /Contents object
        cont = bytearray(page.read_contents())  # Read the contents source as a modifyable bytearray

        # Find and remove the watermark
        while True:
            i1 = cont.find(b"/Fm0 Do")  # Start of the watermark definition
            if i1 < 0:
                break  # No more watermarks left
            i2 = cont.find(b"Q", i1)  # End of the watermark definition
            cont[i1: i2 + 1] = b""  # Remove the watermark definition

        # Update the content stream
        doc.update_stream(xref, cont)

    # Save the modified document
    doc.save(output_path)

def english_to_tamil(article_en):
    model_inputs = tokenizer(article_en, return_tensors="pt")
    # translate from English to Tamil
    generated_tokens = model.generate(
        **model_inputs, forced_bos_token_id=tokenizer.lang_code_to_id["ta_IN"]
    )
    translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    # Join the list of strings into a single string
    tamil_text = " ".join(translation)
    return tamil_text

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    if file:
        # Use secure_filename to ensure a safe filename
        filename = secure_filename(file.filename)

        # Save the uploaded file to a temporary location
        # Use tempfile.gettempdir() to get the path to the temporary directory
        file_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(file_path)

        # Remove watermark from the PDF
        watermark_removed_path = os.path.join(tempfile.gettempdir(), "watermark_removed.pdf")
        remove_watermark(file_path, watermark_removed_path)

        # Process the PDF with your script
        process_pdf(watermark_removed_path)

        # Assuming the modified PDF is saved as 'modified.pdf' in the current working directory
        modified_file_path = os.path.join(os.getcwd(), "modified.pdf")
        with open(modified_file_path, "rb") as f:
            modified_pdf_data = f.read()

        return Response(modified_pdf_data, mimetype="application/pdf", headers={"Content-Disposition": "attachment;filename=modified.pdf"})

def process_pdf(file_path):
    doc = fitz.open(file_path)
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

            result = english_to_tamil(full_text)
            tamil_text = result
            print(tamil_text)

            # Insert the Tamil text into the rectangle
            page.insert_htmlbox(
                bounding_box,
                tamil_text,
                css="* {font-family: sans-serif; font-size:11px;}",
            )

        # Save the modified PDF
        doc.save("modified.pdf", garbage=4, deflate=True, linear=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
