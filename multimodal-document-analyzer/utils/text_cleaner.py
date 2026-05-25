"""
Text cleaning and preprocessing utilities for document analysis.
Handles text normalization, formatting, and quality improvement.
"""

import re
import unicodedata
from typing import List, Tuple


class TextCleaner:
    """
    Provides text cleaning and preprocessing operations.
    Handles removal of extra whitespace, special characters, and text normalization.
    """

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize Unicode text and handle special characters.

        Args:
            text (str): Input text.

        Returns:
            str: Normalized text.
        """
        # Normalize Unicode characters
        text = unicodedata.normalize('NFKD', text)
        # Remove control characters
        text = ''.join(char for char in text if unicodedata.category(char) != 'Cc')
        return text

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing extra whitespace and special characters.

        Args:
            text (str): Input text.

        Returns:
            str: Cleaned text.
        """
        # Normalize text first
        text = TextCleaner.normalize_text(text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text

    @staticmethod
    def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
        """
        Remove special characters from text.

        Args:
            text (str): Input text.
            keep_punctuation (bool): Whether to keep punctuation marks.

        Returns:
            str: Text with special characters removed.
        """
        if keep_punctuation:
            # Keep letters, digits, punctuation, and spaces
            text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\'\"-]', '', text)
        else:
            # Keep only letters, digits, and spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text

    @staticmethod
    def remove_urls(text: str) -> str:
        """
        Remove URLs from text.

        Args:
            text (str): Input text.

        Returns:
            str: Text with URLs removed.
        """
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        return text

    @staticmethod
    def remove_emails(text: str) -> str:
        """
        Remove email addresses from text.

        Args:
            text (str): Input text.

        Returns:
            str: Text with emails removed.
        """
        text = re.sub(r'\S+@\S+', '', text)
        return text

    @staticmethod
    def split_into_sentences(text: str) -> List[str]:
        """
        Split text into sentences.

        Args:
            text (str): Input text.

        Returns:
            List[str]: List of sentences.
        """
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def split_into_chunks(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks for processing.

        Args:
            text (str): Input text.
            chunk_size (int): Size of each chunk.
            overlap (int): Overlap between chunks.

        Returns:
            List[str]: List of text chunks.
        """
        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)
            start = end - overlap

        return chunks

    @staticmethod
    def extract_numbers(text: str) -> List[str]:
        """
        Extract all numbers from text.

        Args:
            text (str): Input text.

        Returns:
            List[str]: List of numbers found.
        """
        numbers = re.findall(r'\d+\.?\d*', text)
        return numbers

    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """
        Extract dates from text using common patterns.

        Args:
            text (str): Input text.

        Returns:
            List[str]: List of dates found.
        """
        # Common date patterns: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, etc.
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{1,2}-\d{1,2}',
            r'\d{1,2}-\d{1,2}-\d{4}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}',
        ]
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        return dates

    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """
        Extract phone numbers from text.

        Args:
            text (str): Input text.

        Returns:
            List[str]: List of phone numbers found.
        """
        # Phone number patterns
        pattern = r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(pattern, text)
        return ['-'.join(phone) for phone in phones]

    @staticmethod
    def remove_duplicate_lines(text: str) -> str:
        """
        Remove duplicate consecutive lines.

        Args:
            text (str): Input text.

        Returns:
            str: Text with duplicate lines removed.
        """
        lines = text.split('\n')
        unique_lines = []
        prev_line = ""

        for line in lines:
            if line.strip() != prev_line.strip():
                unique_lines.append(line)
                prev_line = line

        return '\n'.join(unique_lines)

    @staticmethod
    def convert_to_lowercase(text: str) -> str:
        """
        Convert text to lowercase.

        Args:
            text (str): Input text.

        Returns:
            str: Lowercase text.
        """
        return text.lower()

    @staticmethod
    def remove_stopwords(text: str, stopwords: List[str] = None) -> str:
        """
        Remove common stopwords from text.

        Args:
            text (str): Input text.
            stopwords (List[str]): List of stopwords to remove.

        Returns:
            str: Text with stopwords removed.
        """
        if stopwords is None:
            stopwords = [
                'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by',
                'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of',
                'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there',
                'these', 'they', 'this', 'to', 'was', 'will', 'with'
            ]

        words = text.lower().split()
        filtered_words = [word for word in words if word not in stopwords]
        return ' '.join(filtered_words)

    @staticmethod
    def expand_contractions(text: str) -> str:
        """
        Expand contractions (e.g., don't -> do not).

        Args:
            text (str): Input text.

        Returns:
            str: Text with contractions expanded.
        """
        contractions_dict = {
            "ain't": "am not",
            "aren't": "are not",
            "can't": "cannot",
            "can't've": "cannot have",
            "could've": "could have",
            "couldn't": "could not",
            "didn't": "did not",
            "doesn't": "does not",
            "don't": "do not",
            "hadn't": "had not",
            "hasn't": "has not",
            "haven't": "have not",
            "he'd": "he would",
            "he'll": "he will",
            "he's": "he is",
            "how'd": "how did",
            "how'll": "how will",
            "how's": "how is",
            "i'd": "i would",
            "i'll": "i will",
            "i'm": "i am",
            "i've": "i have",
            "isn't": "is not",
            "it'd": "it would",
            "it'll": "it will",
            "it's": "it is",
            "let's": "let us",
            "shouldn't": "should not",
            "that's": "that is",
            "there's": "there is",
            "they'd": "they would",
            "they'll": "they will",
            "they're": "they are",
            "they've": "they have",
            "wasn't": "was not",
            "we'd": "we would",
            "we'll": "we will",
            "we're": "we are",
            "we've": "we have",
            "weren't": "were not",
            "what's": "what is",
            "won't": "will not",
            "wouldn't": "would not",
            "you'd": "you would",
            "you'll": "you will",
            "you're": "you are",
            "you've": "you have",
        }

        pattern = re.compile(r'\b(' + '|'.join(contractions_dict.keys()) + r')\b')
        return pattern.sub(lambda x: contractions_dict[x.group(0).lower()], text, flags=re.IGNORECASE)
