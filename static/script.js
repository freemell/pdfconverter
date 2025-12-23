const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadForm = document.getElementById('uploadForm');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');
const convertBtn = document.getElementById('convertBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const errorMessage = document.getElementById('errorMessage');

// Click to select file
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    if (e.dataTransfer.files.length > 0) {
        const file = e.dataTransfer.files[0];
        if (file.name.endsWith('.doc') || file.name.endsWith('.docx')) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect(file);
        } else {
            showError('Please select a .doc or .docx file');
        }
    }
});

// Handle file selection
function handleFileSelect(file) {
    fileName.textContent = file.name;
    fileInfo.style.display = 'flex';
    convertBtn.disabled = false;
    hideError();
}

// Remove file
removeFileBtn.addEventListener('click', () => {
    fileInput.value = '';
    fileInfo.style.display = 'none';
    convertBtn.disabled = true;
    hideError();
});

// Form submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!fileInput.files.length) {
        showError('Please select a file first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    // Show loading state
    convertBtn.disabled = true;
    btnText.textContent = 'Converting...';
    btnLoader.style.display = 'block';
    hideError();
    
    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            // Get the PDF file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = fileInput.files[0].name.replace(/\.(doc|docx)$/i, '.pdf');
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            // Reset form
            fileInput.value = '';
            fileInfo.style.display = 'none';
            convertBtn.disabled = true;
            btnText.textContent = 'Convert to PDF';
            btnLoader.style.display = 'none';
        } else {
            const error = await response.json();
            showError(error.error || 'Conversion failed. Please try again.');
        }
    } catch (error) {
        showError('An error occurred. Please try again.');
    } finally {
        convertBtn.disabled = false;
        btnText.textContent = 'Convert to PDF';
        btnLoader.style.display = 'none';
    }
});

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

