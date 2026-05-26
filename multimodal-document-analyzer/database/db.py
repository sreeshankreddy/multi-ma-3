"""
Database module for MultiModal Document Analyzer.
Handles user authentication, document storage, and analysis results.
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any


class DatabaseManager:
    """
    Manages SQLite database operations for user and document management.
    Provides methods for user authentication, document storage, and result retrieval.
    """

    def __init__(self, db_path: str = "analyzer.db"):
        """
        Initialize database manager and create tables if they don't exist.

        Args:
            db_path (str): Path to SQLite database file.
        """
        self.db_path = db_path
        self._connection = None

        # Use a persistent connection for in-memory databases
        if self.db_path == ":memory:":
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row

        self.init_database()

    def _get_connection(self):
        if self._connection:
            return self._connection
        return sqlite3.connect(self.db_path)

    def _close_connection(self, conn):
        if conn is not self._connection:
            conn.close()

    def init_database(self) -> None:
        """Initialize database and create required tables."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create analysis results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                summary TEXT,
                keywords TEXT,
                entities TEXT,
                topics TEXT,
                sentiment TEXT,
                extracted_text TEXT,
                tables TEXT,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
            )
        """)

        # Create chat history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                user_question TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        self._close_connection(conn)

    def _hash_password(self, password: str) -> str:
        """
        Hash a password using SHA256.

        Args:
            password (str): Plain text password.

        Returns:
            str: Hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, email: str, password: str) -> bool:
        """
        Register a new user.

        Args:
            username (str): Username.
            email (str): Email address.
            password (str): Plain text password.

        Returns:
            bool: True if registration successful, False otherwise.
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            password_hash = self._hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            """, (username, email, password_hash))
            conn.commit()
            self._close_connection(conn)
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        """
        Authenticate user and return user ID if credentials are valid.

        Args:
            username (str): Username.
            password (str): Plain text password.

        Returns:
            Optional[int]: User ID if authentication successful, None otherwise.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        password_hash = self._hash_password(password)
        cursor.execute("""
            SELECT id FROM users WHERE username = ? AND password_hash = ?
        """, (username, password_hash))
        result = cursor.fetchone()
        self._close_connection(conn)
        return result[0] if result else None

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve user information by ID.

        Args:
            user_id (int): User ID.

        Returns:
            Optional[Dict]: User information or None if not found.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        self._close_connection(conn)
        return dict(result) if result else None

    def save_document(self, user_id: int, filename: str, file_path: str,
                      file_type: str, file_size: int) -> int:
        """
        Save document metadata to database.

        Args:
            user_id (int): User ID.
            filename (str): Original filename.
            file_path (str): Path to uploaded file.
            file_type (str): File type (pdf, jpg, png, docx, txt).
            file_size (int): File size in bytes.

        Returns:
            int: Document ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO documents (user_id, filename, file_path, file_type, file_size)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, filename, file_path, file_type, file_size))
        conn.commit()
        doc_id = cursor.lastrowid
        self._close_connection(conn)
        return doc_id

    def get_user_documents(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve all documents for a specific user.

        Args:
            user_id (int): User ID.
            limit (int): Maximum number of documents to retrieve.

        Returns:
            List[Dict]: List of document information.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM documents WHERE user_id = ?
            ORDER BY upload_date DESC LIMIT ?
        """, (user_id, limit))
        results = cursor.fetchall()
        self._close_connection(conn)
        return [dict(row) for row in results]

    def save_analysis_result(self, document_id: int, summary: str, keywords: List[str],
                            entities: Dict[str, List[str]], topics: List[str],
                            sentiment: str, extracted_text: str, tables: List[Dict]) -> int:
        """
        Save analysis results for a document.

        Args:
            document_id (int): Document ID.
            summary (str): Document summary.
            keywords (List[str]): Extracted keywords.
            entities (Dict): Named entities (persons, locations, organizations).
            topics (List[str]): Detected topics.
            sentiment (str): Overall sentiment.
            extracted_text (str): Full extracted text.
            tables (List[Dict]): Extracted tables.

        Returns:
            int: Analysis result ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_results
            (document_id, summary, keywords, entities, topics, sentiment, extracted_text, tables)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            document_id,
            summary,
            json.dumps(keywords),
            json.dumps(entities),
            json.dumps(topics),
            sentiment,
            extracted_text,
            json.dumps(tables)
        ))
        conn.commit()
        result_id = cursor.lastrowid
        self._close_connection(conn)
        return result_id

    def get_analysis_result(self, document_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve analysis results for a document.

        Args:
            document_id (int): Document ID.

        Returns:
            Optional[Dict]: Analysis results or None if not found.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM analysis_results WHERE document_id = ?
        """, (document_id,))
        result = cursor.fetchone()
        self._close_connection(conn)

        if result:
            result_dict = dict(result)
            # Parse JSON fields
            result_dict['keywords'] = json.loads(result_dict['keywords'])
            result_dict['entities'] = json.loads(result_dict['entities'])
            result_dict['topics'] = json.loads(result_dict['topics'])
            result_dict['tables'] = json.loads(result_dict['tables'])
            return result_dict
        return None

    def save_chat_message(self, document_id: int, question: str, response: str) -> int:
        """
        Save chat message and response.

        Args:
            document_id (int): Document ID.
            question (str): User question.
            response (str): AI response.

        Returns:
            int: Chat history ID.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (document_id, user_question, ai_response)
            VALUES (?, ?, ?)
        """, (document_id, question, response))
        conn.commit()
        chat_id = cursor.lastrowid
        self._close_connection(conn)
        return chat_id

    def get_chat_history(self, document_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve chat history for a document.

        Args:
            document_id (int): Document ID.
            limit (int): Maximum number of messages to retrieve.

        Returns:
            List[Dict]: List of chat messages.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM chat_history WHERE document_id = ?
            ORDER BY timestamp DESC LIMIT ?
        """, (document_id, limit))
        results = cursor.fetchall()
        self._close_connection(conn)
        return [dict(row) for row in results]

    def delete_document(self, document_id: int, user_id: int) -> bool:
        """
        Delete a document and associated analysis results.

        Args:
            document_id (int): Document ID.
            user_id (int): User ID (for verification).

        Returns:
            bool: True if deletion successful.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        # Verify document belongs to user
        cursor.execute("""
            SELECT user_id FROM documents WHERE id = ?
        """, (document_id,))
        result = cursor.fetchone()

        if result and result[0] == user_id:
            cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            conn.commit()
            self._close_connection(conn)
            return True
        self._close_connection(conn)
        return False

    def search_documents(self, user_id: int, search_term: str) -> List[Dict[str, Any]]:
        """
        Search documents by filename.

        Args:
            user_id (int): User ID.
            search_term (str): Search term.

        Returns:
            List[Dict]: List of matching documents.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM documents
            WHERE user_id = ? AND filename LIKE ?
            ORDER BY upload_date DESC
        """, (user_id, f"%{search_term}%"))
        results = cursor.fetchall()
        self._close_connection(conn)
        return [dict(row) for row in results]
