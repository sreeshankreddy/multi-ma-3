"""
Document question answering system.
Handles context-aware Q&A using transformer models.
"""

from typing import List, Dict, Any, Tuple
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
import torch


class DocumentQAEngine:
    """
    Provides context-aware question answering for documents.
    Uses transformer models to find relevant context and generate answers.
    """

    def __init__(self):
        """Initialize QA pipeline and models."""
        try:
            # Initialize question answering pipeline
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Warning: Could not load QA model: {e}")
            try:
                # Fallback to simpler model
                self.qa_pipeline = pipeline(
                    "question-answering",
                    model="distilbert-base-cased-distilled-squad",
                    device=-1
                )
            except Exception as e2:
                print(f"Error loading fallback QA model: {e2}")
                self.qa_pipeline = None

        try:
            # Initialize retrieval model for finding relevant passages
            self.retrieval_pipeline = pipeline(
                "feature-extraction",
                model="sentence-transformers/all-MiniLM-L6-v2",
                device=-1
            )
        except Exception as e:
            print(f"Warning: Could not load retrieval model: {e}")
            self.retrieval_pipeline = None

    def answer_question(self, question: str, context: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """
        Answer a question based on provided context.

        Args:
            question (str): User question.
            context (str): Document context to search for answers.
            top_k (int): Number of top answers to return.

        Returns:
            List[Dict]: List of answers with scores.
        """
        if not self.qa_pipeline:
            return [{'answer': 'QA model not available', 'score': 0.0}]

        try:
            # Split context into chunks if too long (512 tokens max for most models)
            chunks = self._split_into_chunks(context, chunk_size=384)

            all_answers = []

            for chunk in chunks:
                try:
                    result = self.qa_pipeline(
                        question=question,
                        context=chunk,
                        top_k=top_k
                    )

                    if isinstance(result, list):
                        all_answers.extend(result)
                    else:
                        all_answers.append(result)

                except Exception as e:
                    continue

            # Remove duplicates and sort by score
            if all_answers:
                # Sort by score
                all_answers = sorted(all_answers, key=lambda x: x.get('score', 0), reverse=True)
                return all_answers[:top_k]
            else:
                return [{'answer': 'No answer found', 'score': 0.0}]

        except Exception as e:
            raise Exception(f"Error answering question: {str(e)}")

    def find_relevant_passages(self, question: str, context: str, num_passages: int = 3) -> List[str]:
        """
        Find relevant passages in context for the question.

        Args:
            question (str): User question.
            context (str): Document context.
            num_passages (int): Number of relevant passages to return.

        Returns:
            List[str]: Most relevant passages.
        """
        if not self.retrieval_pipeline:
            # Fallback to simple keyword matching
            return self._keyword_based_retrieval(question, context, num_passages)

        try:
            # Split context into sentences/passages
            passages = context.split('. ')

            # Get embeddings for question
            question_embedding = self._get_embedding(question)

            # Score passages by relevance
            passage_scores = []
            for passage in passages:
                if len(passage.strip()) < 10:
                    continue

                passage_embedding = self._get_embedding(passage)
                similarity = self._cosine_similarity(question_embedding, passage_embedding)
                passage_scores.append((passage, similarity))

            # Return top passages
            passage_scores = sorted(passage_scores, key=lambda x: x[1], reverse=True)
            return [passage for passage, _ in passage_scores[:num_passages]]

        except Exception as e:
            print(f"Error finding relevant passages: {e}")
            return self._keyword_based_retrieval(question, context, num_passages)

    def _get_embedding(self, text: str) -> Any:
        """
        Get embedding for text.

        Args:
            text (str): Input text.

        Returns:
            Any: Text embedding.
        """
        if not self.retrieval_pipeline:
            return None

        try:
            embedding = self.retrieval_pipeline(text)
            return embedding[0]
        except Exception:
            return None

    def _cosine_similarity(self, vec1: Any, vec2: Any) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector.
            vec2: Second vector.

        Returns:
            float: Cosine similarity score.
        """
        if vec1 is None or vec2 is None:
            return 0.0

        import numpy as np
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _split_into_chunks(self, text: str, chunk_size: int = 384) -> List[str]:
        """
        Split text into overlapping chunks for QA.

        Args:
            text (str): Input text.
            chunk_size (int): Target chunk size in tokens.

        Returns:
            List[str]: Text chunks.
        """
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence.split())

            if current_length + sentence_length > chunk_size and current_chunk:
                chunks.append('. '.join(current_chunk))
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append('. '.join(current_chunk))

        return chunks

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
