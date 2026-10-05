#!/usr/bin/env python3
"""Gerador de apresentações (highlights) em PDF de altíssima definição.

Renderiza cada slide em HTML5/CSS3 moderno (dark mode corporativo,
tipografia Inter/JetBrains Mono, zero quebra ou truncamento de texto)
via Google Chrome headless em 1920x1080 e compila o deck completo em PDF
com qualidade profissional para LinkedIn, documentação e apresentações.

O PDF é vetorial (texto selecionável e fontes embutidas): cada slide sai do
Chrome com --print-to-pdf e as páginas são unidas com `pdfunite` (poppler,
`brew install poppler`). Sem o pdfunite, o script gera um PDF rasterizado.
"""

from __future__ import annotations

import argparse
import html as html_lib
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DEFAULT_INPUTS = [
    ROOT / "0005_prompt_engineering_avancado" / "highlight" / "highlight.md",
    ROOT / "0006_llm_evals_regressao" / "highlight" / "highlight.md",
    ROOT / "0007_agentes_tool_calling" / "highlight" / "highlight.md",
    ROOT / "0008_llms_locais_ollama" / "highlight" / "highlight.md",
    ROOT / "0009_saida_estruturada" / "highlight" / "highlight.md",
    ROOT / "0010_mcp_local" / "highlight" / "highlight.md",
]


@dataclass
class Theme:
    accent: str
    accent_glow: str
    badge_bg: str
    badge_border: str
    badge_text: str
    callout_border: str


THEMES = {
    "0005_prompt_engineering_avancado": Theme(
        accent="#3b82f6",
        accent_glow="rgba(59, 130, 246, 0.25)",
        badge_bg="rgba(37, 99, 235, 0.18)",
        badge_border="rgba(59, 130, 246, 0.45)",
        badge_text="#60a5fa",
        callout_border="#3b82f6",
    ),
    "0006_llm_evals_regressao": Theme(
        accent="#10b981",
        accent_glow="rgba(16, 185, 129, 0.25)",
        badge_bg="rgba(16, 185, 129, 0.18)",
        badge_border="rgba(16, 185, 129, 0.45)",
        badge_text="#34d399",
        callout_border="#10b981",
    ),
    "0007_agentes_tool_calling": Theme(
        accent="#8b5cf6",
        accent_glow="rgba(139, 92, 246, 0.25)",
        badge_bg="rgba(139, 92, 246, 0.18)",
        badge_border="rgba(139, 92, 246, 0.45)",
        badge_text="#a78bfa",
        callout_border="#8b5cf6",
    ),
    "0008_llms_locais_ollama": Theme(
        accent="#f59e0b",
        accent_glow="rgba(245, 158, 11, 0.25)",
        badge_bg="rgba(245, 158, 11, 0.18)",
        badge_border="rgba(245, 158, 11, 0.45)",
        badge_text="#fbbf24",
        callout_border="#f59e0b",
    ),
    "0009_saida_estruturada": Theme(
        accent="#06b6d4",
        accent_glow="rgba(6, 182, 212, 0.25)",
        badge_bg="rgba(6, 182, 212, 0.18)",
        badge_border="rgba(6, 182, 212, 0.45)",
        badge_text="#22d3ee",
        callout_border="#06b6d4",
    ),
    "0010_mcp_local": Theme(
        accent="#f43f5e",
        accent_glow="rgba(244, 63, 94, 0.25)",
        badge_bg="rgba(244, 63, 94, 0.18)",
        badge_border="rgba(244, 63, 94, 0.45)",
        badge_text="#fb7185",
        callout_border="#f43f5e",
    ),
}


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


DIRECTIVE_RE = re.compile(r"^\[(?P<key>[\w-]+):\s*(?P<value>.*)\]$")


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


def format_text(text: str) -> str:
    escaped = html_lib.escape(text)
    # Sub backticks with styled code tags
    return re.sub(
        r"`([^`]+)`",
        r'<code style="font-family:\'JetBrains Mono\', monospace; font-size: 16px; background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(255, 255, 255, 0.14); padding: 2px 8px; border-radius: 6px; color: #38bdf8; font-weight: 500;">\1</code>',
        escaped,
    )


