from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
from fpdf import FPDF
from model.predict import predict_varicose  # Import the prediction function
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to fix frontend-backend connection issue

UPLOAD_FOLDER = 'static/uploads/'
REPORT_FOLDER = 'static/reports/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Preprocessing Function (Resize Image to 640x640)
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (640, 640))  # Resize to 640x640
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = cv2.equalizeHist(img)  # Apply histogram equalization
    img = img / 255.0  # Normalize pixel values
    return img

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Preprocess image
    processed_image = preprocess_image(filepath)

    # Run the model for prediction
    prediction, confidence, processed_img_path = predict_varicose(filepath)

    # Generate report
    report_filename = generate_report(filepath, prediction, confidence, processed_img_path)

    return jsonify({
        'filename': filename,
        'prediction': prediction,
        'confidence': confidence,
        'report_url': f'http://127.0.0.1:5000/download-report?filename={report_filename}'
    })

# Generate PDF Report
def generate_report(image_path, prediction, confidence, processed_img_path):
    report_filename = f"report_{os.path.basename(image_path).split('.')[0]}.pdf"
    report_path = os.path.join(REPORT_FOLDER, report_filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Varicose Vein Detection Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Result: {'Varicose Vein Detected' if prediction == 'Yes' else 'No Varicose Vein'}", ln=True)
    pdf.cell(200, 10, f"Likelihood: {confidence:.2f}%", ln=True)
    pdf.ln(10)

    # Add original image
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Original Image:", ln=True)
    pdf.image(image_path, x=10, y=None, w=100)

    pdf.ln(10)

    # Add processed image
    pdf.cell(200, 10, "Processed Image (Detected Regions):", ln=True)
    pdf.image(processed_img_path, x=10, y=None, w=100)

    pdf.output(report_path)
    return report_filename

@app.route('/download-report', methods=['GET'])
def download_report():
    filename = request.args.get('filename')
    return send_file(os.path.join(REPORT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
