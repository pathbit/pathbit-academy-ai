from __future__ import annotations

import argparse
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from PIL import Image, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUTS = [
    ROOT / "0005_prompt_engineering_avancado" / "highlight" / "highlight.md",
    ROOT / "0006_llm_evals_regressao" / "highlight" / "highlight.md",
    ROOT / "0007_agentes_tool_calling" / "highlight" / "highlight.md",
]

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["ps.fonttype"] = 42


@dataclass
class Palette:
    background: str
    background_alt: str
    accent: str
    accent_soft: str
    text: str
    muted: str
    line: str
    panel: str
    chip_text: str
    callout: str


@dataclass
class Slide:
    index: int
    layout: str = "split"
    eyebrow: str = ""
    image: str | None = None
    gallery: list[str] = field(default_factory=list)
    caption: str = ""
    title: str = ""
    elements: list[tuple[str, list[str] | str]] = field(default_factory=list)


PALETTES = {
    "0005_prompt_engineering_avancado": Palette(
        background="#ffffff",
        background_alt="#f6f9ff",
        accent="#156ff7",
        accent_soft="#eaf2ff",
        text="#102030",
        muted="#66758a",
        line="#d7e2f0",
        panel="#fdfefe",
        chip_text="#156ff7",
        callout="#f4f8ff",
    ),
    "0006_llm_evals_regressao": Palette(
        background="#ffffff",
        background_alt="#f4fcf8",
        accent="#0e9b74",
        accent_soft="#e8f8f1",
        text="#13231f",
        muted="#678078",
        line="#d5e9e0",
        panel="#fcfffe",
        chip_text="#0e9b74",
        callout="#f1fbf7",
    ),
    "0007_agentes_tool_calling": Palette(
        background="#ffffff",
        background_alt="#f4f9ff",
        accent="#1690e8",
        accent_soft="#eaf5ff",
        text="#102033",
        muted="#6a7f97",
        line="#d7e6f4",
        panel="#fbfdff",
        chip_text="#1690e8",
        callout="#f2f8ff",
    ),
}


