from stegano import lsb
from PyPDF2 import PdfReader, PdfWriter
import docx
import os
import logging
from typing import Optional, Union
from PIL import Image
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Watermarker:
    def __init__(self):
        self.image_quality = 95  # For JPEG quality when saving
        self.pdf_metadata_key = "/HushTag"  # Custom metadata key
        self.docx_property = "hush_tag"  # Custom document property

    def embed(self, file_path: str, watermark: str, output_path: str) -> bool:
        """Embed watermark into file with improved error handling"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Input file not found: {file_path}")

            ext = os.path.splitext(file_path)[1].lower()

            if ext in (".png", ".jpg", ".jpeg"):
                return self._embed_image(file_path, watermark, output_path)
            elif ext == ".pdf":
                return self._embed_pdf(file_path, watermark, output_path)
            elif ext == ".docx":
                return self._embed_docx(file_path, watermark, output_path)
            else:
                logger.error(f"Unsupported file format: {ext}")
                return False
        except Exception as e:
            logger.error(f"Error embedding watermark: {str(e)}", exc_info=True)
            return False

    def extract(self, file_path: str) -> Optional[str]:
        """Extract watermark from file with improved error handling"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Input file not found: {file_path}")

            ext = os.path.splitext(file_path)[1].lower()

            if ext in (".png", ".jpg", ".jpeg"):
                return self._extract_image(file_path)
            elif ext == ".pdf":
                return self._extract_pdf(file_path)
            elif ext == ".docx":
                return self._extract_docx(file_path)
            else:
                logger.error(f"Unsupported file format: {ext}")
                return None
        except Exception as e:
            logger.error(f"Error extracting watermark: {str(e)}", exc_info=True)
            return None

    def _embed_image(self, file_path: str, watermark: str, output_path: str) -> bool:
        """Embed watermark in image using LSB steganography"""
        try:
            # Convert to PNG if needed for better LSB results
            if not file_path.lower().endswith(".png"):
                with Image.open(file_path) as img:
                    temp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                    img.save(temp_png.name, "PNG")
                    secret = lsb.hide(temp_png.name, watermark)
                    os.unlink(temp_png.name)
            else:
                secret = lsb.hide(file_path, watermark)

            # Save with original format if possible
            if output_path.lower().endswith(".jpg") or output_path.lower().endswith(
                ".jpeg"
            ):
                secret.save(output_path, quality=self.image_quality)
            else:
                secret.save(output_path)
            return True
        except Exception as e:
            logger.error(f"Error embedding image watermark: {str(e)}")
            return False

    def _extract_image(self, file_path: str) -> Optional[str]:
        """Extract LSB watermark from image"""
        try:
            # Convert to PNG if needed for better LSB results
            if not file_path.lower().endswith(".png"):
                with Image.open(file_path) as img:
                    temp_png = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                    img.save(temp_png.name, "PNG")
                    result = lsb.reveal(temp_png.name)
                    os.unlink(temp_png.name)
                    return result
            return lsb.reveal(file_path)
        except Exception as e:
            logger.error(f"Error extracting image watermark: {str(e)}")
            return None

    def _embed_pdf(self, file_path: str, watermark: str, output_path: str) -> bool:
        """Embed watermark in PDF metadata"""
        try:
            reader = PdfReader(file_path)
            writer = PdfWriter()

            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)

            # Add custom metadata
            writer.add_metadata(
                {
                    self.pdf_metadata_key: watermark,
                    "/Creator": "HushTag Watermarking System",
                }
            )

            # Preserve existing metadata
            if reader.metadata:
                for key, value in reader.metadata.items():
                    if (
                        key != self.pdf_metadata_key
                    ):  # Don't overwrite existing watermark
                        writer.add_metadata({key: value})

            with open(output_path, "wb") as f:
                writer.write(f)
            return True
        except Exception as e:
            logger.error(f"Error embedding PDF watermark: {str(e)}")
            return False

    def _extract_pdf(self, file_path: str) -> Optional[str]:
        """Extract watermark from PDF metadata"""
        try:
            reader = PdfReader(file_path)
            return reader.metadata.get(self.pdf_metadata_key, None)
        except Exception as e:
            logger.error(f"Error extracting PDF watermark: {str(e)}")
            return None

    def _embed_docx(self, file_path: str, watermark: str, output_path: str) -> bool:
        """Embed watermark in DOCX custom properties"""
        try:
            doc = docx.Document(file_path)

            # Set both standard and custom properties
            doc.core_properties.author = "HushTag Watermarked Document"
            doc.core_properties.comments = watermark

            # Add custom document property
            if not hasattr(doc.core_properties, self.docx_property):
                doc.core_properties.add_custom_property(self.docx_property, watermark)
            else:
                setattr(doc.core_properties, self.docx_property, watermark)

            doc.save(output_path)
            return True
        except Exception as e:
            logger.error(f"Error embedding DOCX watermark: {str(e)}")
            return False

    def _extract_docx(self, file_path: str) -> Optional[str]:
        """Extract watermark from DOCX properties"""
        try:
            doc = docx.Document(file_path)

            # First try custom property
            if hasattr(doc.core_properties, self.docx_property):
                return getattr(doc.core_properties, self.docx_property)

            # Fallback to comments
            if doc.core_properties.comments:
                return doc.core_properties.comments

            return None
        except Exception as e:
            logger.error(f"Error extracting DOCX watermark: {str(e)}")
            return None


# Maintain original function interface for backward compatibility
def embed_watermark(file_path: str, watermark: str, output_path: str) -> bool:
    return Watermarker().embed(file_path, watermark, output_path)


def extract_watermark(file_path: str) -> Optional[str]:
    return Watermarker().extract(file_path)
