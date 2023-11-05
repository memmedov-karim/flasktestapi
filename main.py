from flask import Flask,jsonify,request
import pdfplumber
import PyPDF2
import re
import pyresparser
app = Flask(__name__)

@app.route("/")
def home():
    return "Home"
@app.route("/getusers")
def getusers():
    a = {
        'name':"Samir"
    }
    return jsonify(a)
@app.route("/uploadpdf", methods=["POST"])
def upload_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files["pdf_file"]

    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if pdf_file:
        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()

            return jsonify({"text_from_pdf": text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
@app.route("/extract_links_from_pdf", methods=["POST"])
def extract_links_from_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    pdf_file = request.files["pdf_file"]

    if pdf_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if pdf_file:
        try:
            links = extract_links(pdf_file)
            return jsonify({"links_from_pdf": links})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
def extract_links(pdf_file):
    links = []
    
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_text = page.extractText()
        
        # Use regular expression to find links in the text
        link_pattern = r'https?://\S+|www\.\S+'
        page_links = re.findall(link_pattern, page_text)
        links.extend(page_links)
    
    return links
@app.route("/extract_resume_info", methods=["POST"])
def extract_resume_info():
    if "resume_file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    resume_file = request.files["resume_file"]

    if resume_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if resume_file:
        try:
            resume_info = pyresparser.extract_text(resume_file)
            return jsonify(resume_info)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
if(__name__) == "__main__":
    app.run(debug=True)