from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import pandas as pd
import os
from werkzeug.utils import secure_filename
from classify import classify
PORT = int(os.environ.get("PORT", "5000"))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'csv'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "log-classification-api"})

@app.route('/classify', methods=['POST'])
def classify_logs():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check if file is CSV
        if not allowed_file(file.filename):
            return jsonify({"error": "File must be a CSV"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read CSV
        df = pd.read_csv(filepath)
        
        # Check required columns
        if "source" not in df.columns or "log_message" not in df.columns:
            return jsonify({"error": "CSV must contain 'source' and 'log_message' columns"}), 400
        
        # Perform classification
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))
        
        # Save output file
        output_filename = f"classified_{filename}"
        output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        df.to_csv(output_filepath, index=False)
        
        # Return the file
        return send_file(
            output_filepath,
            as_attachment=True,
            download_name=output_filename,
            mimetype='text/csv'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
