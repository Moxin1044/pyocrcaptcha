"""YOLO-backed CAPTCHA OCR implementation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Union

from PIL import Image
from ultralytics import YOLO

PathLike = Union[str, Path]


@dataclass(frozen=True)
class CaptchaResult:
    """Recognition result with per-character confidence information."""

    text: str
    confidence: float
    character_confidences: tuple[float, ...]
    positions: int

    def __str__(self) -> str:
        return self.text


class CaptchaOCR:
    """Recognize fixed-width 4- or 5-character image CAPTCHAs.

    Args:
        model: Optional path to a YOLO classification model. If omitted, the
            package's bundled model is used.
        positions: Character count to force. ``None`` auto-tests 4 and 5.
        imgsz: YOLO classification input size.
        device: Ultralytics device selector, for example ``"cpu"`` or ``0``.
    """

    def __init__(self, model: PathLike | None = None, positions: int | None = None,
                 imgsz: int = 96, device: str | int | None = None) -> None:
        self.model_path = Path(model) if model is not None else Path(__file__).with_name("models") / "captcha-character-classifier-yolo11n-100e.pt"
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")
        if positions is not None and positions < 1:
            raise ValueError("positions must be at least 1")
        self.positions = positions
        self.imgsz = imgsz
        self.device = device
        kwargs = {} if device is None else {"device": device}
        self.model = YOLO(str(self.model_path), **kwargs)

    def recognize(self, image: PathLike, positions: int | None = None) -> CaptchaResult:
        """Recognize an image and return a structured :class:`CaptchaResult`."""
        requested = positions if positions is not None else self.positions
        counts = (requested,) if requested is not None else (4, 5)
        candidates = [self._recognize_fixed(image, count) for count in counts]
        return max(candidates, key=lambda result: result.confidence)

    def __call__(self, image: PathLike, positions: int | None = None) -> str:
        """Recognize an image and return only the decoded text."""
        return self.recognize(image, positions=positions).text

    def _recognize_fixed(self, image_path: PathLike, positions: int) -> CaptchaResult:
        if positions < 1:
            raise ValueError("positions must be at least 1")
        with Image.open(image_path) as source:
            image = source.convert("RGB")
            width, height = image.size
            if width % positions:
                raise ValueError(f"Image width {width} is not divisible by {positions}")
            char_width = width // positions
            characters: list[str] = []
            confidences: list[float] = []
            for index in range(positions):
                crop = image.crop((index * char_width, 0, (index + 1) * char_width, height))
                kwargs = {} if self.device is None else {"device": self.device}
                prediction = self.model.predict(source=crop, imgsz=self.imgsz, verbose=False, **kwargs)[0]
                top1 = int(prediction.probs.top1)
                characters.append(str(prediction.names[top1]))
                confidences.append(float(prediction.probs.top1conf))
        return CaptchaResult("".join(characters), sum(confidences) / positions,
                             tuple(confidences), positions)
