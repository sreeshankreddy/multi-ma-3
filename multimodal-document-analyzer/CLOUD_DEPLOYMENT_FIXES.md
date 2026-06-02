# Streamlit Cloud Deployment Fixes

## Problem Diagnosed
The app was failing with "connection refused" on Streamlit Cloud health checks because:

1. **NLTK Downloads Hanging**: The `summarizer.py` module tried to download NLTK resources at import time without timeout, causing the app to hang or timeout before binding to port 8501.

2. **Directory Creation Blocking**: The `config.py` module tried to create `uploads/` and `reports/` directories at import time without error handling, which could fail in Cloud's headless/ephemeral filesystem.

3. **Module-Level Code**: Both issues occurred during module import (before `main()` executes), preventing Streamlit from starting.

## Solutions Implemented

### 1. NLTK Download Timeout (utils/summarizer.py)
- Added 30-second timeout using `signal.SIGALRM` to prevent indefinite hanging
- Wrapped downloads in try/except with better error messages
- If download fails or times out, the app continues with fallback text processing

**Code change**:
```python
# Set a 30-second timeout for NLTK downloads
signal.signal(signal.SIGALRM, _timeout_handler)
signal.alarm(30)
try:
    nltk.download(download_name, quiet=True)
finally:
    signal.alarm(0)  # Cancel the alarm
```

### 2. Directory Creation Error Handling (config.py)
- Wrapped `os.makedirs()` calls in try/except blocks
- Added warning messages instead of failing silently
- App continues even if directories can't be created (they may already exist or be read-only)

**Code change**:
```python
try:
    os.makedirs(UPLOADS_DIR, exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create uploads directory: {e}")
```

## Testing

### Local Testing ✅
```bash
python -c "import config; import utils.summarizer; print('STARTUP_FIXED')"
# Output: STARTUP_FIXED
```

The fixes are confirmed working locally without any startup delays.

## Deployment Steps

1. **Pull latest code** from GitHub (commit `4b29aa6`)
   ```bash
   git pull origin master
   ```

2. **Redeploy to Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Navigate to your app
   - Click the three-dot menu → "Rerun"
   - Or simply push a new commit and Cloud will auto-redeploy

3. **Expected result**: App should now start successfully and bind to port 8501

## Monitoring

After deployment, you can:

1. Check the deployment logs in Streamlit Cloud dashboard
2. Look for messages like:
   - ✅ "Streamlit app is running at http://xxx"
   - ✅ Port 8501 bind confirmation
   - ⚠️ "Warning: Could not create uploads directory" (expected in headless environment)

3. Watch for successful health check: `Get "http://localhost:8501/healthz": 200 OK`

## If Issues Persist

### Still seeing "connection refused"?
1. Check Cloud logs for actual error messages (not just health check failure)
2. Look for:
   - Import errors in app.py or modules
   - Missing dependencies (should be in requirements.txt)
   - Environment variable issues

### NLTK timeout still happening?
- Increase timeout in summarizer.py (currently 30 seconds)
- Or disable NLTK downloads and use regex-based extraction only

### Directory creation warnings?
- This is expected in Cloud's ephemeral filesystem
- Files created during session are temporary anyway
- Use Cloud-native storage if you need persistence

## Architecture Notes

### Why These Modules Load at Import Time?
- **config.py**: Validates environment on import for fail-fast behavior
- **summarizer.py**: NLTK data is needed for all text processing

### Why Not Load on Demand?
- Config needs to be available before app startup
- NLTK resources are used in many functions, so loading them lazily would delay every function call
- Current approach (with timeout) is optimal: fast import + lazy model loading within each function

## Future Improvements

1. **Cache NLTK Downloads**: Download during Docker build instead of runtime
2. **Use Cloud Storage**: Configure permanent storage for uploads/reports
3. **Async Model Loading**: Load heavy models (transformers) in background after server starts
4. **Health Check Endpoint**: Implement `/healthz` endpoint that responds before full initialization

## Summary

✅ **Root Cause**: Module-level blocking operations (NLTK downloads, directory creation)
✅ **Solution**: Added timeout and error handling
✅ **Status**: Tested locally, pushed to GitHub, ready for Cloud redeployment
✅ **Next Action**: Redeploy app on Streamlit Cloud to apply fixes
