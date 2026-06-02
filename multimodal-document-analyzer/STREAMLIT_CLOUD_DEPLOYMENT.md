# Streamlit Cloud Deployment Guide

## Overview
This guide explains how to deploy the Multimodal Document Analyzer to Streamlit Cloud.

## Prerequisites
- GitHub account with the repository cloned
- Streamlit Cloud account (free tier available at https://streamlit.io/cloud)
- GrokAI API key (optional, for enhanced QA capabilities)

## Step 1: Push Code to GitHub
The code is already pushed to: https://github.com/sreeshankreddy/multi-ma-3

## Step 2: Configure Secrets on Streamlit Cloud

Since the `.env` file is not tracked by Git (for security), you need to set environment variables as secrets in Streamlit Cloud:

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select repository: `sreeshankreddy/multi-ma-3`
4. Select branch: `master`
5. Select main file path: `multimodal-document-analyzer/app.py`
6. Click "Deploy"

After initial deployment:

7. In the app settings (gear icon), go to "Secrets"
8. Add the following secrets (copy from `.env.example`):

```
GROKAI_API_KEY=your_grokai_api_key_here
UPLOADS_DIR=uploads
REPORTS_DIR=reports
DATABASE_PATH=analyzer.db
USE_EASYOCR=true
OCR_LANGUAGES=en
MAX_FILE_SIZE_MB=200
ALLOWED_FORMATS=pdf,jpg,jpeg,png,docx,txt
STREAMLIT_PORT=8501
STREAMLIT_THEME=light
MODEL_DEVICE=cpu
MAX_FAILED_ATTEMPTS=5
SESSION_TIMEOUT_MINUTES=30
API_ENABLE=false
API_PORT=8000
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
SUMMARY_MAX_LENGTH=150
SUMMARY_MIN_LENGTH=50
NUM_KEYWORDS=15
NUM_TOPICS=5
QA_CONFIDENCE_THRESHOLD=0.3
QA_MAX_ANSWER_LENGTH=256
ENABLE_CHAT=true
ENABLE_REPORTS=true
ENABLE_API=false
ENABLE_BATCH_PROCESSING=false
```

## Step 3: Configure Advanced Settings

In app settings:
- **Python version**: 3.14+
- **CPU memory**: 1 GB (minimum)
- **Client error details**: On (for debugging)

## Important Notes

### Database Storage
- The SQLite database (`analyzer.db`) is created in the app's filesystem
- Files are temporary and may be reset when the app restarts
- For persistent data, consider using a cloud database (PostgreSQL, MongoDB, etc.)

### File Uploads
- Streamlit Cloud has file size limits
- Uploaded files are temporarily stored during the session
- Clean up happens after the session ends

### Performance
- Large PDF files may take longer to process
- OCR operations are CPU-intensive
- Consider enabling GPU if available in your Streamlit Cloud tier

### Troubleshooting

#### "Connection refused" error
- Ensure all environment variables are set in Secrets
- Check that `GROKAI_API_KEY` is properly configured
- Verify the app.py path is correct: `multimodal-document-analyzer/app.py`

#### App not starting
1. Check the logs in Streamlit Cloud dashboard
2. Verify all required dependencies are in `requirements.txt`
3. Ensure Python version is compatible (3.10+)

#### Missing modules
- All dependencies should be automatically installed from `requirements.txt`
- If you see import errors, check that the module versions are compatible

## Local Development

To test locally before deploying:

```bash
cd multimodal-document-analyzer
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Next Steps

1. Customize the app branding in `.streamlit/config.toml`
2. Add more document formats if needed
3. Implement persistent database (optional)
4. Monitor app performance and user feedback

## Support

For issues or questions:
- Check Streamlit documentation: https://docs.streamlit.io
- Review app logs in Streamlit Cloud dashboard
- Check GitHub issues: https://github.com/sreeshankreddy/multi-ma-3/issues