DIRECTIVE_RE = re.compile(r"^\[(?P<key>[\w-]+):\s*(?P<value>.*)\]$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="*", help="highlight.md files to render")
    return parser.parse_args()


def split_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line.startswith("**Slide "):
            if current:
                blocks.append(current)
            current = []
            continue
        current.append(line.rstrip("\n"))
    if current:
        blocks.append(current)
    return blocks


def parse_elements(lines: list[str]) -> list[tuple[str, list[str] | str]]:
    elements: list[tuple[str, list[str] | str]] = []
    chunk: list[str] = []

    def flush() -> None:
        nonlocal chunk
        cleaned = [line.strip() for line in chunk if line.strip()]
        chunk = []
        if not cleaned:
            return
        if all(line.startswith("- ") for line in cleaned):
            elements.append(("bullets", [line[2:].strip() for line in cleaned]))
            return
        if all(line.startswith("> ") for line in cleaned):
            elements.append(("callouts", [line[2:].strip() for line in cleaned]))
            return
        text = " ".join(line.lstrip("> ").strip() for line in cleaned)
        elements.append(("paragraph", text))

    for raw in lines:
        if not raw.strip():
            flush()
            continue
        chunk.append(raw)
    flush()
    return elements


def parse_highlight(path: Path) -> list[Slide]:
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    slides: list[Slide] = []
    for index, block in enumerate(split_blocks(raw_lines), start=1):
        directives: dict[str, str] = {}
        content: list[str] = []
        for line in block:
            stripped = line.strip()
            if not stripped:
                content.append("")
                continue
            match = DIRECTIVE_RE.match(stripped)
            if match:
                directives[match.group("key")] = match.group("value")
            else:
                content.append(line.rstrip())
        while content and not content[0].strip():
            content.pop(0)
        while content and not content[-1].strip():
            content.pop()
        title = content[0].strip() if content else ""
        body_lines = content[1:] if len(content) > 1 else []
        gallery = [
            item.strip()
            for item in directives.get("gallery", "").split(",")
            if item.strip()
        ]
        slides.append(
            Slide(
                index=index,
                layout=directives.get("layout", "split"),
                eyebrow=directives.get("eyebrow", ""),
                image=directives.get("image"),
                gallery=gallery,
                caption=directives.get("caption", ""),
                title=title,
                elements=parse_elements(body_lines),
            )
        )
    return slides


def wrap(text: str, width: int) -> str:
    return "\n".join(
        textwrap.wrap(
            text,
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


def prepare_image(path: Path, size: tuple[int, int], mode: str) -> np.ndarray:
    image = Image.open(path).convert("RGBA")
    if mode == "cover":
        image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
    else:
        canvas = Image.new("RGBA", size, (255, 255, 255, 0))
        contained = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
        x = (size[0] - contained.width) // 2
        y = (size[1] - contained.height) // 2
        canvas.alpha_composite(contained, (x, y))
        image = canvas
    return np.asarray(image)


def prepare_cover(path: Path, size: tuple[int, int]) -> np.ndarray:
    image = Image.open(path).convert("RGBA")
    image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
    image = image.filter(ImageFilter.GaussianBlur(radius=0.8))
    return np.asarray(image)


def add_background(fig: plt.Figure, palette: Palette) -> plt.Axes:
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, fc=palette.background, ec="none"))
    ax.add_patch(Circle((0.92, 0.88), 0.18, fc=palette.accent_soft, ec="none", alpha=0.95))
    ax.add_patch(Circle((0.12, 0.10), 0.08, fc=palette.background_alt, ec="none", alpha=0.95))
    ax.add_patch(Rectangle((0.0, 0.93), 1.0, 0.07, fc=palette.background_alt, ec="none"))
    return ax


def draw_footer(ax: plt.Axes, module_name: str, page_num: int, total: int, palette: Palette) -> None:
    ax.plot([0.06, 0.94], [0.075, 0.075], color=palette.line, lw=1.0, alpha=0.9)
    ax.text(0.06, 0.045, f"{page_num} / {total}", color=palette.muted, fontsize=9.5, va="center")
    ax.text(0.50, 0.045, "github.com/pathbit/pathbit-academy-ai", color=palette.muted, fontsize=9.5, ha="center", va="center")
    ax.text(0.94, 0.045, module_name, color=palette.muted, fontsize=9.5, ha="right", va="center")


def draw_chip(ax: plt.Axes, text: str, xy: tuple[float, float], palette: Palette, *, fill: str | None = None) -> None:
    if not text:
        return
    x, y = xy
    width = min(0.42, 0.012 * len(text) + 0.05)
    box = FancyBboxPatch(
        (x, y),
        width,
        0.048,
        boxstyle="round,pad=0.008,rounding_size=0.015",
        fc=fill or palette.accent_soft,
        ec="none",
        alpha=0.98,
    )
    ax.add_patch(box)
    ax.text(x + 0.018, y + 0.024, text, color=palette.chip_text, fontsize=11.5, va="center", fontweight="bold")


def draw_image_card(fig: plt.Figure, ax: plt.Axes, image_path: Path, rect: tuple[float, float, float, float], caption: str, palette: Palette) -> None:
    x, y, width, height = rect
    shadow = FancyBboxPatch(
        (x + 0.01, y - 0.01),
        width,
        height,
        boxstyle="round,pad=0.008,rounding_size=0.03",
        fc="#000000",
        ec="none",
        alpha=0.18,
        zorder=2,
    )
    panel = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.008,rounding_size=0.03",
        fc=palette.panel,
        ec=palette.line,
        lw=1.0,
        zorder=3,
    )
    ax.add_patch(shadow)
    ax.add_patch(panel)
    image_ax = fig.add_axes([x + 0.012, y + 0.032, width - 0.024, height - 0.068], zorder=4)
    image_ax.axis("off")
    image_ax.set_facecolor(palette.panel)
    image_ax.imshow(prepare_image(image_path, (1100, 720), "contain"))
    if caption:
        ax.text(x + 0.015, y + 0.016, wrap(caption, 34), color=palette.muted, fontsize=9.5, va="bottom")


def draw_gallery(fig: plt.Figure, ax: plt.Axes, gallery_paths: list[Path], rect: tuple[float, float, float, float], palette: Palette) -> None:
    x, y, width, height = rect
    gap = 0.02
    card_width = (width - gap * (len(gallery_paths) - 1)) / len(gallery_paths)
    for idx, image_path in enumerate(gallery_paths):
        card_x = x + idx * (card_width + gap)
        draw_image_card(fig, ax, image_path, (card_x, y, card_width, height), "", palette)


