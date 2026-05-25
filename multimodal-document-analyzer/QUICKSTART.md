"""
Quick Start Guide - Get Started in 5 Minutes
"""

# QUICK START GUIDE

## 🚀 5-Minute Setup

### Option 1: Local Installation (Recommended for Development)

```bash
# 1. Navigate to project directory
cd multimodal-document-analyzer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
streamlit run app.py
```

**Done!** Application runs at http://localhost:8501

---

### Option 2: Docker Installation (Recommended for Production)

```bash
# 1. Build and run with Docker Compose
docker-compose up -d

# 2. Access application
# Open http://localhost:8501 in browser

# 3. Stop when done
docker-compose down
```

**Done!** Application runs at http://localhost:8501

---

## 📋 First Steps

### 1. Create Account
- Go to http://localhost:8501
- Click "Register" tab
- Enter username, email, password
- Click "Register" button

### 2. Upload Document
- Go to "Upload" page
- Click file uploader
- Select document (PDF, JPG, PNG, DOCX, TXT)
- Wait for analysis to complete

### 3. View Results
- Check "Analysis" page
- Review summary, keywords, entities, tables
- View document statistics

### 4. Ask Questions
- Go to Chat section
- Ask questions like:
  - "What is this document about?"
  - "Who are the key people mentioned?"
  - "What are the main conclusions?"
- Chat history is automatically saved

### 5. Generate Report
- Go to "Reports" page
- Select formats (PDF, HTML, TXT, JSON)
- Click "Generate Reports"
- Download your reports

---

## 🔧 Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution:**
```bash
# Run on different port
streamlit run app.py --server.port=8502
```

### Issue: OCR not working
**Solution:**
```bash
# Install Tesseract (Windows)
# Download from: https://github.com/UB-Mannheim/tesseract/wiki

# Install Tesseract (macOS)
brew install tesseract

# Install Tesseract (Linux)
sudo apt-get install tesseract-ocr
```

### Issue: Out of memory
**Solution:**
```bash
# Reduce model size in config.py
USE_GPU = False
SUMMARY_MAX_LENGTH = 100  # Reduce summary length
```

---

## 📚 Project Structure Overview

```
multimodal-document-analyzer/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker setup
├── docker-compose.yml        # Docker Compose
├── config.py                 # Configuration
├── logger.py                 # Logging setup
│
├── utils/                    # Utility modules
│   ├── pdf_reader.py        # PDF processing
│   ├── image_reader.py      # Image processing
│   ├── ocr_engine.py        # OCR capabilities
│   ├── table_extractor.py   # Table extraction
│   ├── text_cleaner.py      # Text preprocessing
│   ├── summarizer.py        # NLP analysis
│   ├── qa_engine.py         # Q&A system
│   └── report_generator.py  # Report generation
│
├── models/
│   └── document_model.py    # Main analyzer
│
├── database/
│   └── db.py                # Database manager
│
├── tests/
│   └── test_components.py   # Unit tests
│
├── README.md                # Documentation
├── DEPLOYMENT.md            # Deployment guide
├── ARCHITECTURE.md          # Architecture docs
└── ADVANCED_FEATURES.md     # Advanced features
```

---

## 🎯 Common Use Cases

### Case 1: Analyze Business Report
1. Upload PDF report
2. View summary (auto-generated)
3. Extract tables for analysis
4. Get keywords and topics
5. Generate PDF report
6. Ask Q&A about specific sections

### Case 2: Batch OCR Processing
1. Scan multiple documents
2. Upload each scanned PDF
3. System applies OCR automatically
4. Extract text from scanned images
5. Get analysis and insights
6. Download all reports

### Case 3: Research Paper Analysis
1. Upload research paper (PDF)
2. View summary and key findings
3. Extract author information
4. Get sentiment analysis
5. Ask questions about methodology
6. Generate research summary report

### Case 4: Contract Review
1. Upload contract (DOCX/PDF)
2. Extract key clauses and entities
3. Identify important dates
4. Ask about specific terms
5. Generate summary document
6. Download for further review

---

## 💡 Tips & Tricks

### Optimize Analysis
- Keep documents under 50 pages for faster processing
- Ensure high-quality scanned PDFs (300+ DPI)
- Clean documents (remove watermarks if possible)

### Better Q&A Results
- Ask specific questions
- Reference sections from document
- Ask follow-up questions
- Use clear language

### Generate Better Reports
- Select all report formats
- Include custom title
- Download HTML for best formatting
- Share PDF reports easily

---

## 🔐 Security Tips

- Never share your login credentials
- Use strong passwords (12+ characters)
- Log out when finished
- Don't upload sensitive data without proper security
- Review shared reports carefully

---

## 📞 Getting Help

### Documentation
- [README.md](README.md) - Full documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [ADVANCED_FEATURES.md](ADVANCED_FEATURES.md) - Advanced setup

### Common Issues
- Check error logs: `tail -f logs/app.log`
- Verify all dependencies: `pip list`
- Test database: `sqlite3 analyzer.db "SELECT 1;"`

### Performance Monitoring
```bash
# Monitor container resources
docker stats

# View application logs
docker logs -f multimodal-document-analyzer
```

---

## 🎓 Learning Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [Python Documentation](https://docs.python.org/3/)
- [Docker Documentation](https://docs.docker.com/)

---

## ✅ Verification Checklist

After setup, verify these work:

- [ ] Application starts without errors
- [ ] Can create user account
- [ ] Can upload PDF document
- [ ] Analysis completes and shows results
- [ ] Can ask questions in chat
- [ ] Can generate PDF report
- [ ] Can view document history
- [ ] Dark mode toggle works
- [ ] Logout works correctly

---

## 🚀 Next Steps

After setup:

1. **Explore Features**
   - Test different document types
   - Try various Q&A questions
   - Generate different report formats

2. **Customize Configuration**
   - Edit `.env` file for settings
   - Adjust theme colors
   - Configure logging

3. **Set Up Monitoring**
   - Enable debug mode if needed
   - Set up log rotation
   - Monitor resource usage

4. **Deploy to Production**
   - Use Docker for consistency
   - Set up HTTPS/SSL
   - Configure backup strategy

---

## 📈 Performance Benchmarks

Expected performance on standard hardware:

| Operation | Time |
|-----------|------|
| Document upload | < 1s |
| PDF text extraction | 2-5s |
| OCR on image | 3-10s |
| Document analysis | 5-15s |
| Q&A answer | 2-5s |
| Report generation | 3-10s |

---

**Need help?** Check the documentation files or review the code comments!

**Happy analyzing!** 📄✨
