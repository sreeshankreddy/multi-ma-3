"""
System Architecture and Design Documentation
"""

# SYSTEM ARCHITECTURE DOCUMENTATION

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                   │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │  Login/Auth  │  │   Upload   │  │  Results Display     │  │
│  └──────────────┘  └────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │   History    │  │   Chat Q&A │  │  Report Generation   │  │
│  └──────────────┘  └────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Document Processing Pipeline                     │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │ File Handler │  │ PDF Reader │  │  Image Reader        │  │
│  └──────────────┘  └────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Multi-Modal Processing                          │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────────────┐  │
│  │  OCR Engine  │  │   Tables   │  │  Text Cleaning       │  │
│  │              │  │  Extraction│  │                      │  │
│  └──────────────┘  └────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              AI Analysis Engine                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │          Transformer-Based NLP Models               │    │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │    │
│  │  │Summarize │  │ Keywords │  │   Entity Ext.   │   │    │
│  │  └──────────┘  └──────────┘  └─────────────────┘   │    │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────────┐   │    │
│  │  │Sentiment │  │  Topics  │  │ Insights Gen.   │   │    │
│  │  └──────────┘  └──────────┘  └─────────────────┘   │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Question Answering System                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │      Fine-tuned BERT for Context-Aware Q&A          │    │
│  │  ┌────────────┐          ┌──────────────────────┐   │    │
│  │  │ Retriever  │ ─────→  │  Answer Generator    │   │    │
│  │  └────────────┘          └──────────────────────┘   │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Data Persistence Layer                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              SQLite Database                         │    │
│  │  ┌───────────┐  ┌──────────┐  ┌──────────────────┐  │    │
│  │  │   Users   │  │Documents │  │ Analysis Results │  │    │
│  │  └───────────┘  └──────────┘  └──────────────────┘  │    │
│  │  ┌───────────┐                                       │    │
│  │  │   Chat    │                                       │    │
│  │  │  History  │                                       │    │
│  │  └───────────┘                                       │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Component Interaction Flow

### Document Upload and Analysis

```
1. User uploads document
   ↓
2. File validation
   ├─ Check format
   ├─ Check size
   └─ Check permissions
   ↓
3. Document storage
   ├─ Save to disk
   └─ Register in database
   ↓
4. Content extraction
   ├─ PDF → Text
   ├─ Image → OCR → Text
   ├─ DOCX → Text
   └─ TXT → Direct read
   ↓
5. Pre-processing
   ├─ Text cleaning
   ├─ Normalization
   └─ Tokenization
   ↓
6. Table extraction (if applicable)
   ├─ Detect tables
   ├─ Extract structure
   └─ Convert to DataFrames
   ↓
7. AI Analysis
   ├─ Summarization
   ├─ Keyword extraction
   ├─ NER
   ├─ Topic modeling
   └─ Sentiment analysis
   ↓
8. Results storage
   ├─ Save analysis results
   ├─ Index for search
   └─ Generate metadata
   ↓
9. Display to user
   ├─ Show summary
   ├─ Display tables
   ├─ Show entities
   └─ Enable Q&A
```

### Question Answering Flow

```
1. User asks question
   ↓
2. Context retrieval
   ├─ Find relevant passages
   ├─ Score by relevance
   └─ Select top-k passages
   ↓
3. Answer generation
   ├─ Format context
   ├─ Run QA model
   └─ Score confidence
   ↓
4. Post-processing
   ├─ Extract answer
   ├─ Format response
   └─ Add confidence
   ↓
5. Store in chat history
   ├─ Save question
   ├─ Save answer
   └─ Save timestamp
   ↓
6. Display to user
```

## Data Flow

### Document Storage

```
Upload
  ↓
Validation
  ↓
Temporary Storage (/uploads)
  ↓
Content Extraction
  ↓
Database Registration
```

### Analysis Results Storage

```
Analysis
  ↓
Structured Results
  ↓
JSON Serialization
  ↓
Database Storage
  ↓
Cache (Optional)
```

## Module Dependencies

```
app.py (Streamlit Frontend)
├── models/
│   └── document_model.py
│       ├── utils/pdf_reader.py
│       ├── utils/image_reader.py
│       ├── utils/ocr_engine.py
│       ├── utils/table_extractor.py
│       ├── utils/text_cleaner.py
│       ├── utils/summarizer.py
│       └── utils/qa_engine.py
├── database/
│   └── db.py
└── utils/
    └── report_generator.py
```

## Data Model

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    password_hash VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Documents Table
```sql
CREATE TABLE documents (
    id INT PRIMARY KEY,
    user_id INT FOREIGN KEY,
    filename VARCHAR,
    file_path VARCHAR,
    file_type VARCHAR,
    upload_date TIMESTAMP,
    file_size INT
);
```

