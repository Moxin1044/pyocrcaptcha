"""Public API for fixed-width image CAPTCHA recognition."""

from .ocr import CaptchaOCR, CaptchaResult

__all__ = ["CaptchaOCR", "CaptchaResult"]
__version__ = "1.0.0"
