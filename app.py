import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from utils.extractor import extract_text
from utils.search_engine import build_index, search_index, save_precomputed, load_precomputed
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process file
            extracted_data = extract_text(filepath)
            if not extracted_data:
                flash("Could not extract text from file.")
                return redirect(request.url)
                
            # Build index
            index, chunks = build_index(extracted_data)
            
            # Save processed data
            base_filename = os.path.splitext(filename)[0]
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], base_filename)
            save_precomputed(index, chunks, processed_path)
            
            return redirect(url_for('analysis', filename=base_filename))
            
    return render_template('index.html')

@app.route('/analysis/<filename>')
def analysis(filename):
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    if not os.path.exists(processed_path + ".chunks"):
        flash("Analysis not found for this file.")
        return redirect(url_for('index'))
    return render_template('analysis.html', filename=filename)

@app.route('/search/<filename>', methods=['POST'])
def search(filename):
    query = request.form.get('query')
    search_type = request.form.get('type', 'semantic')
    
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    index, chunks = load_precomputed(processed_path)
    
    if not index or not chunks:
        return jsonify({'error': 'Data not found'}), 404
        
    results = []
    if search_type == 'semantic':
        results = search_index(query, index, chunks)
    else:
        # Simple keyword search
        for chunk in chunks:
            if query.lower() in chunk['text'].lower():
                results.append({
                    'text': chunk['text'], 
                    'page': chunk['page'],
                    'score': 1.0
                })
                
    return jsonify({'results': results})

@app.route('/download/<filename>')
def download(filename):
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    _, chunks = load_precomputed(processed_path)
    
    if not chunks:
        flash("No data to download.")
        return redirect(url_for('index'))
    
    # Create structured DataFrame
    data = []
    for chunk in chunks:
        data.append({
            'Page': chunk.get('page', 'N/A'),
            'Content': chunk.get('text', '')
        })
        
    df = pd.DataFrame(data)
    output = io.BytesIO()
    # UTF-8 with BOM (utf-8-sig) ensures Excel opens it correctly with special chars
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name=f'{filename}_report.csv')

if __name__ == '__main__':
    app.run(debug=True)
