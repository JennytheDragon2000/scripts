import os
import faiss
from sentence_transformers import SentenceTransformer

# Load your transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Directory containing text files
text_files_dir = "path/to/your/text/files"

# Read and preprocess text files
documents = []
file_names = []
for file_name in os.listdir(text_files_dir):
    with open(os.path.join(text_files_dir, file_name), "r") as file:
        text = file.read()
        documents.append(text)
        file_names.append(file_name)

# Vectorize the documents
document_vectors = model.encode(documents)

# Save vectors to FAISS
index = faiss.IndexFlatL2(document_vectors.shape[1])
index.add(document_vectors)

# Save file names and vectors for reference
metadata = {"file_names": file_names, "vectors": document_vectors}


# Convert the query to a vector
query = "Your question here"
query_vector = model.encode([query])

# Search for the closest vectors
k = 5  # Number of closest documents to retrieve
D, I = index.search(query_vector, k)

# Retrieve and display the results
for i in range(k):
    doc_id = I[0][i]
    print(f"File: {metadata['file_names'][doc_id]}")
    print(f"Text: {documents[doc_id]}\n")
