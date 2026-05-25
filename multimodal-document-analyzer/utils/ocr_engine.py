"""
OCR (Optical Character Recognition) engine module.
Handles text extraction from images and scanned documents.
"""

import os
from typing import Dict, List, Tuple, Optional
import easyocr
import pytesseract
from PIL import Image
import cv2
import numpy as np


class OCREngine:
    """
    Provides OCR capabilities for extracting text from images and scanned documents.
    Supports multiple OCR backends: EasyOCR and Tesseract.
    """

    def __init__(self, use_easyocr: bool = True, languages: List[str] = None):
        """
        Initialize OCR engine.

        Args:
            use_easyocr (bool): Whether to use EasyOCR (True) or Tesseract (False).
            languages (List[str]): List of languages to support (e.g., ['en', 'es']).
        """
        self.use_easyocr = use_easyocr
        self.languages = languages or ['en']
        self.reader = None

        if self.use_easyocr:
            try:
                self.reader = easyocr.Reader(self.languages, gpu=False)
            except Exception as e:
                print(f"Warning: Could not initialize EasyOCR: {e}. Will fallback to Tesseract.")
                self.use_easyocr = False

    def extract_text_easyocr(self, image_path: str) -> Dict:
        """
        Extract text from image using EasyOCR.

        Args:
            image_path (str): Path to image file.

        Returns:
            Dict: Extracted text and confidence scores.
        """
        try:
            results = self.reader.readtext(image_path)

            full_text = ""
            text_blocks = []
            total_confidence = 0
            confidence_count = 0

            for detection in results:
                text = detection[1]
                confidence = detection[2]
                bbox = detection[0]

                full_text += text + " "
                text_blocks.append({
                    'text': text,
                    'confidence': float(confidence),
                    'bbox': bbox
                })
                total_confidence += confidence
                confidence_count += 1

            avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0

            return {
                'full_text': full_text.strip(),
                'text_blocks': text_blocks,
                'average_confidence': float(avg_confidence),
                'method': 'easyocr',
                'language': self.languages[0]
            }

        except Exception as e:
            raise Exception(f"Error extracting text with EasyOCR: {str(e)}")

    def extract_text_tesseract(self, image_path: str) -> Dict:
        """
        Extract text from image using Tesseract OCR.

        Args:
            image_path (str): Path to image file.

        Returns:
            Dict: Extracted text and confidence scores.
        """
        try:
            image = Image.open(image_path)

            # Use pytesseract to get detailed results
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            full_text = ""
            text_blocks = []

            for i in range(len(data['text'])):
                text = data['text'][i]
                confidence = int(data['conf'][i])

                if text.strip():
                    full_text += text + " "
                    text_blocks.append({
                        'text': text,
                        'confidence': confidence,
                        'left': int(data['left'][i]),
                        'top': int(data['top'][i]),
                        'width': int(data['width'][i]),
                        'height': int(data['height'][i])
                    })

            # Get average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            return {
                'full_text': full_text.strip(),
                'text_blocks': text_blocks,
                'average_confidence': float(avg_confidence),
                'method': 'tesseract'
            }

        except Exception as e:
            raise Exception(f"Error extracting text with Tesseract: {str(e)}")

    def extract_text(self, image_path: str) -> Dict:
        """
        Extract text from image using available OCR engine.

        Args:
            image_path (str): Path to image file.

        Returns:
            Dict: Extracted text and confidence scores.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        if self.use_easyocr:
            return self.extract_text_easyocr(image_path)
        else:
            return self.extract_text_tesseract(image_path)

    def extract_text_from_multiple_images(self, image_paths: List[str]) -> Dict:
        """
        Extract text from multiple images.

        Args:
            image_paths (List[str]): List of image file paths.

        Returns:
            Dict: Combined extraction results.
        """
        all_text = ""
        all_blocks = []
        total_confidence = 0
        image_count = 0

        for i, image_path in enumerate(image_paths):
            result = self.extract_text(image_path)
            all_text += f"\n--- Image {i + 1} ---\n{result['full_text']}"
            all_blocks.extend(result['text_blocks'])
            total_confidence += result['average_confidence']
            image_count += 1

        avg_confidence = total_confidence / image_count if image_count > 0 else 0

        return {
            'full_text': all_text.strip(),
            'text_blocks': all_blocks,
            'average_confidence': float(avg_confidence),
            'images_processed': len(image_paths),
            'method': self.reader.__class__.__name__ if self.use_easyocr else 'tesseract'
        }

    def extract_handwriting(self, image_path: str) -> Dict:
        """
        Extract handwritten text from image (uses EasyOCR which handles handwriting better).

        Args:
            image_path (str): Path to image file.

        Returns:
            Dict: Extracted handwritten text.
        """
        if not self.use_easyocr:
            raise Exception("Handwriting extraction requires EasyOCR")

        return self.extract_text_easyocr(image_path)

    def extract_text_from_scanned_pdf_image(self, image_path: str) -> Dict:
        """
        Extract text from a scanned PDF page (as image).

        Args:
            image_path (str): Path to scanned PDF page image.

        Returns:
            Dict: Extracted text with preprocessing info.
        """
        # Preprocess image for better OCR
        image = cv2.imread(image_path)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Denoise
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Save preprocessed image temporarily
        temp_path = image_path.replace('.', '_preprocessed.')
        cv2.imwrite(temp_path, denoised)

        try:
            result = self.extract_text(temp_path)
            result['preprocessing'] = 'CLAHE enhancement + denoising'
            return result
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def detect_language(self, image_path: str) -> Dict:
        """
        Detect language in image.

        Args:
            image_path (str): Path to image file.

        Returns:
            Dict: Detected language information.
        """
        if not self.use_easyocr:
            raise Exception("Language detection requires EasyOCR")

        try:
            results = self.reader.readtext(image_path)
            detected_languages = set()

            for detection in results:
                detected_languages.add(detection[3])  # Language code

            return {
                'detected_languages': list(detected_languages),
                'primary_language': detected_languages.pop() if detected_languages else 'unknown'
            }

        except Exception as e:
            raise Exception(f"Error detecting language: {str(e)}")

    def extract_text_with_layout(self, image_path: str) -> Dict:
        """
        Extract text while preserving layout information.

        Args:
            image_path (str): Path to image file.

        Returns:
            Dict: Text with layout and positioning information.
        """
        result = self.extract_text(image_path)

        if self.use_easyocr:
            # Organize text blocks by y-position (top to bottom)
            sorted_blocks = sorted(result['text_blocks'], key=lambda x: x['bbox'][0][1])
            lines = []
            current_line = []

            for block in sorted_blocks:
                if not current_line or abs(block['bbox'][0][1] - current_line[0]['bbox'][0][1]) < 20:
                    current_line.append(block)
                else:
                    lines.append(' '.join([b['text'] for b in current_line]))
                    current_line = [block]

            if current_line:
                lines.append(' '.join([b['text'] for b in current_line]))

            result['structured_text'] = '\n'.join(lines)

        return result

    def get_confidence_map(self, image_path: str) -> Dict:
        """
        Get confidence scores for different regions of text.

        Args:
            image_path (str): Path to image file.

        Returns:
            Dict: Confidence information by region.
        """
        result = self.extract_text(image_path)

        confidence_stats = {
            'high_confidence': [],  # > 0.9
            'medium_confidence': [],  # 0.7 - 0.9
            'low_confidence': []  # < 0.7
        }

        for block in result['text_blocks']:
            confidence = block['confidence']
            if confidence > 0.9:
                confidence_stats['high_confidence'].append(block)
            elif confidence > 0.7:
                confidence_stats['medium_confidence'].append(block)
            else:
                confidence_stats['low_confidence'].append(block)

        return {
            'overall_average_confidence': result['average_confidence'],
            'confidence_distribution': confidence_stats,
            'high_confidence_text': ' '.join([b['text'] for b in confidence_stats['high_confidence']])
        }
