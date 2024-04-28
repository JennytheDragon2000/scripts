import os

import fitz
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/remove-watermark": {"origins": "*"}})


def remove_watermark(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    for page in doc:
        page.clean_contents()
        xref = page.get_contents()[0]
        cont = bytearray(page.read_contents())

        while True:
            i1 = cont.find(b"/Fm0 Do")
            if i1 < 0:
                break
            i2 = cont.find(b"Q", i1)
            cont[i1 : i2 + 1] = b""

        doc.update_stream(xref, cont)

    doc.save(output_path)


@app.route("/remove-watermark", methods=["POST"])
def remove_watermark_endpoint():
    if "pdf" not in request.files:
        return "No PDF file part", 400

    file = request.files["pdf"]
    if file.filename == "":
        return "No selected file", 400

    # Save the uploaded PDF to a temporary file
    temp_pdf_path = "/tmp/uploaded.pdf"
    file.save(temp_pdf_path)

    # Define the output path for the modified PDF
    output_path = "/tmp/no_watermark.pdf"

    # Process the PDF
    remove_watermark(temp_pdf_path, output_path)

    # Send the modified PDF back to the client
    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8001)
