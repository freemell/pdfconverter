from flask import Flask, request, send_file, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import sys

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

ALLOWED_EXTENSIONS = {'docx', 'doc'}

# Try to import conversion libraries
try:
    from docx2pdf import convert as docx2pdf_convert
    HAS_DOCX2PDF = True
except ImportError:
    HAS_DOCX2PDF = False

try:
    import pypandoc
    HAS_PYPANDOC = True
except ImportError:
    HAS_PYPANDOC = False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a .docx or .doc file'}), 400
    
    input_path = None
    output_path = None
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Convert to PDF
        output_filename = os.path.splitext(filename)[0] + '.pdf'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Try different conversion methods
        if HAS_DOCX2PDF and filename.lower().endswith('.docx'):
            # Method 1: docx2pdf (Windows, requires Microsoft Word)
            docx2pdf_convert(input_path, output_path)
        elif HAS_PYPANDOC:
            # Method 2: pypandoc (requires pandoc and a PDF engine)
            try:
                pypandoc.convert_file(
                    input_path,
                    'pdf',
                    outputfile=output_path
                )
            except Exception as e:
                # Try with different PDF engines
                for engine in ['wkhtmltopdf', 'pdflatex', 'xelatex']:
                    try:
                        pypandoc.convert_file(
                            input_path,
                            'pdf',
                            outputfile=output_path,
                            extra_args=[f'--pdf-engine={engine}']
                        )
                        break
                    except:
                        continue
                else:
                    raise e
        else:
            return jsonify({
                'error': 'No conversion library available. Please install docx2pdf (Windows) or pypandoc (requires pandoc)'
            }), 500
        
        # Verify output file was created
        if not os.path.exists(output_path):
            raise Exception('PDF file was not created')
        
        # Clean up input file
        if os.path.exists(input_path):
            os.remove(input_path)
        
        # Send PDF file
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        # Clean up on error
        if input_path and os.path.exists(input_path):
            os.remove(input_path)
        if output_path and os.path.exists(output_path):
            os.remove(output_path)
        
        error_msg = str(e)
        if 'No conversion library' not in error_msg:
            error_msg = f'Conversion failed: {error_msg}'
        
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

