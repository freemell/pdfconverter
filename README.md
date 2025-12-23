# Milla pdf converter (ITS FUCKING FREE)

A simple web application that converts Word documents (.doc, .docx) to PDF format - completely free!

## Features

- Clean, modern user interface
- Drag and drop file upload
- Click to select files
- Automatic PDF download after conversion
- Supports .doc and .docx files up to 16MB

## Prerequisites

- Python 3.7 or higher

### Conversion Methods

The application supports two conversion methods:

**Method 1: docx2pdf (Recommended for Windows)**
- Requires Microsoft Word to be installed
- Works best on Windows
- Automatically used if available

**Method 2: pypandoc (Cross-platform)**
- Requires Pandoc to be installed
- Works on Windows, macOS, and Linux

### Installing Pandoc (Optional, for pypandoc method)

**Windows:**
1. Download from [pandoc.org/installing.html](https://pandoc.org/installing.html)
2. Or use Chocolatey: `choco install pandoc`

**macOS:**
```bash
brew install pandoc
```

**Linux:**
```bash
sudo apt-get install pandoc
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. **For Windows users:** Make sure Microsoft Word is installed (for docx2pdf)

3. **For other platforms or if you prefer pypandoc:** Install Pandoc (see Prerequisites above)

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload a Word document (.doc or .docx) and click "Convert to PDF"

4. The PDF will automatically download when conversion is complete

## Troubleshooting

**"No conversion library available" error:**
- On Windows: Make sure Microsoft Word is installed
- For pypandoc: Make sure Pandoc is installed and in your system PATH

**Conversion fails:**
- Make sure the Word document is not corrupted
- Try a different Word document to test
- Check that you have write permissions in the temp directory

## Notes

- The application uses temporary files that are automatically cleaned up
- Maximum file size is 16MB (configurable in `app.py`)
- The server runs in debug mode by default (change for production)

