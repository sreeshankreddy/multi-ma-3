"""
PDF reading and processing module.
Handles PDF text extraction, page processing, and error handling.
"""

import os
from typing import List, Dict, Tuple, Optional
import PyPDF2
import fitz  # PyMuPDF


class PDFReader:
    """
    Handles reading and processing PDF files.
    Supports both text-based and scanned PDFs through multiple backends.
    """

    @staticmethod
    def extract_text_pymupdf(pdf_path: str) -> Tuple[str, List[Dict]]:
        """
        Extract text from PDF using PyMuPDF (faster and better for modern PDFs).

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            Tuple[str, List[Dict]]: Extracted text and page information.
        """
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            page_info = []

            for page_num, page in enumerate(doc):
                text = page.get_text()
                full_text += f"\n--- Page {page_num + 1} ---\n{text}"

                page_info.append({
                    'page_number': page_num + 1,
                    'text': text,
                    'word_count': len(text.split()),
                    'char_count': len(text)
                })

            doc.close()
            return full_text, page_info

        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    @staticmethod
    def extract_text_pypdf(pdf_path: str) -> Tuple[str, List[Dict]]:
        """
        Extract text from PDF using PyPDF2.

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            Tuple[str, List[Dict]]: Extracted text and page information.
        """
        try:
            full_text = ""
            page_info = []

            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)

                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    full_text += f"\n--- Page {page_num + 1} ---\n{text}"

                    page_info.append({
                        'page_number': page_num + 1,
                        'text': text,
                        'word_count': len(text.split()),
                        'char_count': len(text)
                    })

            return full_text, page_info

        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    @staticmethod
    def extract_text(pdf_path: str) -> Tuple[str, List[Dict]]:
        """
        Extract text from PDF (uses PyMuPDF first, falls back to PyPDF2).

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            Tuple[str, List[Dict]]: Extracted text and page information.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            # Try PyMuPDF first (better for most PDFs)
            return PDFReader.extract_text_pymupdf(pdf_path)
        except Exception as e:
            # Fallback to PyPDF2
            try:
                return PDFReader.extract_text_pypdf(pdf_path)
            except Exception as e2:
                raise Exception(f"Failed to extract text from PDF with both methods: {str(e)}, {str(e2)}")

    @staticmethod
    def get_page_count(pdf_path: str) -> int:
        """
        Get the total number of pages in a PDF.

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            int: Number of pages.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            doc.close()
            return page_count
        except Exception:
            # Fallback to PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return len(reader.pages)

    @staticmethod
    def extract_page(pdf_path: str, page_num: int) -> Dict:
        """
        Extract text and information from a specific page.

        Args:
            pdf_path (str): Path to PDF file.
            page_num (int): Page number (1-indexed).

        Returns:
            Dict: Page information and text.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)
            if page_num < 1 or page_num > len(doc):
                raise ValueError(f"Invalid page number: {page_num}")

            page = doc[page_num - 1]
            text = page.get_text()
            doc.close()

            return {
                'page_number': page_num,
                'text': text,
                'word_count': len(text.split()),
                'char_count': len(text)
            }

        except Exception as e:
            raise Exception(f"Error extracting page {page_num}: {str(e)}")

    @staticmethod
    def extract_metadata(pdf_path: str) -> Dict:
        """
        Extract metadata from PDF (title, author, creation date, etc.).

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            Dict: PDF metadata.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            doc.close()

            return {
                'title': metadata.get('title', 'Unknown'),
                'author': metadata.get('author', 'Unknown'),
                'subject': metadata.get('subject', 'Unknown'),
                'creator': metadata.get('creator', 'Unknown'),
                'producer': metadata.get('producer', 'Unknown'),
                'creation_date': metadata.get('creationDate', 'Unknown'),
                'modification_date': metadata.get('modDate', 'Unknown'),
            }

        except Exception as e:
            raise Exception(f"Error extracting metadata: {str(e)}")

    @staticmethod
    def extract_images(pdf_path: str, output_dir: str) -> List[str]:
        """
        Extract images from PDF and save to disk.

        Args:
            pdf_path (str): Path to PDF file.
            output_dir (str): Directory to save extracted images.

        Returns:
            List[str]: List of saved image file paths.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        os.makedirs(output_dir, exist_ok=True)
        saved_images = []

        try:
            doc = fitz.open(pdf_path)

            for page_num, page in enumerate(doc):
                image_list = page.get_images()

                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)

                    # Save as PNG
                    filename = f"page_{page_num + 1}_image_{img_index + 1}.png"
                    filepath = os.path.join(output_dir, filename)
                    pix.save(filepath)
                    saved_images.append(filepath)

            doc.close()
            return saved_images

        except Exception as e:
            raise Exception(f"Error extracting images: {str(e)}")

    @staticmethod
    def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> List[str]:
        """
        Convert entire PDF to images (useful for OCR on scanned PDFs).

        Args:
            pdf_path (str): Path to PDF file.
            output_dir (str): Directory to save page images.
            dpi (int): DPI for image conversion.

        Returns:
            List[str]: List of saved image file paths.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        os.makedirs(output_dir, exist_ok=True)
        saved_images = []

        try:
            doc = fitz.open(pdf_path)

            for page_num, page in enumerate(doc):
                # Render page to image at specified DPI
                zoom = dpi / 72  # Default DPI is 72
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                filename = f"page_{page_num + 1}.png"
                filepath = os.path.join(output_dir, filename)
                pix.save(filepath)
                saved_images.append(filepath)

            doc.close()
            return saved_images

        except Exception as e:
            raise Exception(f"Error converting PDF to images: {str(e)}")

    @staticmethod
    def get_pdf_info(pdf_path: str) -> Dict:
        """
        Get comprehensive information about a PDF.

        Args:
            pdf_path (str): Path to PDF file.

        Returns:
            Dict: PDF information including page count, metadata, size, etc.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)
            file_size = os.path.getsize(pdf_path)

            info = {
                'page_count': len(doc),
                'metadata': doc.metadata,
                'file_size': file_size,
                'file_size_mb': file_size / (1024 * 1024),
                'is_pdf': True
            }

            doc.close()
            return info

        except Exception as e:
            raise Exception(f"Error getting PDF info: {str(e)}")
