import os
from flask import Flask, request, jsonify, send_file
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def ocr_pdf(pdf_path):
    extracted_text = ""
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            pix = page.get_pixmap(dpi=300)
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(image)
            extracted_text += f"\n--- Page {page_num + 1} ---\n{text}"
        pdf_document.close()
    except Exception as e:
        return f"Error occurred: {e}"
    return extracted_text

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        text = ocr_pdf(file_path)
        output_path = os.path.join(UPLOAD_FOLDER, "output.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        return send_file(output_path, as_attachment=True, download_name="output.txt")

    return jsonify({"error": "File upload failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
