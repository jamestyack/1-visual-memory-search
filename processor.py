"""
Image processing module for screenshot analysis.
Handles OCR extraction and Claude 3 vision API integration.
"""

import base64
import io
import os
from typing import Dict, List, Optional, Tuple
from PIL import Image
import pytesseract
import anthropic
from functools import lru_cache
import hashlib


class ScreenshotProcessor:
    """Process screenshots with OCR and AI vision capabilities."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the processor with optional Anthropic API key.
        
        Args:
            api_key: Anthropic API key for Claude 3 vision
        """
        self.api_key = api_key
        self.client = None
        self.vision_cache = {}
        
        if api_key:
            try:
                self.client = anthropic.Anthropic(api_key=api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Anthropic client: {e}")
                self.client = None
    
    def _image_hash(self, image: Image.Image) -> str:
        """Generate a hash for an image for caching purposes."""
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return hashlib.md5(buffer.getvalue()).hexdigest()
    
    def _resize_image(self, image: Image.Image, max_size: int = 1024) -> Image.Image:
        """
        Resize image if it exceeds max dimensions to optimize API calls.
        
        Args:
            image: PIL Image object
            max_size: Maximum dimension (width or height)
        
        Returns:
            Resized image if needed, original otherwise
        """
        width, height = image.size
        if width > max_size or height > max_size:
            ratio = min(max_size / width, max_size / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return image
    
    def extract_ocr_text(self, image: Image.Image) -> str:
        """
        Extract text from image using OCR.
        
        Args:
            image: PIL Image object
        
        Returns:
            Extracted text string
        """
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return ""
    
    def get_vision_description(self, image: Image.Image, use_cache: bool = True) -> str:
        """
        Get visual description using Claude 3 Haiku.
        
        Args:
            image: PIL Image object
            use_cache: Whether to use cached results
        
        Returns:
            Visual description string
        """
        if not self.client:
            return self._get_fallback_description()
        
        # Check cache
        img_hash = self._image_hash(image)
        if use_cache and img_hash in self.vision_cache:
            return self.vision_cache[img_hash]
        
        try:
            # Resize image for optimization
            optimized_image = self._resize_image(image)
            
            # Convert to base64
            buffer = io.BytesIO()
            optimized_image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Call Claude 3 Haiku API
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this screenshot focusing on: UI elements (buttons, forms, menus), color scheme and theme, main content type, any error messages or notifications, layout structure. Be concise but comprehensive."
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ]
            )
            
            description = response.content[0].text
            
            # Cache the result
            if use_cache:
                self.vision_cache[img_hash] = description
            
            return description
            
        except Exception as e:
            print(f"Claude API call failed: {e}")
            return self._get_fallback_description()
    
    def _get_fallback_description(self) -> str:
        """
        Generate basic description when API is unavailable.
        
        Returns:
            Basic fallback description
        """
        return "Visual description unavailable (API key not configured or API error)"
    
    def process_image(self, image_path: str) -> Dict[str, str]:
        """
        Process a single image file.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Dictionary with OCR text, vision description, and combined text
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Extract OCR text
            ocr_text = self.extract_ocr_text(image)
            
            # Get vision description
            vision_desc = self.get_vision_description(image)
            
            # Combine texts for search
            combined_text = f"{ocr_text}\n\n{vision_desc}"
            
            return {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'ocr_text': ocr_text,
                'vision_description': vision_desc,
                'combined_text': combined_text
            }
            
        except Exception as e:
            print(f"Failed to process {image_path}: {e}")
            return {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'ocr_text': '',
                'vision_description': '',
                'combined_text': ''
            }
    
    def process_batch(self, image_paths: List[str]) -> List[Dict[str, str]]:
        """
        Process multiple images in batch.
        
        Args:
            image_paths: List of image file paths
        
        Returns:
            List of processed image dictionaries
        """
        results = []
        for path in image_paths:
            result = self.process_image(path)
            results.append(result)
        return results