#!/usr/bin/env python3
"""
Generate a Swiss editorial flat illustration via Imagen 4 API.
Reads GEMINI_API_KEY from ~/.baoyu-skills/.env

Usage:
    python3 gen_illustration.py "your prompt text" output.png
    python3 gen_illustration.py "your prompt text" output.png --ratio 4:3
    python3 gen_illustration.py "your prompt text" output.png --ratio 1:1
"""

import os
import sys
import base64
import argparse
import requests
from pathlib import Path


def load_api_key():
    env_path = Path.home() / ".baoyu-skills" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    sys.exit("ERROR: GEMINI_API_KEY not found in ~/.baoyu-skills/.env or environment")


# The canonical Swiss editorial flat style suffix — append to any subject prompt.
STYLE_SUFFIX = (
    "Swiss editorial flat illustration, warm ivory cream background filling the entire frame "
    "edge to edge, thin refined ink outlines, muted desaturated palette — off-white coats, "
    "warm cream walls, slate grey and muted gray-blue clothing, natural skin tones, "
    "characters with clearly drawn faces (eyes, nose, mouth), soft natural expressions, "
    "realistic human proportions, diverse representation, no orange no amber no yellow no ochre, "
    "no gradients, no texture, no text, no labels."
)


def generate(prompt: str, out_path: str, ratio: str = "4:3") -> None:
    api_key = load_api_key()
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"imagen-4.0-generate-001:predict?key={api_key}"
    )

    full_prompt = f"{prompt.rstrip('.')}. {STYLE_SUFFIX}"

    resp = requests.post(endpoint, json={
        "instances": [{"prompt": full_prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": ratio},
    }, timeout=60)

    if resp.status_code != 200:
        sys.exit(f"ERROR {resp.status_code}: {resp.text[:400]}")

    b64 = resp.json()["predictions"][0]["bytesBase64Encoded"]
    Path(out_path).write_bytes(base64.b64decode(b64))
    print(f"Saved: {out_path}")

    # Print data URI for direct embedding in HTML
    data_uri = f"data:image/png;base64,{b64}"
    print(f"\nData URI (first 80 chars): {data_uri[:80]}...")
    print(f"\nEmbed in HTML:\n  <img src=\"{data_uri[:40]}...\" ...>")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Swiss editorial illustration")
    parser.add_argument("prompt", help="Subject description (style suffix auto-appended)")
    parser.add_argument("output", help="Output PNG file path")
    parser.add_argument("--ratio", default="4:3", choices=["4:3", "1:1", "16:9", "3:4"],
                        help="Aspect ratio (default: 4:3)")
    args = parser.parse_args()
    generate(args.prompt, args.output, args.ratio)