def draw_text_stack(ax: plt.Axes, slide: Slide, rect: tuple[float, float, float], palette: Palette) -> None:
    x, start_y, width = rect
    if slide.eyebrow:
        draw_chip(ax, slide.eyebrow, (x, start_y), palette)
        start_y -= 0.07
    title_width = max(20, int(width * 47))
    title = wrap(slide.title, title_width)
    ax.text(
        x,
        start_y,
        title,
        color=palette.accent,
        fontsize=30,
        fontweight="bold",
        va="top",
        linespacing=1.08,
    )
    title_lines = max(1, title.count("\n") + 1)
    y = start_y - 0.055 * title_lines - 0.035
    ax.plot([x, x + min(width, 0.38)], [y + 0.012, y + 0.012], color=palette.line, lw=1.0)

    for kind, payload in slide.elements:
        if kind == "paragraph":
            text = wrap(str(payload), max(24, int(width * 54)))
            ax.text(
                x,
                y - 0.012,
                text,
                color=palette.text,
                fontsize=17.2,
                va="top",
                linespacing=1.24,
            )
            line_count = text.count("\n") + 1
            y -= 0.039 * line_count + 0.04
            continue

        if kind == "bullets":
            bullets = payload if isinstance(payload, list) else [str(payload)]
            for bullet in bullets:
                wrapped = textwrap.wrap(
                    bullet,
                    width=max(24, int(width * 50)),
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                for idx, part in enumerate(wrapped):
                    prefix = "• " if idx == 0 else "  "
                    ax.text(
                        x,
                        y,
                        prefix + part,
                        color=palette.text,
                        fontsize=16.2,
                        va="top",
                    )
                    y -= 0.034
                y -= 0.009
            y -= 0.016
            continue

        callouts = payload if isinstance(payload, list) else [str(payload)]
        callout_lines: list[str] = []
        for callout in callouts:
            callout_lines.extend(
                textwrap.wrap(
                    callout,
                    width=max(22, int(width * 50)),
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )
        box_height = 0.048 * len(callout_lines) + 0.036
        box = FancyBboxPatch(
            (x, y - box_height + 0.012),
            width,
            box_height,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            fc=palette.callout,
            ec=palette.line,
            lw=1.0,
        )
        ax.add_patch(box)
        cursor_y = y - 0.016
        for line in callout_lines:
            ax.text(x + 0.02, cursor_y, line, color=palette.text, fontsize=15.8, va="top")
            cursor_y -= 0.038
        y -= box_height + 0.032


def render_cover(fig: plt.Figure, ax: plt.Axes, slide: Slide, module_name: str, palette: Palette, total: int) -> None:
    image_path = (ROOT / module_name / "highlight" / slide.image).resolve() if slide.image else None
    draw_text_stack(ax, slide, (0.075, 0.80, 0.42), palette)
    if image_path and image_path.exists():
        draw_image_card(fig, ax, image_path, (0.54, 0.17, 0.39, 0.65), slide.caption, palette)
        draw_chip(ax, "Leitura completa no artigo + notebook + CSVs", (0.075, 0.145), palette, fill=palette.accent_soft)
    draw_footer(ax, module_name, slide.index, total, palette)


def render_split(fig: plt.Figure, ax: plt.Axes, slide: Slide, module_name: str, palette: Palette, total: int) -> None:
    draw_text_stack(ax, slide, (0.07, 0.83, 0.41), palette)
    if slide.image:
        image_path = (ROOT / module_name / "highlight" / slide.image).resolve()
        if image_path.exists():
            draw_image_card(fig, ax, image_path, (0.55, 0.18, 0.38, 0.62), slide.caption, palette)
    draw_footer(ax, module_name, slide.index, total, palette)


def render_cta(fig: plt.Figure, ax: plt.Axes, slide: Slide, module_name: str, palette: Palette, total: int) -> None:
    draw_text_stack(ax, slide, (0.07, 0.82, 0.46), palette)
    gallery_paths = [
        (ROOT / module_name / "highlight" / image_path).resolve()
        for image_path in slide.gallery
        if image_path
    ]
    gallery_paths = [path for path in gallery_paths if path.exists()]
    if gallery_paths:
        draw_gallery(fig, ax, gallery_paths[:3], (0.56, 0.28, 0.37, 0.46), palette)
    button = FancyBboxPatch(
        (0.56, 0.16),
        0.37,
        0.08,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        fc=palette.accent,
        ec="none",
        alpha=0.98,
    )
    ax.add_patch(button)
    ax.text(0.745, 0.20, "Artigo completo + codigo no repositorio", color="white", fontsize=15, fontweight="bold", ha="center", va="center")
    draw_footer(ax, module_name, slide.index, total, palette)


def output_path_for(input_path: Path) -> Path:
    module_name = input_path.parents[1].name
    number = module_name.split("_", 1)[0]
    return input_path.parent / f"highlights_{number}.pdf"


def render_file(input_path: Path) -> Path:
    module_name = input_path.parents[1].name
    palette = PALETTES[module_name]
    slides = parse_highlight(input_path)
    output_path = output_path_for(input_path)
    with PdfPages(output_path) as pdf:
        for slide in slides:
            fig = plt.figure(figsize=(13.333, 7.5), facecolor=palette.background)
            ax = add_background(fig, palette)
            if slide.layout == "cover":
                render_cover(fig, ax, slide, module_name, palette, len(slides))
            elif slide.layout == "cta":
                render_cta(fig, ax, slide, module_name, palette, len(slides))
            else:
                render_split(fig, ax, slide, module_name, palette, len(slides))
            pdf.savefig(fig, facecolor=fig.get_facecolor())
            plt.close(fig)
    return output_path


def main() -> None:
    args = parse_args()
    inputs = [Path(item).resolve() for item in args.inputs] if args.inputs else DEFAULT_INPUTS
    for input_path in inputs:
        output_path = render_file(input_path)
        print(output_path)


if __name__ == "__main__":
    main()
