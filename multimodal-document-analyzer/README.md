# Multimodal Document Analyzer - Comprehensive AI-Powered System

## 📋 Overview

Multimodal Document Analyzer is a production-ready, AI-powered application that intelligently analyzes documents containing multiple data types including text, images, tables, charts, graphs, scanned PDFs, and handwritten content.

The system extracts information, understands document context, answers questions, and generates comprehensive insights using state-of-the-art machine learning models.

### 🎯 Key Features

- **Multi-Format Support**: PDF, JPG, PNG, DOCX, TXT
- **OCR Capabilities**: Read scanned PDFs, handwritten text, and low-quality images
- **Table Extraction**: Extract and convert tables to structured formats
- **Image Analysis**: Understand charts, diagrams, and embedded images
- **NLP Analysis**: Summarization, keyword extraction, entity recognition, sentiment analysis
- **Document Q&A**: Ask questions and get intelligent answers
- **Interactive Chat**: Remember context, follow-up questions, chat history
- **User Management**: Login, registration, document history
- **Report Generation**: PDF, HTML, Text, and JSON reports
- **Dark Mode**: User-friendly interface with theme options

---

## 🏗️ Architecture

### System Design

```
User Interface (Streamlit)
        ↓
Document Upload & Processing
        ↓
Multi-Modal Processing Pipeline
├── PDF Extraction
├── OCR Engine
├── Image Analysis
├── Table Extraction
└── Text Cleaning
        ↓
AI Analysis Engine
├── Summarization
├── Keyword Extraction
├── Entity Recognition
├── Topic Modeling
└── Sentiment Analysis
        ↓
Question Answering System
        ↓
Database Storage
        ↓
Report Generation
```

### Technology Stack

**Frontend:**
- Streamlit (Web UI)

**Backend:**
- Python 3.10+

**AI/ML Models:**
- HuggingFace Transformers (NLP)
- BERT (Entity Recognition)
- Vision Transformers (Image Analysis)
- EasyOCR / Tesseract (OCR)

**Document Processing:**
- pdfplumber (PDF extraction)
- PyMuPDF (PDF rendering)
- OpenCV (Image processing)
- Pillow (Image manipulation)

**Data Processing:**
- Pandas (Data manipulation)
- NumPy (Numerical operations)

**Database:**
- SQLite (Local storage)

**Deployment:**
- Docker
- Streamlit Cloud

---

## 📁 Project Structure

```
multimodal-document-analyzer/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This file
│
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── pdf_reader.py              # PDF extraction and processing
│   ├── image_reader.py            # Image loading and preprocessing
│   ├── ocr_engine.py              # OCR for scanned documents
│   ├── table_extractor.py         # Table extraction and conversion
│   ├── text_cleaner.py            # Text preprocessing utilities
│   ├── summarizer.py              # Text summarization and analysis
│   ├── qa_engine.py               # Question answering system
│   └── report_generator.py        # Report generation (PDF, HTML, etc.)
│
├── models/                         # AI models and orchestration
│   ├── __init__.py
│   └── document_model.py          # Main document analyzer orchestrator
│
├── database/                       # Database layer
│   ├── __init__.py
│   └── db.py                      # SQLite database manager
│
├── uploads/                        # Uploaded documents (auto-created)
├── reports/                        # Generated reports (auto-created)
│
└── tests/                          # Unit and integration tests
    ├── __init__.py
    └── test_components.py         # Component tests

```

### Folder Descriptions

- **app.py**: Main Streamlit application with complete UI. Handles user authentication, document upload, analysis display, Q&A interface, and report generation.

