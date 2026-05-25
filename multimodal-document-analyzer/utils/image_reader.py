"""
Image reading and processing module.
Handles image loading, preprocessing, and basic analysis.
"""

import os
from typing import Tuple, Optional, Dict, Any
import cv2
import numpy as np
from PIL import Image


class ImageReader:
    """
    Handles reading, loading, and basic processing of image files.
    Supports multiple image formats and provides image preprocessing.
    """

    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    @staticmethod
    def load_image(image_path: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Load image and return both OpenCV and PIL formats with metadata.

        Args:
            image_path (str): Path to image file.

        Returns:
            Tuple[np.ndarray, Dict]: Image array and metadata.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Check file extension
        _, ext = os.path.splitext(image_path)
        if ext.lower() not in ImageReader.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {ext}")

        try:
            # Load with OpenCV (BGR format)
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Failed to load image")

            # Get metadata
            height, width = image.shape[:2]
            file_size = os.path.getsize(image_path)

            # Load with PIL for additional info
            pil_image = Image.open(image_path)

            metadata = {
                'width': width,
                'height': height,
                'file_size': file_size,
                'file_size_kb': file_size / 1024,
                'format': pil_image.format,
                'mode': pil_image.mode,
                'channels': image.shape[2] if len(image.shape) == 3 else 1,
                'dpi': pil_image.info.get('dpi', (72, 72))
            }

            return image, metadata

        except Exception as e:
            raise Exception(f"Error loading image: {str(e)}")

    @staticmethod
    def resize_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
        """
        Resize image to specified dimensions.

        Args:
            image (np.ndarray): Input image.
            width (int): Target width.
            height (int): Target height.

        Returns:
            np.ndarray: Resized image.
        """
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    @staticmethod
    def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
        """
        Convert image to grayscale.

        Args:
            image (np.ndarray): Input image (BGR).

        Returns:
            np.ndarray: Grayscale image.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def enhance_contrast(image: np.ndarray, clip_limit: float = 2.0,
                        tile_size: int = 8) -> np.ndarray:
        """
        Enhance image contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization).

        Args:
            image (np.ndarray): Input image.
            clip_limit (float): Contrast limit.
            tile_size (int): Tile size for CLAHE.

        Returns:
            np.ndarray: Enhanced image.
        """
        if len(image.shape) == 3:
            # Convert to grayscale first
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
        enhanced = clahe.apply(gray)

        if len(image.shape) == 3:
            # Convert back to BGR
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

        return enhanced

    @staticmethod
    def denoise_image(image: np.ndarray, strength: int = 10) -> np.ndarray:
        """
        Denoise image using bilateral filtering.

        Args:
            image (np.ndarray): Input image.
            strength (int): Denoising strength.

        Returns:
            np.ndarray: Denoised image.
        """
        return cv2.bilateralFilter(image, 9, strength, strength)

    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate image by specified angle.

        Args:
            image (np.ndarray): Input image.
            angle (float): Rotation angle in degrees.

        Returns:
            np.ndarray: Rotated image.
        """
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height))
        return rotated

    @staticmethod
    def detect_edges(image: np.ndarray, threshold1: int = 100,
                    threshold2: int = 200) -> np.ndarray:
        """
        Detect edges in image using Canny edge detection.

        Args:
            image (np.ndarray): Input image.
            threshold1 (int): Lower threshold.
            threshold2 (int): Upper threshold.

        Returns:
            np.ndarray: Edge detected image.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        edges = cv2.Canny(gray, threshold1, threshold2)
        return edges

    @staticmethod
    def detect_contours(image: np.ndarray) -> Tuple[np.ndarray, list]:
        """
        Detect contours in image.

        Args:
            image (np.ndarray): Input image.

        Returns:
            Tuple[np.ndarray, list]: Image with drawn contours and contour list.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours
        image_with_contours = image.copy()
        cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

        return image_with_contours, contours

    @staticmethod
    def get_image_statistics(image: np.ndarray) -> Dict[str, Any]:
        """
        Calculate image statistics (brightness, contrast, saturation).

        Args:
            image (np.ndarray): Input image.

        Returns:
            Dict: Image statistics.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        mean = np.mean(gray)
        std = np.std(gray)
        min_val = np.min(gray)
        max_val = np.max(gray)

        return {
            'mean_brightness': float(mean),
            'std_dev': float(std),
            'min_value': float(min_val),
            'max_value': float(max_val),
            'contrast': float(std),
            'dynamic_range': float(max_val - min_val)
        }

    @staticmethod
    def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR performance.

        Args:
            image (np.ndarray): Input image.

        Returns:
            np.ndarray: Preprocessed image.
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Apply bilateral filter for denoising
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Apply threshold for better text detection
        _, binary = cv2.threshold(denoised, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binary

    @staticmethod
    def save_image(image: np.ndarray, output_path: str) -> None:
        """
        Save image to file.

        Args:
            image (np.ndarray): Image to save.
            output_path (str): Path to save image.
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)

    @staticmethod
    def convert_bgr_to_rgb(image: np.ndarray) -> np.ndarray:
        """
        Convert image from BGR to RGB format.

        Args:
            image (np.ndarray): Image in BGR format.

        Returns:
            np.ndarray: Image in RGB format.
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    @staticmethod
    def get_image_quality_score(image: np.ndarray) -> float:
        """
        Calculate image quality score (0-100).

        Args:
            image (np.ndarray): Input image.

        Returns:
            float: Quality score.
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Calculate Laplacian variance (focus/sharpness)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Normalize to 0-100 scale
        # Typical values range from 100-10000, map to 0-100
        quality_score = min(100, (laplacian_var / 100))

        return quality_score
