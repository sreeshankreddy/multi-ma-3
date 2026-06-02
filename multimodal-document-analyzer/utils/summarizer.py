"""
AI-powered document summarization and analysis module.
Handles text summarization, keyword extraction, and NLP analysis.
"""

from typing import List, Dict, Any, Tuple
from collections import Counter
import re
import math
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy as np


# Download required NLTK data
for resource_name, download_name in [
    ('tokenizers/punkt', 'punkt'),
    ('tokenizers/punkt_tab', 'punkt_tab'),
    ('corpora/stopwords', 'stopwords')
]:
    try:
        nltk.data.find(resource_name)
    except LookupError:
        try:
            nltk.download(download_name, quiet=True)
        except:
            pass


class DocumentSummarizer:
    """
    Provides document summarization and analysis using transformers and NLP.
    Generates summaries, extracts keywords, performs sentiment analysis, etc.
    """

    def __init__(self):
        """Initialize NLP models and pipelines with proper error handling."""
        self.summarizer = None
        self.sentiment_analyzer = None
        self.ner_pipeline = None

    def _load_sentiment_analyzer(self):
        if self.sentiment_analyzer is None:
            try:
                self.sentiment_analyzer = pipeline("sentiment-analysis")
            except Exception as e:
                print(f"Info: Sentiment model initialization deferred: {type(e).__name__}")
                self.sentiment_analyzer = None
        return self.sentiment_analyzer

    def _load_ner_pipeline(self):
        if self.ner_pipeline is None:
            try:
                self.ner_pipeline = pipeline("ner", model="dbmdz/bert-base-cased-ner")
            except Exception as e:
                print(f"Info: NER model not available, using fallback extraction: {type(e).__name__}")
                self.ner_pipeline = None
        return self.ner_pipeline

    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """
        Summarize text using extractive summarization.

        Args:
            text (str): Input text to summarize.
            max_length (int): Maximum length of summary.
            min_length (int): Minimum length of summary.

        Returns:
            str: Summarized text.
        """
        try:
            # Use extractive summarization as primary method
            return self.extractive_summary(text, num_sentences=3)
        except Exception as e:
            print(f"Error in summarization: {e}")
            # Fallback: return first few sentences
            sentences = sent_tokenize(text)
            return ' '.join(sentences[:min(3, len(sentences))])

    def extractive_summary(self, text: str, num_sentences: int = 3) -> str:
        """
        Generate extractive summary by scoring and selecting top sentences.

        Args:
            text (str): Input text.
            num_sentences (int): Number of sentences to extract.

        Returns:
            str: Extractive summary.
        """
        sentences = sent_tokenize(text)

        if len(sentences) <= num_sentences:
            return text

        # Calculate TF scores for words
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if w.isalnum() and w not in stop_words]

        word_freq = Counter(words)
        max_freq = max(word_freq.values()) if word_freq else 1

        # Score sentences based on word frequency
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            score = 0
            for word in words:
                if word in word_freq:
                    score += word_freq[word] / max_freq

            sentence_scores[i] = score

        # Select top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Sort by original order

        summary = ' '.join([sentences[i] for i, _ in top_sentences])
        return summary

    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        Extract keywords from text using TF-IDF scoring.

        Args:
            text (str): Input text.
            num_keywords (int): Number of keywords to extract.

        Returns:
            List[str]: List of keywords.
        """
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))

        # Filter words
        words = [w for w in words if w.isalnum() and w not in stop_words and len(w) > 3]

        # Calculate TF scores
        word_freq = Counter(words)

        # Get top keywords
        keywords = [word for word, _ in word_freq.most_common(num_keywords)]
        return keywords

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text (persons, locations, organizations, etc.).

        Args:
            text (str): Input text.

        Returns:
            Dict: Dictionary mapping entity types to lists of entities.
        """
        ner_pipeline = self._load_ner_pipeline()
        if not ner_pipeline:
            return self._extract_entities_regex(text)

        try:
            # Split text into chunks for NER
            sentences = sent_tokenize(text)
            entities_dict = {
                'PERSON': [],
                'LOCATION': [],
                'ORGANIZATION': [],
                'MISC': [],
                'OTHER': []
            }

            for sentence in sentences:
                if len(sentence.split()) > 512:  # Skip very long sentences
                    continue

                results = ner_pipeline(sentence)

                for result in results:
                    entity_type = result['entity_group']
                    word = result['word']

                    if entity_type in entities_dict:
                        if word not in entities_dict[entity_type]:
                            entities_dict[entity_type].append(word)

            return entities_dict

        except Exception as e:
            print(f"Error in NER: {e}")
            return self._extract_entities_regex(text)

    def _extract_entities_regex(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using regex patterns (fallback method).

        Args:
            text (str): Input text.

        Returns:
            Dict: Dictionary mapping entity types to lists of entities.
        """
        entities = {
            'PERSON': [],
            'LOCATION': [],
            'ORGANIZATION': [],
            'MISC': [],
            'OTHER': []
        }

        # Extract emails
        emails = re.findall(r'\S+@\S+', text)
        entities['OTHER'].extend(emails)

        # Extract phone numbers
        phones = re.findall(r'\+?1?\d{9,15}', text)
        entities['OTHER'].extend(phones)

        return entities

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text.

        Args:
            text (str): Input text.

        Returns:
            Dict: Sentiment analysis results.
        """
        sentiment_analyzer = self._load_sentiment_analyzer()
        if not sentiment_analyzer:
            return {'overall_sentiment': 'UNKNOWN', 'confidence': 0.0}

        try:
            # Split into chunks for analysis
            sentences = sent_tokenize(text)
            sentiments = []

            for sentence in sentences:
                if len(sentence.strip()) < 5:
                    continue

                result = sentiment_analyzer(sentence)
                sentiments.append(result[0])

            # Calculate overall sentiment
            if sentiments:
                positive_count = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
                overall_label = 'POSITIVE' if positive_count > len(sentiments) / 2 else 'NEGATIVE'
                avg_score = sum(s['score'] for s in sentiments) / len(sentiments)

                return {
                    'overall_sentiment': overall_label,
                    'confidence': float(avg_score),
                    'positive_sentences': positive_count,
                    'negative_sentences': len(sentiments) - positive_count,
                    'total_sentences': len(sentiments)
                }
            else:
                return {'overall_sentiment': 'NEUTRAL', 'confidence': 0.5}

        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {'overall_sentiment': 'UNKNOWN', 'confidence': 0.0}

    def extract_topics(self, text: str, num_topics: int = 5) -> List[str]:
        """
        Extract main topics from text.

        Args:
            text (str): Input text.
            num_topics (int): Number of topics to extract.

        Returns:
            List[str]: List of topics.
        """
        # Use keywords as topics
        keywords = self.extract_keywords(text, num_keywords=num_topics * 2)

        # Group related keywords
        topics = keywords[:num_topics]
        return topics

    def generate_bullet_points(self, text: str, num_points: int = 5) -> List[str]:
        """
        Generate bullet point summary.

        Args:
            text (str): Input text.
            num_points (int): Number of bullet points.

        Returns:
            List[str]: List of bullet point summaries.
        """
        sentences = sent_tokenize(text)

        if len(sentences) <= num_points:
            return sentences

        # Score sentences
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if w.isalnum() and w not in stop_words]

        word_freq = Counter(words)
        max_freq = max(word_freq.values()) if word_freq else 1

        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            words = word_tokenize(sentence.lower())
            score = 0
            for word in words:
                if word in word_freq:
                    score += word_freq[word] / max_freq

            sentence_scores[i] = score

        # Select top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_points]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])

        bullet_points = [sentences[i] for i, _ in top_sentences]
        return bullet_points

    def extract_important_phrases(self, text: str, num_phrases: int = 10) -> List[str]:
        """
        Extract important phrases from text.

        Args:
            text (str): Input text.
            num_phrases (int): Number of phrases to extract.

        Returns:
            List[str]: List of important phrases.
        """
        # Extract bigrams and trigrams
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if w.isalnum() and w not in stop_words]

        # Extract bigrams
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
        bigram_freq = Counter(bigrams)

        # Get top phrases
        top_phrases = [phrase for phrase, _ in bigram_freq.most_common(num_phrases)]
        return top_phrases

    def get_document_statistics(self, text: str) -> Dict[str, Any]:
        """
        Get statistics about the document.

        Args:
            text (str): Input text.

        Returns:
            Dict: Document statistics.
        """
        sentences = sent_tokenize(text)
        words = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        meaningful_words = [w for w in words if w.isalnum() and w not in stop_words]

        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        return {
            'total_characters': len(text),
            'total_words': len(words),
            'total_sentences': len(sentences),
            'unique_words': len(set(words)),
            'meaningful_words': len(meaningful_words),
            'average_word_length': float(avg_word_length),
            'average_sentence_length': float(avg_sentence_length),
            'reading_time_minutes': round(len(words) / 200)  # Average reading speed
        }
