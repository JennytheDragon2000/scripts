import fitz  # PyMuPDF

doc = fitz.open("/home/jenny/Downloads/Telegram Desktop/Outline.pdf")
text = ""
for page in doc:
    text += page.get_text("text")

print(text)
