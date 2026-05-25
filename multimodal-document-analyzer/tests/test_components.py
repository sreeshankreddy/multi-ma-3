"""
Unit tests for document analyzer components.
"""

import unittest
import os
import tempfile
from utils.text_cleaner import TextCleaner
from utils.table_extractor import TableExtractor
import pandas as pd


class TestTextCleaner(unittest.TestCase):
    """Test TextCleaner utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.cleaner = TextCleaner()
        self.sample_text = "Hello   WORLD!  This is a TEST document with   extra   spaces."

    def test_clean_text(self):
        """Test text cleaning functionality."""
        cleaned = self.cleaner.clean_text(self.sample_text)
        self.assertNotIn("   ", cleaned)
        self.assertEqual(cleaned, "Hello WORLD! This is a TEST document with extra spaces.")

    def test_normalize_text(self):
        """Test text normalization."""
        text_with_unicode = "Hëllo Wörld"
        normalized = self.cleaner.normalize_text(text_with_unicode)
        self.assertIsInstance(normalized, str)

    def test_remove_special_characters(self):
        """Test special character removal."""
        text = "Hello@#$%World^&*()"
        cleaned = self.cleaner.remove_special_characters(text, keep_punctuation=False)
        self.assertEqual(cleaned, "HelloWorld")

    def test_split_into_sentences(self):
        """Test sentence splitting."""
        text = "First sentence. Second sentence! Third sentence?"
        sentences = self.cleaner.split_into_sentences(text)
        self.assertEqual(len(sentences), 3)

    def test_extract_numbers(self):
        """Test number extraction."""
        text = "The price is 99.99 dollars and quantity is 100."
        numbers = self.cleaner.extract_numbers(text)
        self.assertIn("99.99", numbers)
        self.assertIn("100", numbers)

    def test_extract_dates(self):
        """Test date extraction."""
        text = "The meeting is on 2024-01-15 or 01/15/2024"
        dates = self.cleaner.extract_dates(text)
        self.assertTrue(len(dates) > 0)

    def test_remove_urls(self):
        """Test URL removal."""
        text = "Visit https://example.com or http://test.org for more info"
        cleaned = self.cleaner.remove_urls(text)
        self.assertNotIn("https://", cleaned)
        self.assertNotIn("http://", cleaned)

    def test_expand_contractions(self):
        """Test contraction expansion."""
        text = "don't can't won't"
        expanded = self.cleaner.expand_contractions(text)
        self.assertIn("do not", expanded)
        self.assertIn("cannot", expanded)


class TestTableExtractor(unittest.TestCase):
    """Test TableExtractor functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.extractor = TableExtractor()
        # Create sample DataFrame
        self.sample_df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['NYC', 'LA', 'Chicago']
        })

    def test_table_statistics(self):
        """Test table statistics extraction."""
        stats = self.extractor.get_table_statistics(self.sample_df)

        self.assertEqual(stats['row_count'], 3)
        self.assertEqual(stats['column_count'], 3)
        self.assertIn('Name', stats['columns'])

    def test_clean_table_data(self):
        """Test table data cleaning."""
        # Create DataFrame with whitespace
        df = pd.DataFrame({
            'Column1': ['  value1  ', '  value2  ', '  value3  '],
            'Column2': [1, 2, 3]
        })

        cleaned = self.extractor.clean_table_data(df)

        # Check that whitespace is stripped
        self.assertEqual(cleaned.iloc[0, 0], 'value1')

    def test_table_to_dict(self):
        """Test converting table to dictionary."""
        table_dict = self.extractor.table_to_dict(self.sample_df)

        self.assertEqual(len(table_dict), 3)
        self.assertEqual(table_dict[0]['Name'], 'Alice')

    def test_extract_numeric_columns(self):
        """Test numeric column extraction."""
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob'],
            'Age': ['25', '30'],
            'Score': ['95.5', '87.3']
        })

        numeric_df = self.extractor.extract_numeric_columns(df)

        # Age and Score should be numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(numeric_df['Age']))


class TestDocumentAnalyzer(unittest.TestCase):
    """Test DocumentAnalyzer functionality."""

    def setUp(self):
        """Set up test fixtures."""
        from models.document_model import DocumentAnalyzer
        self.analyzer = DocumentAnalyzer()

    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        self.assertIsNotNone(self.analyzer.pdf_reader)
        self.assertIsNotNone(self.analyzer.image_reader)
        self.assertIsNotNone(self.analyzer.summarizer)
        self.assertIsNotNone(self.analyzer.qa_engine)

    def test_text_loading(self):
        """Test loading text document."""
        # Create temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document for analysis.")
            temp_file = f.name

        try:
            success, text = self.analyzer.load_document(temp_file)
            self.assertTrue(success)
            self.assertIn("test document", text)
        finally:
            os.unlink(temp_file)

    def test_text_analysis(self):
        """Test text analysis."""
        # Manually set extracted text
        self.analyzer.extracted_text = "This is a test document. It contains important information. Testing is crucial."

        results = self.analyzer.analyze_text()

        self.assertIn('summary', results)
        self.assertIn('keywords', results)
        self.assertIn('statistics', results)

    def test_reset(self):
        """Test analyzer reset."""
        self.analyzer.extracted_text = "Some text"
        self.analyzer.reset()

        self.assertEqual(self.analyzer.extracted_text, "")
        self.assertEqual(self.analyzer.tables, [])


class TestDatabase(unittest.TestCase):
    """Test database operations."""

    def setUp(self):
        """Set up test fixtures."""
        from database.db import DatabaseManager
        # Use in-memory database for testing
        self.db = DatabaseManager(":memory:")

    def test_user_registration(self):
        """Test user registration."""
        success = self.db.register_user("testuser", "test@example.com", "password123")
        self.assertTrue(success)

    def test_user_authentication(self):
        """Test user authentication."""
        self.db.register_user("testuser2", "test2@example.com", "password456")
        user_id = self.db.authenticate_user("testuser2", "password456")

        self.assertIsNotNone(user_id)

    def test_user_authentication_failure(self):
        """Test failed authentication."""
        self.db.register_user("testuser3", "test3@example.com", "password789")
        user_id = self.db.authenticate_user("testuser3", "wrongpassword")

        self.assertIsNone(user_id)


if __name__ == '__main__':
    unittest.main()
