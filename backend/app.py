from flask import Flask, request, jsonify, send_file
import os
from model.predict import predict_varicose
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
@cross_origin() 
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    prediction = predict_varicose(filepath)

    return jsonify({'filename': filename, 'prediction': prediction})

@app.route('/download-report', methods=['GET'])
@cross_origin() 
def download_report():
    return send_file("static/report.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
