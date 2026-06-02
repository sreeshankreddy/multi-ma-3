#!/usr/bin/env python
"""Test analysis pipeline to identify issues."""

import sys
import traceback

try:
    from utils.text_cleaner import TextCleaner
    from utils.summarizer import DocumentSummarizer
    
    test_text = "This is a test document. It contains multiple sentences. Each sentence has some meaning. We need to test the summarizer. The analysis should work properly. This paragraph provides important information about testing. The text needs to be long enough for proper analysis. We are testing all the analysis functions. This is essential for document understanding. Finally, we complete the test text with additional content."
    
    print("=" * 60)
    print("TESTING ANALYSIS PIPELINE")
    print("=" * 60)
    
    print("\n1️⃣ Testing TextCleaner...")
    try:
        cleaner = TextCleaner()
        cleaned = cleaner.clean_text(test_text)
        print(f"✅ Cleaned text: {cleaned[:100]}...")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n2️⃣ Testing DocumentSummarizer initialization...")
    try:
        summarizer = DocumentSummarizer()
        print(f"✅ Summarizer initialized")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n3️⃣ Testing summarize_text...")
    try:
        summary = summarizer.summarize_text(cleaned)
        print(f"✅ Summary: {summary}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n4️⃣ Testing extract_keywords...")
    try:
        keywords = summarizer.extract_keywords(cleaned)
        print(f"✅ Keywords: {keywords}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n5️⃣ Testing extract_entities...")
    try:
        entities = summarizer.extract_entities(cleaned)
        print(f"✅ Entities: {entities}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n6️⃣ Testing extract_topics...")
    try:
        topics = summarizer.extract_topics(cleaned)
        print(f"✅ Topics: {topics}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n7️⃣ Testing generate_bullet_points...")
    try:
        bullets = summarizer.generate_bullet_points(cleaned)
        print(f"✅ Bullets: {bullets}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n8️⃣ Testing analyze_sentiment...")
    try:
        sentiment = summarizer.analyze_sentiment(cleaned)
        print(f"✅ Sentiment: {sentiment}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n9️⃣ Testing extract_important_phrases...")
    try:
        phrases = summarizer.extract_important_phrases(cleaned)
        print(f"✅ Phrases: {phrases}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n🔟 Testing get_document_statistics...")
    try:
        stats = summarizer.get_document_statistics(cleaned)
        print(f"✅ Stats: {stats}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    traceback.print_exc()