# Flags comuns: esperam layout, fontes e compositor antes de capturar, evitando
# slides com blocos brancos ou fonte de fallback.
CHROME_STABLE_FLAGS = [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=5000",
]


def _run_chrome(html_content: str, output: Path, output_flags: list[str]) -> None:
    temp_html = output.parent / f"_temp_slide_{output.stem}.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()  # nunca aceitar um arquivo antigo como resultado
    temp_html.write_text(html_content, encoding="utf-8")
    cmd = [CHROME_PATH, *CHROME_STABLE_FLAGS, *output_flags, str(temp_html)]
    try:
        subprocess.run(cmd, capture_output=True, timeout=60)
        if not output.exists() or output.stat().st_size < 1000:
            raise RuntimeError(f"Falha ao gerar slide {output}")
    finally:
        if temp_html.exists():
            temp_html.unlink()


def render_html_to_png(html_content: str, output_png: Path) -> None:
    _run_chrome(html_content, output_png, [f"--screenshot={output_png}", "--window-size=1920,1080"])


def render_html_to_pdf(html_content: str, output_pdf: Path) -> None:
    """Uma página PDF vetorial (texto selecionável) de 1920x1080 px."""
    _run_chrome(html_content, output_pdf, [f"--print-to-pdf={output_pdf}", "--no-pdf-header-footer"])


