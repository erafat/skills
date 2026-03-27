#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, parse, request


API_BASE = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_OUTPUT = Path("resources/images/generated")
DEFAULT_PAGE_SIZE = 200
KEYCHAIN_SERVICE = "codex-gemini-api-key"
SUPPORTED_ASPECT_RATIOS = {
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
}
SUPPORTED_IMAGE_SIZES = {"1k", "2k", "4k"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate images with the Gemini API using the Interactions endpoint. "
            "Provide a prompt directly or with --prompt-file."
        )
    )
    parser.add_argument(
        "--api-key",
        help=(
            "Gemini API key. Falls back to GEMINI_API_KEY, then GOOGLE_API_KEY, "
            f"then macOS Keychain service '{KEYCHAIN_SERVICE}'."
        ),
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model name to use. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--prompt",
        help="Prompt text for the image generation request.",
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        help="Path to a UTF-8 text file containing the prompt.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=(
            "Output file or directory. If a directory is provided, files are saved "
            "as <slug>-<index>.<ext>. Default: resources/images/generated"
        ),
    )
    parser.add_argument(
        "--aspect-ratio",
        choices=sorted(SUPPORTED_ASPECT_RATIOS),
        help="Optional image aspect ratio.",
    )
    parser.add_argument(
        "--image-size",
        choices=sorted(SUPPORTED_IMAGE_SIZES),
        help="Optional image size preset.",
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List models returned by the Gemini API and exit.",
    )
    parser.add_argument(
        "--show-all-models",
        action="store_true",
        help="With --list-models, include non-image models too.",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=DEFAULT_PAGE_SIZE,
        help=f"Page size for --list-models. Default: {DEFAULT_PAGE_SIZE}",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Retry count for transient 5xx Gemini API failures. Default: 3",
    )
    return parser


def read_keychain_api_key() -> str | None:
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                os.getenv("USER", ""),
                "-s",
                KEYCHAIN_SERVICE,
                "-w",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    key = result.stdout.strip()
    return key or None


def resolve_api_key(explicit_key: str | None) -> str:
    key = (
        explicit_key
        or os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or read_keychain_api_key()
    )
    if not key:
        raise SystemExit(
            "Missing API key. Pass --api-key, set GEMINI_API_KEY / GOOGLE_API_KEY, "
            f"or save it in macOS Keychain as service '{KEYCHAIN_SERVICE}'."
        )
    return key


def slugify(text: str, limit: int = 48) -> str:
    chars: list[str] = []
    last_was_dash = False
    for char in text.lower():
        if char.isalnum():
            chars.append(char)
            last_was_dash = False
        elif not last_was_dash and chars:
            chars.append("-")
            last_was_dash = True
        if len(chars) >= limit:
            break
    slug = "".join(chars).strip("-")
    return slug or "gemini-image"


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt and args.prompt_file:
        raise SystemExit("Use either --prompt or --prompt-file, not both.")
    if args.prompt_file:
        return args.prompt_file.read_text(encoding="utf-8").strip()
    if args.prompt:
        return args.prompt.strip()
    raise SystemExit("A prompt is required. Use --prompt or --prompt-file.")


def api_request(
    *,
    api_key: str,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    query: dict[str, Any] | None = None,
    retries: int = 1,
) -> dict[str, Any]:
    url = f"{API_BASE}{path}"
    if query:
        filtered_query = {key: value for key, value in query.items() if value is not None}
        url = f"{url}?{parse.urlencode(filtered_query)}"

    body = None
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    req = request.Request(url, data=body, headers=headers, method=method.upper())
    attempts = max(1, retries)
    last_error: BaseException | None = None

    for attempt in range(1, attempts + 1):
        try:
            with request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last_error = SystemExit(
                f"Gemini API request failed ({exc.code}): {detail}"
            )
            if exc.code >= 500 and attempt < attempts:
                time.sleep(min(2 ** (attempt - 1), 8))
                continue
            raise last_error from exc
        except error.URLError as exc:
            last_error = SystemExit(f"Gemini API request failed: {exc.reason}")
            if attempt < attempts:
                time.sleep(min(2 ** (attempt - 1), 8))
                continue
            raise last_error from exc

    if last_error is not None:
        raise last_error
    raise SystemExit("Gemini API request failed for an unknown reason.")


def infer_extension(mime_type: str) -> str:
    guessed = mimetypes.guess_extension(mime_type)
    if guessed == ".jpe":
        return ".jpg"
    if guessed:
        return guessed
    return ".bin"


def ensure_output_path(output: Path, prompt: str, index: int, extension: str) -> Path:
    if output.suffix:
        if index > 1:
            stem = output.stem
            return output.with_name(f"{stem}-{index}{output.suffix}")
        return output

    output.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(prompt)}-{index}{extension}"
    return output / filename


def save_images(interaction: dict[str, Any], output: Path, prompt: str) -> list[Path]:
    outputs = interaction.get("outputs", [])
    saved_paths: list[Path] = []
    image_index = 0

    for item in outputs:
        if item.get("type") != "image":
            continue
        data = item.get("data")
        mime_type = item.get("mime_type", "application/octet-stream")
        if not data:
            continue

        image_index += 1
        extension = infer_extension(mime_type)
        destination = ensure_output_path(output, prompt, image_index, extension)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(base64.b64decode(data))
        saved_paths.append(destination)

    if not saved_paths:
        raise SystemExit(
            "The API response did not include image output. "
            "Try a different image-capable model."
        )
    return saved_paths


def build_generation_payload(args: argparse.Namespace, prompt: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": args.model,
        "input": prompt,
        "response_modalities": ["IMAGE"],
    }

    image_config: dict[str, str] = {}
    if args.aspect_ratio:
        image_config["aspect_ratio"] = args.aspect_ratio
    if args.image_size:
        image_config["image_size"] = args.image_size
    if image_config:
        payload["generation_config"] = {"image_config": image_config}

    return payload


def looks_like_image_model(model: dict[str, Any]) -> bool:
    searchable_fields = [
        model.get("name", ""),
        model.get("baseModelId", ""),
        model.get("displayName", ""),
        model.get("description", ""),
    ]
    haystack = " ".join(searchable_fields).lower()
    return "image" in haystack or "imagen" in haystack


def list_models(api_key: str, page_size: int, show_all: bool) -> int:
    response = api_request(
        api_key=api_key,
        method="GET",
        path="/models",
        query={"pageSize": max(1, min(page_size, 1000))},
        retries=1,
    )
    models = response.get("models", [])
    if not show_all:
        models = [model for model in models if looks_like_image_model(model)]

    if not models:
        print("No matching models found.", file=sys.stderr)
        return 1

    for model in models:
        name = model.get("name", "").removeprefix("models/")
        display_name = model.get("displayName", "")
        description = model.get("description", "").strip()
        print(name)
        if display_name:
            print(f"  display: {display_name}")
        if description:
            print(f"  desc: {description}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    api_key = resolve_api_key(args.api_key)

    if args.list_models:
        return list_models(api_key, args.page_size, args.show_all_models)

    prompt = read_prompt(args)
    payload = build_generation_payload(args, prompt)
    response = api_request(
        api_key=api_key,
        method="POST",
        path="/interactions",
        payload=payload,
        retries=args.retries,
    )
    saved_paths = save_images(response, args.output, prompt)

    print(f"Model: {args.model}")
    for path in saved_paths:
        print(f"Saved: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
