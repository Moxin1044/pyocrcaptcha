"""Command line interface for pyocrcaptcha."""

from __future__ import annotations

import argparse
from pathlib import Path

from .ocr import CaptchaOCR


def main() -> int:
    parser = argparse.ArgumentParser(description="Recognize a fixed-width image CAPTCHA")
    parser.add_argument("image", type=Path, help="Path to the CAPTCHA image")
    parser.add_argument("--model", type=Path, default=None, help="Optional YOLO model path")
    parser.add_argument("--positions", type=int, choices=(4, 5), default=None,
                        help="Force character count; default auto-tests 4 and 5")
    parser.add_argument("--imgsz", type=int, default=96)
    parser.add_argument("--device", default=None, help="cpu, 0, 1, ...")
    parser.add_argument("--details", action="store_true", help="Print confidence details")
    args = parser.parse_args()
    result = CaptchaOCR(args.model, args.positions, args.imgsz, args.device).recognize(args.image)
    if args.details:
        print(f"{result.text}\tconfidence={result.confidence:.4f}\tpositions={result.positions}")
    else:
        print(result.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
