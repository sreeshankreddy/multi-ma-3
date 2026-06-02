"""
Document question answering system.
Handles context-aware Q&A using transformer models.
"""

from typing import List, Dict, Any, Tuple
import re
from nltk.tokenize import sent_tokenize
import nltk

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass


class DocumentQAEngine:
    """
    Provides context-aware question answering for documents.
    Uses simple keyword matching and context retrieval when models unavailable.
    """

    def __init__(self):
        """Initialize QA engine with graceful fallback."""
        self.qa_pipeline = None
        self.retrieval_pipeline = None
        print("Info: Using fallback Q&A engine (keyword-based extraction)")


    def answer_question(self, question: str, context: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """
        Answer a question based on provided context using keyword matching.

        Args:
            question (str): User question.
            context (str): Document context to search for answers.
            top_k (int): Number of top answers to return.

        Returns:
            List[Dict]: List of answers with scores.
        """
        try:
            # Use keyword-based approach
            passages = self.find_relevant_passages(question, context, num_passages=3)
            
            if passages:
                return [{
                    'answer': passages[0],
                    'score': 0.8,
                    'start': context.find(passages[0]),
                    'end': context.find(passages[0]) + len(passages[0])
                }]
            else:
                return [{'answer': 'Answer not found in context', 'score': 0.0}]

        except Exception as e:
            return [{'answer': f'Error answering question: {str(e)}', 'score': 0.0}]

    def find_relevant_passages(self, question: str, context: str, num_passages: int = 3) -> List[str]:
        """
        Find relevant passages in context for the question using keyword matching.

        Args:
            question (str): User question.
            context (str): Document context.
            num_passages (int): Number of relevant passages to return.

        Returns:
            List[str]: Most relevant passages.
        """
        # Use keyword-based retrieval directly
        return self._keyword_based_retrieval(question, context, num_passages)

    def _keyword_based_retrieval(self, question: str, context: str, num_passages: int) -> List[str]:
        """
        Simple keyword-based retrieval (fallback method).

        Args:
            question (str): User question.
            context (str): Document context.
            num_passages (int): Number of passages to return.

        Returns:
            List[str]: Relevant passages.
        """
        from nltk.tokenize import sent_tokenize
        import nltk

        try:
            sentences = sent_tokenize(context)
        except:
            sentences = context.split('. ')

        # Extract keywords from question
        keywords = question.lower().split()
        keywords = [w for w in keywords if len(w) > 3]

        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            score = sum(1 for keyword in keywords if keyword in sentence.lower())
            if score > 0:
                sentence_scores.append((sentence, score))

        # Sort by score
        sentence_scores = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
        return [sentence for sentence, _ in sentence_scores[:num_passages]]

    def generate_qa_pairs(self, context: str, num_pairs: int = 5) -> List[Dict[str, str]]:
        """
        Generate question-answer pairs from context (useful for training/testing).

        Args:
            context (str): Document context.
            num_pairs (int): Number of QA pairs to generate.

        Returns:
            List[Dict]: List of QA pairs.
        """
        from nltk.tokenize import sent_tokenize
        import random

        try:
            sentences = sent_tokenize(context)
        except:
            sentences = context.split('. ')

        qa_pairs = []

        for i, sentence in enumerate(sentences[:num_pairs]):
            # Simple QA pair generation
            words = sentence.split()

            if len(words) > 5:
                # Create question from sentence structure
                if words[0].lower() in ['the', 'a', 'an']:
                    # Format: "The X is Y" -> "What is X?"
                    subject = ' '.join(words[1:3])
                    question = f"What is {subject}?"
                else:
                    # Format: "X is Y" -> "What is X?"
                    subject = words[0]
                    question = f"What about {subject}?"

                qa_pairs.append({
                    'question': question,
                    'answer': sentence,
                    'context': context
                })

        return qa_pairs

    def batch_answer_questions(self, questions: List[str], context: str) -> List[Dict[str, Any]]:
        """
        Answer multiple questions about the same context.

        Args:
            questions (List[str]): List of questions.
            context (str): Document context.

        Returns:
            List[Dict]: Answers for each question.
        """
        results = []

        for question in questions:
            try:
                answer = self.answer_question(question, context)
                results.append({
                    'question': question,
                    'answer': answer[0] if answer else None
                })
            except Exception as e:
                results.append({
                    'question': question,
                    'answer': None,
                    'error': str(e)
                })

        return results

    def contextualized_answer(self, question: str, document_text: str, chat_history: List[str] = None) -> Dict[str, Any]:
        """
        Generate contextually aware answer considering chat history.

        Args:
            question (str): Current question.
            document_text (str): Full document text.
            chat_history (List[str]): Previous questions in conversation.

        Returns:
            Dict: Answer with context information.
        """
        # Find relevant passages
        relevant_passages = self.find_relevant_passages(question, document_text, num_passages=3)
        context = ' '.join(relevant_passages)

        # Generate answer
        answer_result = self.answer_question(question, context)

        return {
            'question': question,
            'answer': answer_result[0]['answer'] if answer_result else 'No answer found',
            'confidence': answer_result[0]['score'] if answer_result else 0.0,
            'relevant_context': context,
            'passages_used': len(relevant_passages)
        }

    def extract_key_information(self, document_text: str) -> Dict[str, Any]:
        """
        Extract key information by asking predefined questions.

        Args:
            document_text (str): Document text.

        Returns:
            Dict: Extracted key information.
        """
        predefined_questions = [
            "What is this document about?",
            "What are the main topics?",
            "What are the key findings?",
            "What are the conclusions?",
            "What are the recommendations?"
        ]

        key_info = {}

        for question in predefined_questions:
            try:
                answer = self.answer_question(question, document_text)
                key_info[question] = answer[0]['answer'] if answer else 'Not found'
            except Exception as e:
                key_info[question] = f'Error: {str(e)}'

        return key_info