### Analysis Results Table
```sql
CREATE TABLE analysis_results (
    id INT PRIMARY KEY,
    document_id INT FOREIGN KEY,
    summary TEXT,
    keywords TEXT (JSON),
    entities TEXT (JSON),
    topics TEXT (JSON),
    sentiment TEXT,
    extracted_text TEXT,
    tables TEXT (JSON),
    analysis_date TIMESTAMP
);
```

### Chat History Table
```sql
CREATE TABLE chat_history (
    id INT PRIMARY KEY,
    document_id INT FOREIGN KEY,
    user_question TEXT,
    ai_response TEXT,
    timestamp TIMESTAMP
);
```

## Processing Pipelines

### Text Processing Pipeline

```
Raw Text
  ↓
Normalization (Unicode)
  ↓
Cleaning (whitespace, special chars)
  ↓
Tokenization
  ↓
Stop word removal
  ↓
Processed Text
```

### NLP Analysis Pipeline

```
Processed Text
  ├─→ Summarization Model (BART)
  │   └─→ Summary
  ├─→ Keyword Extraction (TF-IDF)
  │   └─→ Keywords
  ├─→ NER Model (BERT)
  │   └─→ Entities
  ├─→ Sentiment Model (DistilBERT)
  │   └─→ Sentiment
  └─→ Topic Extraction
      └─→ Topics
```

### OCR Pipeline

```
Image
  ↓
Quality Assessment
  ↓
Preprocessing
├─ Grayscale conversion
├─ Contrast enhancement (CLAHE)
├─ Denoising
└─ Thresholding
  ↓
OCR (EasyOCR / Tesseract)
  ↓
Text Extraction
  ├─ Full text
  ├─ Confidence scores
  └─ Bounding boxes
  ↓
Post-processing
  ├─ Correction
  └─ Formatting
```

## Error Handling

```
User Action
  ↓
Validation
├─ Success → Proceed
└─ Failure → User Error Message
  ↓
Processing
├─ Success → Continue
├─ Recoverable Error → Fallback
└─ Fatal Error → Admin Alert
  ↓
Storage
├─ Success → Confirm
└─ Failure → Log & Notify User
```

## Scalability Considerations

### Horizontal Scaling

```
Load Balancer
├─ Instance 1
│  ├─ Streamlit App
│  └─ Local Cache
├─ Instance 2
│  ├─ Streamlit App
│  └─ Local Cache
└─ Instance N
   ├─ Streamlit App
   └─ Local Cache
   ↓
Shared Database
```

### Caching Strategy

```
User Request
  ↓
Check Local Cache
├─ Hit → Return cached
└─ Miss → Check Redis
    ├─ Hit → Update local, return
    └─ Miss → Process & cache
```

## Performance Optimization

### Model Optimization

```
Full Model (4GB)
  ↓
Quantization (1GB)
  ↓
Distillation (512MB)
  ↓
Pruning (256MB)
```

### Text Chunking

```
Large Document (100K tokens)
  ↓
Split into chunks (512 tokens each)
  ↓
Process chunks independently
  ↓
Aggregate results
```

## Security Architecture

```
Public Internet
  ↓
HTTPS/SSL
  ↓
Load Balancer
  ↓
Web Server (Nginx)
  ↓
Streamlit App
  ↓
Authentication Layer
├─ JWT validation
└─ Permission check
  ↓
Business Logic
  ↓
Database Layer
└─ Parameterized queries
```

## Monitoring and Logging

```
Application Events
  ↓
Logger
├─ Console output
├─ File logging (rotating)
└─ External service (optional)
  ↓
Metrics Collection
├─ Performance metrics
├─ Error rates
└─ User analytics
  ↓
Dashboard/Alerts
```

## Deployment Architecture

### Local Development
```
Developer Machine
├─ Python Virtual Environment
├─ SQLite Database
└─ Running Streamlit App
```

### Docker Container
```
Docker Image
└─ Container
   ├─ Python Runtime
   ├─ Dependencies
   ├─ Application Code
   └─ Volume Mounts (data)
```

### Kubernetes Cluster
```
Kubernetes Cluster
├─ Ingress Controller (HTTPS)
├─ Service (Load Balancer)
├─ Deployment (3 replicas)
│  ├─ Pod 1
│  ├─ Pod 2
│  └─ Pod 3
├─ StatefulSet (Database)
└─ ConfigMap/Secrets
```

## Integration Points

### External Services

```
Application
├─ Email Service (SMTP)
│  └─ Send notifications
├─ Cloud Storage (S3, GCS)
│  └─ Backup reports
├─ Analytics Service (GA, Mixpanel)
│  └─ Track usage
└─ Logging Service (ELK, Datadog)
   └─ Centralized logging
```

This architecture provides scalability, maintainability, and robustness
for production-ready document analysis system.
