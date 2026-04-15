#!/usr/bin/env python3
"""
Publish Xiaohongshu image notes from explicit image paths or a renderer manifest.

Priority for cookie loading:
1) --cookie argument
2) XHS_COOKIE environment variable
3) .env files in known locations (current directory / skill directory)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def parse_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return values

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def cookie_search_paths() -> List[Path]:
    script_dir = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / ".env",
        script_dir.parent / ".env",
        script_dir.parent.parent / ".env",
    ]
    # Keep order stable and deduplicate.
    seen: set[str] = set()
    unique: List[Path] = []
    for path in candidates:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def load_cookie(explicit_cookie: str = "") -> str:
    if explicit_cookie.strip():
        return explicit_cookie.strip()

    env_cookie = os.getenv("XHS_COOKIE", "").strip()
    if env_cookie:
        return env_cookie

    for env_path in cookie_search_paths():
        if not env_path.exists():
            continue
        values = parse_env_file(env_path)
        cookie = values.get("XHS_COOKIE", "").strip()
        if cookie:
            print(f"Using cookie from: {env_path}")
            return cookie

    print("XHS cookie not found.")
    print("Set XHS_COOKIE in env/.env, or pass --cookie.")
    return ""


def parse_cookie(cookie_string: str) -> Dict[str, str]:
    cookies: Dict[str, str] = {}
    for item in cookie_string.split(";"):
        item = item.strip()
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        cookies[key.strip()] = value.strip()
    return cookies


def validate_cookie(cookie_string: str) -> bool:
    parsed = parse_cookie(cookie_string)
    required = ["a1", "web_session"]
    missing = [name for name in required if name not in parsed]
    if missing:
        print(f"Warning: cookie may be incomplete, missing: {', '.join(missing)}")
        return False
    return True


def resolve_manifest_images(manifest_path: Path) -> tuple[List[str], Dict[str, Any]]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    output_dir_raw = data.get("output_dir", str(manifest_path.parent))
    output_dir = Path(output_dir_raw).expanduser().resolve()
    cards = data.get("cards", [])
    images: List[str] = []
    for card in cards:
        candidate = Path(card)
        if not candidate.is_absolute():
            candidate = output_dir / card
        images.append(str(candidate.resolve()))
    return images, data


def validate_images(image_paths: List[str]) -> List[str]:
    valid: List[str] = []
    for raw in image_paths:
        path = Path(raw).expanduser().resolve()
        if path.exists():
            valid.append(str(path))
        else:
            print(f"Warning: image not found: {path}")
    return valid


def publish_local(
    cookie: str,
    title: str,
    desc: str,
    images: List[str],
    is_private: bool,
    post_time: Optional[str],
) -> Dict[str, Any]:
    try:
        from xhs import XhsClient
        from xhs.help import sign as local_sign
    except ImportError as exc:
        print(f"Missing dependency: {exc}")
        print("Install with: python3 -m pip install xhs")
        raise SystemExit(1) from exc

    parsed = parse_cookie(cookie)
    a1_value = parsed.get("a1", "")

    def sign_func(uri, data=None, a1="", web_session="", **kwargs):
        return local_sign(uri, data, a1=a1_value or a1)

    client = XhsClient(cookie=cookie, sign=sign_func)
    result = client.create_image_note(
        title=title,
        desc=desc,
        files=images,
        is_private=is_private,
        post_time=post_time,
    )
    return result if isinstance(result, dict) else {"raw_result": result}


def publish_api(
    cookie: str,
    title: str,
    desc: str,
    images: List[str],
    is_private: bool,
    post_time: Optional[str],
    api_url: str,
) -> Dict[str, Any]:
    try:
        import requests
    except ImportError as exc:
        print(f"Missing dependency: {exc}")
        print("Install with: python3 -m pip install requests")
        raise SystemExit(1) from exc

    session_id = "md_to_xhs_cards_session"
    init_resp = requests.post(
        f"{api_url}/init",
        json={"session_id": session_id, "cookie": cookie},
        timeout=30,
    )
    init_result = init_resp.json()
    if init_resp.status_code != 200 or init_result.get("status") not in {"success", "warning"}:
        raise RuntimeError(f"API init failed: {init_result}")

    payload: Dict[str, Any] = {
        "session_id": session_id,
        "title": title,
        "desc": desc,
        "files": images,
        "is_private": is_private,
    }
    if post_time:
        payload["post_time"] = post_time

    publish_resp = requests.post(f"{api_url}/publish/image", json=payload, timeout=120)
    publish_result = publish_resp.json()
    if publish_resp.status_code == 200 and publish_result.get("status") == "success":
        raw = publish_result.get("result", {})
        return raw if isinstance(raw, dict) else {"raw_result": raw}
    raise RuntimeError(f"API publish failed: {publish_result}")


def choose_title(explicit_title: str, manifest_data: Dict[str, Any], manifest_path: Optional[Path]) -> str:
    if explicit_title.strip():
        title = explicit_title.strip()
    else:
        cover = manifest_data.get("cover", {}) if manifest_data else {}
        title = str(cover.get("title", "")).strip()
        if not title and manifest_path:
            source = str(manifest_data.get("source_markdown", "")).strip()
            if source:
                title = Path(source).stem
            else:
                title = manifest_path.stem
    if not title:
        title = "小红书图文"
    if len(title) > 20:
        print("Title exceeds 20 chars and will be truncated.")
        title = title[:20]
    return title


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish Xiaohongshu image notes from cards/manifest.")
    parser.add_argument("--manifest", help="Path to manifest.json generated by md_to_xhs_cards.py.")
    parser.add_argument("--images", nargs="+", help="Explicit image list (overrides manifest images).")
    parser.add_argument("--title", default="", help="Note title (<=20 chars recommended).")
    parser.add_argument("--desc", default="", help="Note description/body.")
    parser.add_argument("--cookie", default="", help="XHS cookie string override.")
    parser.add_argument("--private", action="store_true", help="Publish as private note.")
    parser.add_argument("--post-time", default=None, help="Scheduled time: YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--api-mode", action="store_true", help="Publish via xhs-api service.")
    parser.add_argument("--api-url", default="", help="xhs-api base URL (default from XHS_API_URL or localhost).")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, do not publish.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest_data: Dict[str, Any] = {}
    manifest_path: Optional[Path] = None

    images: List[str] = []
    if args.images:
        images = args.images
    elif args.manifest:
        manifest_path = Path(args.manifest).expanduser().resolve()
        if not manifest_path.exists():
            print(f"Manifest not found: {manifest_path}")
            return 1
        images, manifest_data = resolve_manifest_images(manifest_path)
    else:
        print("Provide --images or --manifest.")
        return 1

    valid_images = validate_images(images)
    if not valid_images:
        print("No valid images to publish.")
        return 1

    title = choose_title(args.title, manifest_data, manifest_path)
    desc = args.desc.strip()

    cookie = load_cookie(args.cookie)
    if not cookie:
        return 1
    validate_cookie(cookie)

    api_url = args.api_url.strip() or os.getenv("XHS_API_URL", "http://localhost:5005")

    if args.dry_run:
        print("Dry run passed.")
        print(f"Title: {title}")
        print(f"Images: {len(valid_images)}")
        print(f"Private: {args.private}")
        print(f"API mode: {args.api_mode}")
        if args.post_time:
            print(f"Post time: {args.post_time}")
        return 0

    try:
        if args.api_mode:
            result = publish_api(
                cookie=cookie,
                title=title,
                desc=desc,
                images=valid_images,
                is_private=args.private,
                post_time=args.post_time,
                api_url=api_url,
            )
        else:
            result = publish_local(
                cookie=cookie,
                title=title,
                desc=desc,
                images=valid_images,
                is_private=args.private,
                post_time=args.post_time,
            )
    except Exception as exc:
        print(f"Publish failed: {exc}")
        return 1

    note_id = result.get("note_id") or result.get("id")
    print("Publish success.")
    if note_id:
        print(f"Note ID: {note_id}")
        print(f"URL: https://www.xiaohongshu.com/explore/{note_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
