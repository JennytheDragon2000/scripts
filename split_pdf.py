import argparse
import os
import PyPDF2


def split_pdf(input_pdf, output_folder):
    # Open the input PDF file
    with open(input_pdf, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through each page and save it as a separate PDF
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            output_path = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
            writer = PyPDF2.PdfWriter()
            writer.add_page(page)
            with open(output_path, "wb") as output_file:
                writer.write(output_file)


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Split a PDF into individual pages")
    parser.add_argument("input_pdf", help="Input PDF file to split")
    parser.add_argument("output_folder", help="Output folder to save individual pages")
    args = parser.parse_args()

    # Split the PDF
    split_pdf(args.input_pdf, args.output_folder)


if __name__ == "__main__":
    main()