def build_slide_html(slide: Slide, module_name: str, total_slides: int, highlight_dir: Path) -> str:
    theme = THEMES.get(
        module_name,
        Theme(
            accent="#3b82f6",
            accent_glow="rgba(59, 130, 246, 0.25)",
            badge_bg="rgba(37, 99, 235, 0.18)",
            badge_border="rgba(59, 130, 246, 0.45)",
            badge_text="#60a5fa",
            callout_border="#3b82f6",
        ),
    )

    # Render body elements
    body_html_parts: list[str] = []
    for kind, payload in slide.elements:
        if kind == "paragraph":
            text = format_text(str(payload))
            body_html_parts.append(
                f'<p style="font-size: 20px; line-height: 1.6; color: #94a3b8;">{text}</p>'
            )
        elif kind == "callouts":
            lines = payload if isinstance(payload, list) else [str(payload)]
            formatted_lines = "<br>".join(format_text(l) for l in lines)
            body_html_parts.append(
                f"""<div style="background: rgba(15, 23, 42, 0.75); border-left: 4px solid {theme.callout_border}; padding: 18px 24px; border-radius: 0 12px 12px 0; font-size: 19px; line-height: 1.55; color: #f8fafc; font-weight: 500; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);">
                    {formatted_lines}
                </div>"""
            )
        elif kind == "bullets":
            bullets = payload if isinstance(payload, list) else [str(payload)]
            items_html = "".join(
                f'<li style="display: flex; gap: 12px; align-items: flex-start; margin-bottom: 12px; font-size: 19px; color: #cbd5e1; line-height: 1.5;"><span style="color: {theme.accent}; font-weight: 800; font-size: 22px; line-height: 1;">•</span><span>{format_text(b)}</span></li>'
                for b in bullets
            )
            body_html_parts.append(f'<ul style="list-style: none; padding: 0; margin: 4px 0;">{items_html}</ul>')

    body_html = "\n".join(body_html_parts)

    # Resolve image path if present
    img_tag = ""
    if slide.image:
        resolved_img = (highlight_dir / slide.image).resolve()
        if resolved_img.exists():
            img_tag = f'<img src="{resolved_img}" style="width: 100%; height: auto; max-height: 640px; object-fit: contain; border-radius: 12px; display: block;" />'

    # Build content depending on layout
    if slide.layout == "cta":
        # Gallery of 3 cards
        gallery_cards: list[str] = []
        for g_img in slide.gallery[:3]:
            g_path = (highlight_dir / g_img).resolve()
            if g_path.exists():
                gallery_cards.append(
                    f"""<div style="flex: 1; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 14px; padding: 10px; box-shadow: 0 16px 32px rgba(0,0,0,0.5);">
                        <img src="{g_path}" style="width: 100%; height: 260px; object-fit: cover; border-radius: 8px; display: block;" />
                    </div>"""
                )
        gallery_html = "".join(gallery_cards)

        main_content = f"""
        <div style="display: flex; flex-direction: column; flex: 1; justify-content: space-between; padding: 56px 80px 32px 80px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 48px;">
                <div style="flex: 1; display: flex; flex-direction: column; gap: 20px;">
                    <div style="align-self: flex-start; padding: 6px 16px; background: {theme.badge_bg}; border: 1px solid {theme.badge_border}; border-radius: 999px; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: {theme.badge_text};">
                        {slide.eyebrow}
                    </div>
                    <div style="font-size: 44px; font-weight: 800; line-height: 1.15; color: #ffffff; letter-spacing: -0.02em;">
                        {slide.title}
                    </div>
                    <div style="width: 64px; height: 3px; background: linear-gradient(90deg, {theme.accent}, transparent); border-radius: 2px;"></div>
                    <div style="display: flex; flex-direction: column; gap: 14px; max-width: 900px;">
                        {body_html}
                    </div>
                </div>
                <div style="flex: 0 0 380px; display: flex; flex-direction: column; justify-content: center; gap: 18px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 32px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
                    <div style="font-size: 15px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Repositório Oficial</div>
                    <div style="font-size: 22px; font-weight: 700; color: #ffffff;">github.com/pathbit/pathbit-academy-ai</div>
                    <div style="font-size: 14px; color: #64748b; line-height: 1.5;">Código 100% aberto, sem chave de API e pronto para execução local.</div>
                    <div style="padding: 12px 20px; background: {theme.accent}; border-radius: 10px; color: #ffffff; font-weight: 700; font-size: 15px; text-align: center; box-shadow: 0 8px 20px {theme.accent_glow};">
                        Acessar Laboratório Completo ➔
                    </div>
                </div>
            </div>

            <!-- Gallery row -->
            <div style="display: flex; gap: 24px; width: 100%; margin-top: 24px;">
                {gallery_html}
            </div>
        </div>
        """

    elif slide.layout == "cover":
        main_content = f"""
        <div style="display: flex; flex: 1; padding: 64px 80px 32px 80px; gap: 60px; align-items: center;">
            <div style="flex: 0 0 820px; display: flex; flex-direction: column; gap: 26px;">
                <div style="align-self: flex-start; padding: 6px 18px; background: {theme.badge_bg}; border: 1px solid {theme.badge_border}; border-radius: 999px; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: {theme.badge_text};">
                    {slide.eyebrow}
                </div>
                <div style="font-size: 52px; font-weight: 900; line-height: 1.12; color: #ffffff; letter-spacing: -0.025em;">
                    {slide.title}
                </div>
                <div style="width: 80px; height: 4px; background: linear-gradient(90deg, {theme.accent}, transparent); border-radius: 2px;"></div>
                <div style="display: flex; flex-direction: column; gap: 16px;">
                    {body_html}
                </div>
                <div style="align-self: flex-start; margin-top: 12px; display: inline-flex; align-items: center; gap: 10px; padding: 10px 20px; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; font-size: 15px; font-weight: 600; color: #cbd5e1;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: {theme.accent};"></span>
                    Leitura completa no artigo + notebook + CSVs no repositório
                </div>
            </div>
            <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="width: 100%; background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 16px; box-shadow: 0 24px 48px -12px rgba(0, 0, 0, 0.6); display: flex; flex-direction: column; align-items: center;">
                    {img_tag}
                    <div style="margin-top: 14px; font-size: 14px; color: #64748b; text-align: center;">{slide.caption}</div>
                </div>
            </div>
        </div>
        """

    else:  # split layout
        main_content = f"""
        <div style="display: flex; flex: 1; padding: 64px 80px 32px 80px; gap: 60px; align-items: center;">
            <div style="flex: 0 0 760px; display: flex; flex-direction: column; justify-content: center; gap: 24px;">
                <div style="align-self: flex-start; padding: 6px 16px; background: {theme.badge_bg}; border: 1px solid {theme.badge_border}; border-radius: 999px; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: {theme.badge_text};">
                    {slide.eyebrow}
                </div>
                <div style="font-size: 42px; font-weight: 800; line-height: 1.15; color: #ffffff; letter-spacing: -0.02em;">
                    {slide.title}
                </div>
                <div style="width: 64px; height: 3px; background: linear-gradient(90deg, {theme.accent}, transparent); border-radius: 2px;"></div>
                <div style="display: flex; flex-direction: column; gap: 18px;">
                    {body_html}
                </div>
            </div>
            <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="width: 100%; background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 16px; box-shadow: 0 24px 48px -12px rgba(0, 0, 0, 0.6); display: flex; flex-direction: column; align-items: center;">
                    {img_tag}
                    <div style="margin-top: 14px; font-size: 15px; color: #64748b; text-align: center;">{slide.caption}</div>
                </div>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
@page {{ size: 1920px 1080px; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{
    width: 1920px;
    height: 1080px;
    overflow: hidden;
    background: #070a13;
    background-image: 
        radial-gradient(circle at 12% 15%, {theme.accent_glow} 0%, transparent 45%),
        radial-gradient(circle at 88% 85%, rgba(16, 185, 129, 0.08) 0%, transparent 45%);
    font-family: 'Inter', -apple-system, sans-serif;
    color: #f1f5f9;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.footer {{
    height: 64px;
    padding: 0 80px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    color: #64748b;
    background: rgba(7, 10, 19, 0.85);
}}
</style>
</head>
<body>
    {main_content}
    <div class="footer">
        <div><strong>{slide.index} / {total_slides}</strong></div>
        <div>github.com/pathbit/pathbit-academy-ai</div>
        <div><strong>{module_name}</strong></div>
    </div>
</body>
</html>"""


