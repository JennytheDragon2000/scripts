import fitz


def remove_watermark(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    for page in doc:
        # Standardize the page's content stream
        page.clean_contents()
        xref = page.get_contents()[0]  # Get the xref of the resulting /Contents object
        cont = bytearray(
            page.read_contents()
        )  # Read the contents source as a modifyable bytearray

        # Find and remove the watermark
        while True:
            i1 = cont.find(b"/Fm0 Do")  # Start of the watermark definition
            if i1 < 0:
                break  # No more watermarks left
            i2 = cont.find(b"Q", i1)  # End of the watermark definition
            cont[i1 : i2 + 1] = b""  # Remove the watermark definition

        # Update the content stream
        doc.update_stream(xref, cont)

    # Save the modified document
    doc.save(output_path)


# Example usage
remove_watermark("/tmp/page_1.pdf", "output-no-watermark.pdf")
