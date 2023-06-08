import os
import time
from PyPDF2 import PdfMerger

def merge_pdfs(input_dir, output_file):
    merger = PdfMerger()
    
    # Get the initial list of PDF files in the input directory
    file_list = get_pdf_files(input_dir)
    
    while True:
        # Check for new PDF files
        new_files = get_new_pdf_files(input_dir, file_list)
        
        if new_files:
            print(f"Merging {len(new_files)} new file(s)...")
            # Merge the new PDF files
            for filename in new_files:
                file_path = os.path.join(input_dir, filename)
                merger.append(file_path)
            
            # Write the merged PDF to the output file
            merger.write(output_file)
            merger.close()
            
            print("Merge complete!")
            
            # Update the file list
            file_list.extend(new_files)
        
        # Wait for 1 second before checking again
        time.sleep(1)

def get_pdf_files(directory):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_files.append(filename)
    return pdf_files

def get_new_pdf_files(directory, file_list):
    pdf_files = get_pdf_files(directory)
    new_files = [filename for filename in pdf_files if filename not in file_list]
    return new_files

# Specify the input directory and output file path
input_directory = '/path/to/input/folder'
output_file_path = '/path/to/output/file.pdf'

# Call the merge_pdfs function with the specified paths
merge_pdfs(input_directory, output_file_path)