- **utils/**: Utility modules for specialized tasks
  - `pdf_reader.py`: Extracts text and metadata from PDF files using PyMuPDF and PyPDF2
  - `image_reader.py`: Loads images, applies preprocessing, enhancement for OCR
  - `ocr_engine.py`: Performs OCR on scanned documents using EasyOCR and Tesseract
  - `table_extractor.py`: Extracts tables from PDFs and converts to DataFrames
  - `text_cleaner.py`: Normalizes text, removes noise, handles special characters
  - `summarizer.py`: Generates summaries, extracts keywords, entities, topics using transformers
  - `qa_engine.py`: Provides context-aware question answering functionality
  - `report_generator.py`: Generates professional reports in multiple formats

- **models/**: AI orchestration
  - `document_model.py`: Main orchestrator that combines all components for end-to-end analysis

- **database/**: Data persistence
  - `db.py`: SQLite database manager for users, documents, analysis results, and chat history

- **uploads/**: Temporary storage for uploaded documents

- **reports/**: Generated analysis reports in various formats

- **tests/**: Test suite covering all major components

---

## ⚙️ Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- (Optional) Tesseract OCR engine for advanced OCR
- (Optional) Docker and Docker Compose for containerized deployment

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/multimodal-document-analyzer.git
cd multimodal-document-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install Tesseract OCR (Optional but Recommended)**

   **Windows:**
   - Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
   - Run installer
   - Update path in environment variables

   **macOS:**
   ```bash
   brew install tesseract
   ```

   **Linux:**
   ```bash
   sudo apt-get install tesseract-ocr
   ```

5. **Download NLP models**
```bash
python -m nltk.downloader punkt stopwords
```

6. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

---

## 🚀 Usage

### Basic Workflow

1. **Register/Login**
   - Create a new account or log in with existing credentials
   - Your documents and analysis history will be saved

2. **Upload Document**
   - Go to "Upload" page
   - Select document (PDF, JPG, PNG, DOCX, TXT)
   - Click "Analyze Document"

3. **View Results**
   - Navigate to "Analysis" page
   - View summary, keywords, entities, sentiment, statistics, tables

4. **Ask Questions**
   - Use "Chat" section to ask questions
   - System provides context-aware answers
   - Chat history is maintained

5. **Generate Reports**
   - Go to "Reports" page
   - Select report formats (PDF, HTML, Text, JSON)
   - Download reports

6. **Manage Documents**
   - View upload history
   - Search previous documents

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start container
docker-compose up -d

# Stop container
docker-compose down

# View logs
docker-compose logs -f
```

Access application at `http://localhost:8501`

### Using Docker

```bash
# Build image
docker build -t document-analyzer:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/reports:/app/reports \
  document-analyzer:latest

# Access at http://localhost:8501
```

---

## ☁️ Streamlit Cloud Deployment

1. Push code to GitHub repository
2. Go to https://share.streamlit.io
3. Select repository and main file (app.py)
4. Click "Deploy"

**Note:** Streamlit Cloud has limitations for large models. Consider using Docker deployment for production.

---

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/test_components.py -v
```

Run specific test:
```bash
python -m pytest tests/test_components.py::TestTextCleaner::test_clean_text -v
```

---

## 📊 Key Components Explained

### PDF Reader (`pdf_reader.py`)
- Extracts text from both modern and scanned PDFs
- Handles multi-page documents
- Extracts metadata and images
- Supports fallback methods if primary fails

### OCR Engine (`ocr_engine.py`)
- Uses EasyOCR for better accuracy with handwriting
- Falls back to Tesseract if needed
- Handles low-quality images through preprocessing
- Provides confidence scores for extracted text

### Table Extractor (`table_extractor.py`)
- Identifies and extracts tables from PDFs
- Converts to Pandas DataFrames for analysis
- Exports tables to CSV, JSON, HTML formats
- Handles merged cells and complex layouts

### Summarizer (`summarizer.py`)
- Generates abstractive summaries using transformer models
- Extracts keywords using TF-IDF
- Performs NER for entity extraction
- Analyzes sentiment (positive, negative, neutral)
- Detects main topics
- Calculates readability metrics

### QA Engine (`qa_engine.py`)
- Uses fine-tuned BERT models for question answering
- Retrieves relevant passages based on question
- Provides confidence scores
- Supports multi-turn conversation
- Maintains chat context

### Report Generator (`report_generator.py`)
- Generates professional PDF reports
- Creates interactive HTML reports
- Exports data as JSON for integration
- Generates plain text summaries

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```
# Database
DATABASE_PATH=analyzer.db

# Model Settings
USE_EASYOCR=true
OCR_LANGUAGES=en,es,fr

# Upload Settings
MAX_FILE_SIZE=100MB
ALLOWED_FORMATS=pdf,jpg,png,docx,txt
```

### Streamlit Configuration

Edit `.streamlit/config.toml`:
```
[theme]
primaryColor = "#1f4788"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
maxUploadSize = 200
```

---

## 🚨 Troubleshooting

### OCR Not Working
- **Issue**: Tesseract not found
- **Solution**: Install tesseract-ocr or set PYTESSERACT_PATH environment variable

### Low PDF Extraction Quality
- **Issue**: Text not extracting from scanned PDFs
- **Solution**: Enable OCR through EasyOCR in settings

### Memory Issues with Large Files
- **Issue**: Application crashes with large PDFs
- **Solution**: Process documents in chunks or increase available memory

### Slow Analysis
- **Issue**: Analysis takes too long
- **Solution**: Reduce model complexity or use GPU acceleration (if available)

---

## 📈 Performance Optimization

1. **GPU Support**: Install CUDA for faster model inference
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Model Quantization**: Use smaller, quantized models for faster inference

3. **Caching**: Results are cached to avoid re-processing

4. **Batch Processing**: Process multiple documents efficiently

---

## 🔒 Security Considerations

- **Passwords**: Hashed using SHA256 (consider bcrypt for production)
- **File Upload**: Validate file types and sizes
- **Database**: Use encrypted SQLite database for sensitive data
- **API Keys**: Store securely using environment variables
- **HTTPS**: Use SSL/TLS in production deployment

---

## 📚 Dependencies Overview

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **opencv-python**: Image processing
- **pillow**: Image manipulation

### OCR & Document Processing
- **easyocr**: Advanced OCR with handwriting support
- **pytesseract**: Tesseract interface
- **pdfplumber**: PDF table extraction
- **PyPDF2**: PDF manipulation
- **pymupdf**: PDF rendering
- **python-docx**: DOCX file handling

### NLP & Machine Learning
- **transformers**: HuggingFace transformers for NLP tasks
- **torch**: PyTorch deep learning framework
- **nltk**: Natural language toolkit
- **sentence-transformers**: Sentence embeddings for retrieval

### Report Generation
- **reportlab**: PDF generation

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

---

## 📄 License

This project is licensed under MIT License - see LICENSE file for details.

---

## 🙋 Support & Issues

For issues and feature requests:
1. Check existing GitHub issues
2. Create detailed issue report
3. Include error logs and reproduction steps
4. Attach sample documents if applicable

---

## 🔄 Version History

### v1.0 (Current)
- Initial release
- Core document analysis features
- User authentication
- Report generation
- Q&A system

### Planned Features (v2.0)
- Multi-language support
- Advanced chart recognition
- Handwriting signature verification
- Batch document processing
- API endpoint
- Advanced permission system

---

## 📞 Contact

For support and inquiries:
- Email: support@documentanalyzer.com
- Documentation: https://documentanalyzer.com/docs
- GitHub Issues: https://github.com/yourusername/multimodal-document-analyzer/issues

---

## 🎓 Learn More

- [Streamlit Documentation](https://docs.streamlit.io)
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)

---

**Made with ❤️ using AI and Modern ML Technologies**
