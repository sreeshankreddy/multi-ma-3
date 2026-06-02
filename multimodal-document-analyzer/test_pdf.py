#!/usr/bin/env python
"""Test PDF extraction pipeline."""

import os
import sys
from pathlib import Path

try:
    from utils.pdf_reader import PDFReader
    from models.document_model import DocumentAnalyzer
    
    print("=" * 60)
    print("TESTING PDF EXTRACTION")
    print("=" * 60)
    
    # Look for test PDFs in reports or uploads
    test_pdfs = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pdf'):
                test_pdfs.append(os.path.join(root, file))
    
    if not test_pdfs:
        print("❌ No PDF files found for testing")
        print("Please upload a PDF to the application first")
        sys.exit(1)
    
    print(f"\n📄 Found {len(test_pdfs)} PDF(s) for testing:")
    for pdf in test_pdfs[:3]:  # Test first 3
        print(f"  • {pdf}")
    
    # Test each PDF
    for pdf_path in test_pdfs[:1]:  # Test first one
        print(f"\n📖 Testing: {pdf_path}")
        print("-" * 60)
        
        try:
            print("1️⃣ Testing PDFReader.extract_text()...")
            reader = PDFReader()
            text, page_info = reader.extract_text(pdf_path)
            print(f"✅ Extracted {len(text)} characters from {len(page_info)} pages")
            print(f"   First page preview: {text[:200]}...")
            
            if len(text) < 50:
                print(f"⚠️  WARNING: Very short text extracted ({len(text)} chars)")
            
            print("\n2️⃣ Testing DocumentAnalyzer.load_document()...")
            analyzer = DocumentAnalyzer()
            success, result_text = analyzer.load_document(pdf_path)
            print(f"✅ Load result: {success}")
            print(f"   Extracted text length: {len(analyzer.extracted_text)} chars")
            print(f"   Document metadata: {analyzer.document_metadata}")
            
            if success and analyzer.extracted_text:
                print("\n3️⃣ Testing full analysis...")
                results = analyzer.analyze_text()
                
                if 'error' in results:
                    print(f"❌ Analysis error: {results['error']}")
                else:
                    print(f"✅ Analysis successful!")
                    for key in ['summary', 'keywords', 'entities', 'topics', 'sentiment']:
                        value = results.get(key)
                        if isinstance(value, str):
                            print(f"   • {key}: {value[:50]}...")
                        elif isinstance(value, list):
                            print(f"   • {key}: {len(value)} items")
                        elif isinstance(value, dict):
                            print(f"   • {key}: {len(value)} keys")
                        else:
                            print(f"   • {key}: {type(value).__name__}")
            else:
                print(f"❌ Failed to load document: {result_text}")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ PDF EXTRACTION TEST COMPLETED!")
    print("=" * 60)

except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
