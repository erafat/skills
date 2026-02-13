#!/usr/bin/env python3
"""
Render a Markdown file into Xiaohongshu-style image cards.

The renderer is deterministic and keeps source order:
- headings
- paragraphs
- lists
- blockquotes
- fenced code blocks
- horizontal rules
- local images (from markdown image syntax)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

try:
    from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
except ImportError as exc:
    print("Missing dependency: Pillow (PIL). Install with: python -m pip install pillow")
    raise SystemExit(1) from exc


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
OBS_IMAGE_RE = re.compile(r"!\[\[([^\]]+)\]\]")
ORDERED_ITEM_RE = re.compile(r"^\s*(\d+)\.\s+(.*)$")
UNORDERED_ITEM_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
HR_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")
WIDE_DASH_HR_RE = re.compile(r"^\s*[—－]{3,}\s*$")
FENCE_RE = re.compile(r"^\s*```")
STRONG_ONLY_RE = re.compile(r"^\s*(\*\*|__)\s*(.+?)\s*\1\s*$")


def strip_inline_markdown(text: str) -> str:
    """Reduce inline markdown to plain text while preserving semantics."""
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r"\1", text)
    text = re.sub(r"!\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?\]\]", r"\3", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    return text.strip()


def split_obsidian_embed(token: str) -> tuple[str, str]:
    """
    Parse Obsidian embed payload.

    Examples:
    - cover.png
    - folder/cover.png|Caption
    - cover.png|800
    - cover.png#anchor|Caption
    """
    parts = [part.strip() for part in token.split("|")]
    raw_src = parts[0]
    src = raw_src.split("#", 1)[0].strip()
    alt = ""
    for candidate in parts[1:]:
        if not candidate:
            continue
        # Ignore size hints like 800 or 800x600.
        if re.fullmatch(r"\d+(x\d+)?", candidate):
            continue
        alt = candidate
        break
    return src, alt


def find_vault_root(start: Path) -> Optional[Path]:
    current = start.resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / ".obsidian").exists():
            return candidate
    return None


@dataclass
class Block:
    kind: str
    text: str = ""
    level: int = 0
    items: Optional[List[str]] = None
    ordered: bool = False
    alt: str = ""
    src: str = ""


@dataclass
class CoverSpec:
    image_src: str = ""
    title: str = ""
    subtitle: str = ""
    author: str = ""


def parse_markdown(content: str) -> List[Block]:
    blocks: List[Block] = []
    lines = content.splitlines()
    i = 0

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if not line.strip():
            i += 1
            continue

        if FENCE_RE.match(line):
            code_lines: List[str] = []
            i += 1
            while i < len(lines) and not FENCE_RE.match(lines[i]):
                code_lines.append(lines[i].rstrip("\n"))
                i += 1
            if i < len(lines):
                i += 1
            blocks.append(Block(kind="code", text="\n".join(code_lines).rstrip()))
            continue

        heading = HEADING_RE.match(line)
        if heading:
            blocks.append(
                Block(
                    kind="heading",
                    level=min(len(heading.group(1)), 6),
                    text=strip_inline_markdown(heading.group(2)),
                )
            )
            i += 1
            continue

        if HR_RE.match(line) or WIDE_DASH_HR_RE.match(line):
            blocks.append(Block(kind="hr"))
            i += 1
            continue

        image = IMAGE_RE.fullmatch(line.strip())
        if image:
            blocks.append(
                Block(
                    kind="image",
                    alt=image.group(1).strip(),
                    src=image.group(2).strip().strip('"').strip("'"),
                )
            )
            i += 1
            continue

        obs_image = OBS_IMAGE_RE.fullmatch(line.strip())
        if obs_image:
            src, alt = split_obsidian_embed(obs_image.group(1))
            blocks.append(Block(kind="image", alt=alt, src=src))
            i += 1
            continue

        if line.lstrip().startswith(">"):
            quote_lines: List[str] = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote_lines.append(lines[i].lstrip()[1:].lstrip())
                i += 1
            blocks.append(Block(kind="quote", text=strip_inline_markdown("\n".join(quote_lines))))
            continue

        strong_only = STRONG_ONLY_RE.match(line)
        if strong_only:
            blocks.append(Block(kind="subheading", text=strip_inline_markdown(strong_only.group(2))))
            i += 1
            continue

        ordered_match = ORDERED_ITEM_RE.match(line)
        unordered_match = UNORDERED_ITEM_RE.match(line)
        if ordered_match or unordered_match:
            ordered = bool(ordered_match)
            items: List[str] = []
            while i < len(lines):
                candidate = lines[i].rstrip()
                if ordered:
                    matched = ORDERED_ITEM_RE.match(candidate)
                    if not matched:
                        break
                    items.append(strip_inline_markdown(matched.group(2)))
                else:
                    matched = UNORDERED_ITEM_RE.match(candidate)
                    if not matched:
                        break
                    items.append(strip_inline_markdown(matched.group(1)))
                i += 1
            blocks.append(Block(kind="list", items=items, ordered=ordered))
            continue

        paragraph_lines: List[str] = []
        while i < len(lines):
            candidate = lines[i].rstrip()
            if not candidate.strip():
                break
            if (
                HEADING_RE.match(candidate)
                or FENCE_RE.match(candidate)
                or IMAGE_RE.fullmatch(candidate.strip())
                or OBS_IMAGE_RE.fullmatch(candidate.strip())
                or candidate.lstrip().startswith(">")
                or STRONG_ONLY_RE.match(candidate)
                or ORDERED_ITEM_RE.match(candidate)
                or UNORDERED_ITEM_RE.match(candidate)
                or HR_RE.match(candidate)
                or WIDE_DASH_HR_RE.match(candidate)
            ):
                break
            paragraph_lines.append(candidate.strip())
            i += 1

        if paragraph_lines:
            blocks.append(Block(kind="paragraph", text=strip_inline_markdown(" ".join(paragraph_lines))))
        else:
            i += 1

    return blocks


def prepare_cover(
    blocks: List[Block],
    markdown_path: Path,
    mode: str,
    title_override: Optional[str],
    subtitle_override: Optional[str],
    author_override: Optional[str],
    image_override: Optional[str],
) -> tuple[Optional[CoverSpec], List[Block]]:
    remaining = list(blocks)
    first_is_image = bool(remaining and remaining[0].kind == "image")
    auto_trigger = bool(first_is_image or image_override or title_override or subtitle_override or author_override)
    should_create = mode == "force" or (mode == "auto" and auto_trigger)
    if mode == "off" or not should_create:
        return None, remaining

    cover = CoverSpec()

    if image_override:
        cover.image_src = image_override.strip()
    elif remaining and remaining[0].kind == "image":
        cover.image_src = remaining.pop(0).src

    while remaining and remaining[0].kind == "hr":
        remaining.pop(0)

    if title_override:
        cover.title = title_override.strip()
    elif remaining and remaining[0].kind == "heading":
        cover.title = remaining.pop(0).text.strip()
    else:
        cover.title = markdown_path.stem.strip()

    while remaining and remaining[0].kind == "hr":
        remaining.pop(0)

    if subtitle_override:
        cover.subtitle = subtitle_override.strip()
    elif remaining and remaining[0].kind == "paragraph":
        first_paragraph = remaining[0].text.strip()
        if first_paragraph and len(first_paragraph) <= 48:
            cover.subtitle = remaining.pop(0).text.strip()

    while remaining and remaining[0].kind == "hr":
        remaining.pop(0)

    if author_override:
        cover.author = author_override.strip()

    return cover, remaining


@dataclass
class RenderConfig:
    width: int
    height: int
    margin: int
    background: str
    text_color: str
    muted_color: str
    accent_color: str
    image_border: str
    quote_bg: str
    quote_border: str
    quote_accent: str
    line_height_scale: float
    block_gap: int
    image_max_ratio: float
    output_dir: Path
    source_dir: Path
    font_serif_path: Optional[str] = None
    font_sans_path: Optional[str] = None
    font_mono_path: Optional[str] = None


class MarkdownCardRenderer:
    def __init__(self, config: RenderConfig):
        self.config = config
        self.page_index = 0
        self.cards: List[Path] = []
        self.missing_images: List[str] = []
        self.vault_root = find_vault_root(self.config.source_dir)
        self._image_lookup_cache: dict[str, Optional[Path]] = {}
        self._new_page()
        self._load_fonts()

    def _load_font(
        self,
        size: int,
        preferred: Optional[str],
        candidates: Iterable[str],
    ) -> ImageFont.FreeTypeFont:
        def _parse_spec(spec: str) -> tuple[str, int]:
            if "::" not in spec:
                return spec, 0
            raw_path, raw_index = spec.rsplit("::", 1)
            try:
                return raw_path, int(raw_index)
            except ValueError:
                return raw_path, 0

        if preferred:
            try:
                return ImageFont.truetype(preferred, size=size)
            except OSError:
                pass
        for spec in candidates:
            path, font_index = _parse_spec(spec)
            if Path(path).exists():
                try:
                    return ImageFont.truetype(path, size=size, index=font_index)
                except OSError:
                    continue
        return ImageFont.load_default()

    def _load_fonts(self) -> None:
        self.font_body = self._load_font(
            42,
            self.config.font_serif_path,
            [
                "/System/Library/Fonts/Supplemental/Songti.ttc::3",
                "/System/Library/Fonts/Supplemental/Songti.ttc::6",
                "/System/Library/Fonts/Supplemental/Songti.ttc::4",
                "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
                "/System/Library/Fonts/Times.ttc",
            ],
        )
        self.font_h1 = self._load_font(
            70,
            self.config.font_serif_path,
            [
                "/System/Library/Fonts/Supplemental/Songti.ttc::0",
                "/System/Library/Fonts/Supplemental/Songti.ttc::1",
                "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
                "/System/Library/Fonts/Times.ttc",
            ],
        )
        self.font_h2 = self._load_font(
            58,
            self.config.font_serif_path,
            [
                "/System/Library/Fonts/Supplemental/Songti.ttc::1",
                "/System/Library/Fonts/Supplemental/Songti.ttc::6",
                "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
                "/System/Library/Fonts/Times.ttc",
            ],
        )
        self.font_h3 = self._load_font(
            50,
            self.config.font_serif_path,
            [
                "/System/Library/Fonts/Supplemental/Songti.ttc::6",
                "/System/Library/Fonts/Supplemental/Songti.ttc::4",
                "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
                "/System/Library/Fonts/Times.ttc",
            ],
        )
        self.font_subtitle = self._load_font(
            50,
            self.config.font_serif_path,
            [
                "/System/Library/Fonts/Supplemental/Songti.ttc::1",
                "/System/Library/Fonts/Supplemental/Songti.ttc::0",
                "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
                "/System/Library/Fonts/Times.ttc",
            ],
        )
        self.font_meta = self._load_font(
            32,
            self.config.font_sans_path,
            [
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/System/Library/Fonts/Helvetica.ttc",
                "/System/Library/Fonts/ArialHB.ttc",
            ],
        )
        self.font_code = self._load_font(
            32,
            self.config.font_mono_path,
            [
                "/System/Library/Fonts/SFNSMono.ttf",
                "/System/Library/Fonts/Menlo.ttc",
                "/System/Library/Fonts/Courier.ttc",
            ],
        )

    def _new_page(self) -> None:
        self.image = Image.new("RGB", (self.config.width, self.config.height), color=self.config.background)
        self.draw = ImageDraw.Draw(self.image)
        self.cursor_y = self.config.margin
        self.bottom_limit = self.config.height - self.config.margin
        self.page_has_content = False

    def _finish_current_page(self) -> None:
        if not self.page_has_content:
            return
        self.page_index += 1
        name = f"{self.page_index:02d}-card.png"
        path = self.config.output_dir / name
        self.image.save(path, format="PNG")
        self.cards.append(path)

    def _start_next_page(self) -> None:
        self._finish_current_page()
        self._new_page()

    def _line_height(self, font: ImageFont.ImageFont) -> int:
        box = self.draw.textbbox((0, 0), "A中", font=font)
        return int((box[3] - box[1]) * self.config.line_height_scale)

    def _measure_text(self, text: str, font: ImageFont.ImageFont) -> float:
        return self.draw.textlength(text, font=font)

    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
        lines: List[str] = []
        for paragraph in text.split("\n"):
            if not paragraph:
                lines.append("")
                continue
            current = ""
            for ch in paragraph:
                probe = current + ch
                if not current or self._measure_text(probe, font) <= max_width:
                    current = probe
                    continue
                lines.append(current.rstrip())
                current = ch
            if current:
                lines.append(current.rstrip())
        return lines or [""]

    def _draw_lines(
        self,
        lines: List[str],
        font: ImageFont.ImageFont,
        color: str,
        x: int,
        gap_after: int,
    ) -> None:
        line_height = self._line_height(font)
        for line in lines:
            if self.cursor_y + line_height > self.bottom_limit:
                self._start_next_page()
            self.draw.text((x, self.cursor_y), line, fill=color, font=font)
            self.page_has_content = True
            self.cursor_y += line_height
        self.cursor_y += gap_after

    def _render_heading(self, text: str, level: int) -> None:
        font = self.font_h1 if level == 1 else self.font_h2 if level == 2 else self.font_h3
        lines = self._wrap_text(text, font, self.config.width - self.config.margin * 2)
        self._draw_lines(
            lines,
            font,
            self.config.text_color,
            self.config.margin,
            self.config.block_gap + 10,
        )

    def _render_subheading(self, text: str) -> None:
        lines = self._wrap_text(text, self.font_subtitle, self.config.width - self.config.margin * 2)
        self._draw_lines(
            lines,
            self.font_subtitle,
            self.config.text_color,
            self.config.margin,
            self.config.block_gap + 6,
        )

    def _render_paragraph(self, text: str) -> None:
        lines = self._wrap_text(text, self.font_body, self.config.width - self.config.margin * 2)
        self._draw_lines(lines, self.font_body, self.config.text_color, self.config.margin, self.config.block_gap)

    def _render_list(self, items: List[str], ordered: bool) -> None:
        marker_width = int(self._measure_text("88. ", self.font_body))
        text_width = self.config.width - self.config.margin * 2 - marker_width
        line_height = self._line_height(self.font_body)

        for idx, item in enumerate(items, start=1):
            marker = f"{idx}." if ordered else "•"
            lines = self._wrap_text(item, self.font_body, text_width)
            if not lines:
                lines = [""]
            for line_i, line in enumerate(lines):
                if self.cursor_y + line_height > self.bottom_limit:
                    self._start_next_page()
                draw_marker = marker if line_i == 0 else ""
                self.draw.text(
                    (self.config.margin, self.cursor_y),
                    draw_marker,
                    fill=self.config.text_color,
                    font=self.font_body,
                )
                self.draw.text(
                    (self.config.margin + marker_width, self.cursor_y),
                    line,
                    fill=self.config.text_color,
                    font=self.font_body,
                )
                self.cursor_y += line_height
            self.cursor_y += 12

        self.cursor_y += self.config.block_gap

    def _render_quote(self, text: str) -> None:
        # Render quotes as a callout block for higher readability:
        # subtle background + accent bar + padded text.
        callout_left = self.config.margin
        callout_right = self.config.width - self.config.margin
        callout_width = callout_right - callout_left
        inner_pad_x = 26
        inner_pad_y = 18
        accent_width = 8
        accent_gap = 18
        quote_font = self.font_body
        line_height = self._line_height(quote_font)

        text_x = callout_left + inner_pad_x + accent_width + accent_gap
        text_width = callout_width - (inner_pad_x * 2 + accent_width + accent_gap)
        lines = self._wrap_text(text, quote_font, text_width)
        remaining = list(lines)

        while remaining:
            available_height = self.bottom_limit - self.cursor_y
            min_box_height = inner_pad_y * 2 + line_height
            if available_height < min_box_height:
                self._start_next_page()
                available_height = self.bottom_limit - self.cursor_y

            max_lines = max(1, int((available_height - inner_pad_y * 2) // line_height))
            chunk = remaining[:max_lines]
            remaining = remaining[max_lines:]

            box_height = inner_pad_y * 2 + len(chunk) * line_height
            top = self.cursor_y
            bottom = top + box_height

            self.draw.rounded_rectangle(
                [callout_left, top, callout_right, bottom],
                radius=18,
                fill=self.config.quote_bg,
                outline=self.config.quote_border,
                width=2,
            )
            self.page_has_content = True

            accent_left = callout_left + inner_pad_x
            accent_top = top + inner_pad_y - 2
            accent_bottom = bottom - inner_pad_y + 2
            self.draw.rounded_rectangle(
                [accent_left, accent_top, accent_left + accent_width, accent_bottom],
                radius=4,
                fill=self.config.quote_accent,
            )
            self.page_has_content = True

            y = top + inner_pad_y
            for line in chunk:
                self.draw.text((text_x, y), line, fill=self.config.text_color, font=quote_font)
                self.page_has_content = True
                y += line_height

            self.cursor_y = bottom + self.config.block_gap
            if remaining and self.cursor_y < self.bottom_limit:
                # Keep visual continuity between split quote chunks.
                self.cursor_y += 6

    def _render_code(self, text: str) -> None:
        code_lines = text.split("\n") if text else [""]
        wrapped: List[str] = []
        max_width = self.config.width - self.config.margin * 2 - 36
        for code_line in code_lines:
            wrapped.extend(self._wrap_text(code_line, self.font_code, max_width))

        line_height = self._line_height(self.font_code)
        block_height = 20 + len(wrapped) * line_height + 20
        if self.cursor_y + block_height > self.bottom_limit and self.cursor_y > self.config.margin:
            self._start_next_page()

        left = self.config.margin
        top = self.cursor_y
        right = self.config.width - self.config.margin
        bottom = min(self.bottom_limit, top + block_height)
        self.draw.rounded_rectangle(
            [left, top, right, bottom],
            radius=16,
            fill="#f0f0f0",
            outline="#dadada",
            width=2,
        )
        self.page_has_content = True

        y = top + 20
        for line in wrapped:
            if y + line_height > bottom - 12:
                break
            self.draw.text((left + 18, y), line, fill=self.config.accent_color, font=self.font_code)
            self.page_has_content = True
            y += line_height
        self.cursor_y = bottom + self.config.block_gap

    def _render_hr(self) -> None:
        h = 30
        if self.cursor_y + h > self.bottom_limit:
            self._start_next_page()
        y = self.cursor_y + 10
        self.draw.line(
            (self.config.margin, y, self.config.width - self.config.margin, y),
            fill=self.config.muted_color,
            width=3,
        )
        self.page_has_content = True
        self.cursor_y += h

    def _resolve_by_basename(self, basename: str) -> Optional[Path]:
        key = basename.lower()
        if key in self._image_lookup_cache:
            return self._image_lookup_cache[key]

        if not self.vault_root:
            self._image_lookup_cache[key] = None
            return None

        source_parts = self.config.source_dir.parts
        candidates = list(self.vault_root.rglob(basename))
        if not candidates:
            self._image_lookup_cache[key] = None
            return None

        def score(path: Path) -> tuple[int, int]:
            common = 0
            for a, b in zip(source_parts, path.parts):
                if a != b:
                    break
                common += 1
            return (-common, len(path.parts))

        best = sorted(candidates, key=score)[0]
        self._image_lookup_cache[key] = best
        return best

    def _resolve_image(self, src: str) -> Optional[Path]:
        if re.match(r"^(https?://|data:)", src):
            return None

        candidate = Path(src)
        if candidate.is_absolute():
            return candidate if candidate.exists() else None

        resolved = (self.config.source_dir / src).resolve()
        if resolved.exists():
            return resolved

        if self.vault_root:
            from_vault = (self.vault_root / src).resolve()
            if from_vault.exists():
                return from_vault

        basename = Path(src).name
        if basename:
            fallback = self._resolve_by_basename(basename)
            if fallback:
                return fallback

        return None

    def _render_image(self, src: str, alt: str) -> None:
        image_path = self._resolve_image(src)
        if not image_path:
            self.missing_images.append(src)
            self._render_paragraph(f"[Missing local image: {src}]")
            return

        with Image.open(image_path) as raw_image:
            picture = raw_image.convert("RGB")
        max_width = self.config.width - self.config.margin * 2
        max_height = int(self.config.height * self.config.image_max_ratio)
        picture = ImageOps.contain(picture, (max_width, max_height))

        caption_lines: List[str] = []
        caption_height = 0
        if alt:
            caption_lines = self._wrap_text(alt, self.font_meta, max_width)
            caption_height = len(caption_lines) * self._line_height(self.font_meta) + 8

        required = picture.height + caption_height + self.config.block_gap + 6
        if self.cursor_y + required > self.bottom_limit and self.cursor_y > self.config.margin:
            self._start_next_page()

        x = self.config.margin + (max_width - picture.width) // 2
        y = self.cursor_y
        self.image.paste(picture, (x, y))
        self.page_has_content = True
        self.draw.rectangle(
            [x - 2, y - 2, x + picture.width + 2, y + picture.height + 2],
            outline=self.config.image_border,
            width=2,
        )
        self.page_has_content = True
        self.cursor_y += picture.height + 12

        if caption_lines:
            self._draw_lines(
                caption_lines,
                self.font_meta,
                self.config.muted_color,
                self.config.margin,
                10,
            )

        self.cursor_y += self.config.block_gap

    def _render_cover(self, cover: CoverSpec, show_author: bool = False) -> None:
        max_width = self.config.width - self.config.margin * 2
        y = self.config.margin

        if cover.image_src:
            image_path = self._resolve_image(cover.image_src)
            if image_path:
                with Image.open(image_path) as raw_image:
                    picture = raw_image.convert("RGB")
                picture = ImageOps.contain(picture, (max_width, int(self.config.height * 0.44)))
                x = self.config.margin + (max_width - picture.width) // 2
                self.image.paste(picture, (x, y))
                self.page_has_content = True
                self.draw.rectangle(
                    [x - 2, y - 2, x + picture.width + 2, y + picture.height + 2],
                    outline=self.config.image_border,
                    width=2,
                )
                self.page_has_content = True
                y += picture.height + 30

        self.cursor_y = y
        if cover.title:
            title_lines = self._wrap_text(cover.title, self.font_h1, max_width)
            self._draw_lines(title_lines, self.font_h1, self.config.text_color, self.config.margin, 10)

        lower_section_top = max(int(self.config.height * 0.60), self.cursor_y + 16)
        self.cursor_y = lower_section_top

        if cover.subtitle:
            subtitle_lines = self._wrap_text(cover.subtitle, self.font_subtitle, max_width)
            self._draw_lines(
                subtitle_lines,
                self.font_subtitle,
                self.config.text_color,
                self.config.margin,
                18,
            )

        if show_author and cover.author:
            author_text = f"作者：{cover.author}"
            bar_left = self.config.margin
            bar_top = self.cursor_y + 6
            bar_height = self._line_height(self.font_meta) - 12
            self.draw.rectangle(
                [bar_left, bar_top, bar_left + 8, bar_top + max(8, bar_height)],
                fill=self.config.text_color,
            )
            self.page_has_content = True
            self.draw.text(
                (bar_left + 26, self.cursor_y),
                author_text,
                fill=self.config.text_color,
                font=self.font_meta,
            )
            self.page_has_content = True
            self.cursor_y += self._line_height(self.font_meta) + 10

        divider_y = self.config.height - self.config.margin - 30
        self.draw.line(
            (self.config.margin, divider_y, self.config.width - self.config.margin, divider_y),
            fill=self.config.muted_color,
            width=3,
        )
        self.page_has_content = True

    def _render_signature(self, signature_text: str) -> None:
        text = signature_text.strip()
        if not text:
            return
        if not text.startswith("--"):
            text = f"-- {text}"

        sig_font = self.font_meta
        box = self.draw.textbbox((0, 0), text, font=sig_font)
        text_width = box[2] - box[0]
        text_height = box[3] - box[1]
        x = self.config.width - self.config.margin - text_width

        # Keep signature close to body end (about 2-3 lines below content).
        line_gap = self._line_height(sig_font)
        desired_y = self.cursor_y + int(line_gap * 2.5)

        # If there is not enough space, place signature on a dedicated final page.
        if desired_y + text_height > self.bottom_limit:
            self._start_next_page()
            box = self.draw.textbbox((0, 0), text, font=sig_font)
            text_width = box[2] - box[0]
            text_height = box[3] - box[1]
            x = self.config.width - self.config.margin - text_width
            line_gap = self._line_height(sig_font)
            desired_y = self.cursor_y + int(line_gap * 2.5)

        y = min(desired_y, self.bottom_limit - text_height)

        self.draw.text((x, y), text, fill=self.config.muted_color, font=sig_font)
        self.page_has_content = True

    def render(
        self,
        blocks: List[Block],
        cover: Optional[CoverSpec] = None,
        signature_text: str = "",
        cover_author: bool = False,
    ) -> List[Path]:
        if cover:
            self._render_cover(cover, show_author=cover_author)
            self._start_next_page()

        for block in blocks:
            if block.kind == "heading":
                self._render_heading(block.text, block.level)
            elif block.kind == "subheading":
                self._render_subheading(block.text)
            elif block.kind == "paragraph":
                self._render_paragraph(block.text)
            elif block.kind == "list":
                self._render_list(block.items or [], block.ordered)
            elif block.kind == "quote":
                self._render_quote(block.text)
            elif block.kind == "code":
                self._render_code(block.text)
            elif block.kind == "hr":
                self._render_hr()
            elif block.kind == "image":
                self._render_image(block.src, block.alt)

        if signature_text:
            self._render_signature(signature_text)

        self._finish_current_page()
        return self.cards


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert markdown into Xiaohongshu cards.")
    parser.add_argument("markdown", help="Path to source markdown file.")
    parser.add_argument("--output-dir", help="Output directory. Default: <md-stem>-xhs-cards next to source file.")
    parser.add_argument("--width", type=int, default=1080, help="Card width in pixels. Default: 1080.")
    parser.add_argument("--height", type=int, default=1440, help="Card height in pixels. Default: 1440.")
    parser.add_argument("--margin", type=int, default=84, help="Page margin in pixels. Default: 84.")
    parser.add_argument("--block-gap", type=int, default=42, help="Vertical gap between blocks.")
    parser.add_argument("--line-height-scale", type=float, default=1.80, help="Line-height multiplier.")
    parser.add_argument("--image-max-ratio", type=float, default=0.36, help="Max image height ratio per card.")
    parser.add_argument("--background", default="#f7f6f2", help="Background color.")
    parser.add_argument("--text-color", default="#141414", help="Body text color.")
    parser.add_argument("--muted-color", default="#767676", help="Muted text / divider color.")
    parser.add_argument("--accent-color", default="#222222", help="Code text color.")
    parser.add_argument("--image-border", default="#d9d9d9", help="Image border color.")
    parser.add_argument("--quote-bg", default="#f0ede6", help="Quote callout background.")
    parser.add_argument("--quote-border", default="#ded9cd", help="Quote callout border.")
    parser.add_argument("--quote-accent", default="#6e6e6e", help="Quote accent bar color.")
    parser.add_argument("--font-serif", help="Preferred serif font path.")
    parser.add_argument("--font-sans", help="Preferred sans font path.")
    parser.add_argument("--font-mono", help="Preferred mono font path.")
    parser.add_argument(
        "--cover-mode",
        choices=["auto", "off", "force"],
        default="auto",
        help="Cover generation strategy. Default: auto.",
    )
    parser.add_argument("--cover-image", help="Explicit cover image path.")
    parser.add_argument("--title", help="Cover title override.")
    parser.add_argument("--subtitle", help="Cover subtitle override.")
    parser.add_argument("--author", help="Cover author name; rendered as 作者：<name>.")
    parser.add_argument("--cover-author", action="store_true", help="Render author on cover (disabled by default).")
    parser.add_argument("--signature-text", default="", help="Signature shown on the last page (e.g. '-- 鹿不角').")
    return parser.parse_args()


def validate_color(name: str, value: str) -> str:
    try:
        ImageColor.getrgb(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid color for {name}: {value}") from exc
    return value


def main() -> int:
    args = parse_args()
    markdown_path = Path(args.markdown).expanduser().resolve()
    if not markdown_path.exists():
        print(f"Markdown file not found: {markdown_path}")
        return 1

    source_dir = markdown_path.parent
    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else source_dir / f"{markdown_path.stem}-xhs-cards"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    content = markdown_path.read_text(encoding="utf-8")
    blocks = parse_markdown(content)
    if not blocks:
        print(f"No renderable content found in: {markdown_path}")
        return 1

    cover, blocks = prepare_cover(
        blocks=blocks,
        markdown_path=markdown_path,
        mode=args.cover_mode,
        title_override=args.title,
        subtitle_override=args.subtitle,
        author_override=args.author,
        image_override=args.cover_image,
    )

    config = RenderConfig(
        width=args.width,
        height=args.height,
        margin=args.margin,
        background=validate_color("background", args.background),
        text_color=validate_color("text-color", args.text_color),
        muted_color=validate_color("muted-color", args.muted_color),
        accent_color=validate_color("accent-color", args.accent_color),
        image_border=validate_color("image-border", args.image_border),
        quote_bg=validate_color("quote-bg", args.quote_bg),
        quote_border=validate_color("quote-border", args.quote_border),
        quote_accent=validate_color("quote-accent", args.quote_accent),
        line_height_scale=args.line_height_scale,
        block_gap=args.block_gap,
        image_max_ratio=args.image_max_ratio,
        output_dir=output_dir,
        source_dir=source_dir,
        font_serif_path=args.font_serif,
        font_sans_path=args.font_sans,
        font_mono_path=args.font_mono,
    )
    signature_text = args.signature_text.strip()
    if not signature_text and args.author:
        signature_text = f"-- {args.author.strip()}"

    renderer = MarkdownCardRenderer(config)
    cards = renderer.render(
        blocks,
        cover=cover,
        signature_text=signature_text,
        cover_author=args.cover_author,
    )

    manifest = {
        "source_markdown": str(markdown_path),
        "output_dir": str(output_dir),
        "card_size": {"width": args.width, "height": args.height},
        "count": len(cards),
        "cards": [path.name for path in cards],
        "missing_images": renderer.missing_images,
        "cover": {
            "enabled": bool(cover),
            "title": cover.title if cover else "",
            "subtitle": cover.subtitle if cover else "",
            "author": cover.author if cover and args.cover_author else "",
            "image_src": cover.image_src if cover else "",
        },
        "signature_text": signature_text,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Rendered {len(cards)} card(s) to: {output_dir}")
    for card in cards:
        print(f"- {card}")
    if renderer.missing_images:
        print(f"- missing images: {len(renderer.missing_images)}")
        for src in renderer.missing_images:
            print(f"  * {src}")
    print(f"- {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