def render_file(input_path: Path) -> Path:
    module_name = input_path.parents[1].name
    number = module_name.split("_", 1)[0]
    output_pdf = input_path.parent / f"highlights_{number}.pdf"
    slides = parse_highlight(input_path)
    highlight_dir = input_path.parent

    print(f"\nRenderizando deck {module_name} ({len(slides)} slides)...")
    # Preferência: PDF vetorial (texto selecionável) unido com pdfunite (poppler).
    # Sem pdfunite, cai para o deck rasterizado a partir de PNGs.
    vector = shutil.which("pdfunite") is not None
    temp_files: list[Path] = []
    try:
        for slide in slides:
            html_content = build_slide_html(slide, module_name, len(slides), highlight_dir)
            if vector:
                temp = highlight_dir / f"_deck_slide_{slide.index}.pdf"
                render_html_to_pdf(html_content, temp)
            else:
                temp = highlight_dir / f"_deck_slide_{slide.index}.png"
                render_html_to_png(html_content, temp)
            temp_files.append(temp)
            print(f"  ✓ Slide {slide.index}/{len(slides)} renderizado")

        if output_pdf.exists():
            output_pdf.unlink()
        if vector:
            subprocess.run(["pdfunite", *map(str, temp_files), str(output_pdf)], check=True)
        else:
            images = [Image.open(p).convert("RGB") for p in temp_files]
            images[0].save(
                output_pdf,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=images[1:],
            )
        kind = "vetorial" if vector else "rasterizado"
        print(f"✓ PDF {kind} gerado: {output_pdf.relative_to(ROOT)} ({output_pdf.stat().st_size // 1024} KB)")
    finally:
        for p in temp_files:
            if p.exists():
                p.unlink()

    return output_pdf


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="*", help="highlight.md files to render")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    inputs = [Path(item).resolve() for item in args.inputs] if args.inputs else DEFAULT_INPUTS
    for input_path in inputs:
        render_file(input_path)


if __name__ == "__main__":
    main()
