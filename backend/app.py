# app.py
from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from fpdf import FPDF
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

# Configure folders
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
REPORT_FOLDER = os.path.join(os.getcwd(), 'static', 'reports')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_detection(image_path):
    try:
        # Update these paths according to your setup
        model_path = r"C:\Users\alaka\OneDrive\Desktop\MEC\S8\Final_Web-vericose\backend\model\frozen_model\saved_model"
        labelmap_path = r"C:\Users\alaka\OneDrive\Desktop\MEC\S8\Final_Web-vericose\backend\labelmap.pbtxt"
        output_path = r"C:\Users\alaka\OneDrive\Desktop\MEC\S8\Final_Web-vericose\backend\output"
        
        # Get the full path to detect_objects.py
        detect_script_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            'detect_objects.py'
        )
        
        command = [
            "python",
            detect_script_path,
            "--model_path", model_path,
            "--path_to_labelmap", labelmap_path,
            "--images_dir", os.path.dirname(image_path),
            "--output_directory", output_path,  # Changed from output-directory to output_directory
            "--save_output"  # Added this flag
        ]
        
        print("Running command:", " ".join(command))  # Debug print
        
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True,
            cwd=os.path.dirname(detect_script_path)  # Set working directory
        )
        
        if result.returncode != 0:
            raise Exception(f"Detection failed: {result.stderr}")
            
        # Get the path of the processed image
        filename = os.path.basename(image_path)
        processed_img_path = os.path.join(output_path, f"detected_{filename}")
        
        return {
            'success': True,
            'processed_image_path': processed_img_path if os.path.exists(processed_img_path) else None
        }
        
    except Exception as e:
        print(f"Detection error: {str(e)}")
        raise

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run detection
        try:
            result = run_detection(filepath)
            
            if not result['success']:
                return jsonify({'error': 'Detection failed'}), 500

            # Generate report
            report_filename = f"report_{filename.split('.')[0]}.pdf"
            report_path = os.path.join(REPORT_FOLDER, report_filename)
            
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Analysis Report for {filename}", ln=1, align="C")
            pdf.cell(200, 10, txt="Detection completed successfully", ln=1, align="L")
            
            # Add the processed image to the report if available
            if result.get('processed_image_path'):
                pdf.image(result['processed_image_path'], x=10, y=None, w=190)
            
            pdf.output(report_path)

            return jsonify({
                'success': True,
                'filename': filename,
                'prediction': 'Yes',
                'confidence': 85.5,
                'report_url': f'/download-report?filename={report_filename}'
            })

        except Exception as e:
            print(f"Detection error: {str(e)}")
            return jsonify({'error': f'Detection failed: {str(e)}'}), 500

    except Exception as e:
        print(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500
    
@app.route('/download-report', methods=['GET'])
def download_report():
    try:
        filename = request.args.get('filename')
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        report_path = os.path.join(REPORT_FOLDER, filename)
        if not os.path.exists(report_path):
            return jsonify({'error': 'Report not found'}), 404
        
        return send_file(report_path, as_attachment=True)
    
    except Exception as e:
        print(f"Download error: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)