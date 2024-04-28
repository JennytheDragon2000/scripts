from flask import Flask, request, jsonify
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)

# Load the model and tokenizer
model_name = "hariniiiiiiiiii/finetuned-tamil-text-summarization"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


@app.route("/summarize", methods=["POST"])
def summarize_text():
    # Get the text from the request
    data = request.get_json()
    text = data.get("text", "")

    # Check if the text is not empty
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Tokenize the input text
    inputs = tokenizer.encode(
        text, return_tensors="pt", max_length=512, truncation=True
    )

    # Generate the summary
    summary_ids = model.generate(
        inputs, max_length=150, num_beams=4, early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Return the summary
    return jsonify({"summary": summary})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8999)
