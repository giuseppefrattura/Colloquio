#!/usr/bin/env python3
"""Genera le edizioni Markdown e testo dai capitoli e dalla prefazione."""
from pathlib import Path
import re


def load_chapters(repo_root):
    chapters = []
    for directory in sorted(repo_root.iterdir()):
        if not directory.is_dir() or not re.match(r"^\d{2}\.", directory.name):
            continue
        sources = sorted(directory.glob("*.md"))
        if not sources:
            raise ValueError(f"Nessun capitolo Markdown in {directory.name}")
        main_source = directory / (directory.name[3:].strip() + ".md")
        if main_source not in sources:
            if len(sources) != 1:
                raise ValueError(
                    f"Capitolo principale ambiguo in {directory.name}: "
                    f"creare {main_source.name} per identificare il capitolo principale"
                )
            main_source = sources[0]
        ordered_sources = [main_source] + [source for source in sources if source != main_source]
        sections = []
        title = None
        for source in ordered_sources:
            content = source.read_text(encoding="utf-8").strip()
            lines = content.splitlines()
            if not lines or not lines[0].startswith("# "):
                raise ValueError(f"Titolo principale mancante in {source}")
            if source == main_source:
                title = lines[0][2:]
                sections.append(content)
            else:
                sections.append(lower_headings(content))
        chapters.append((directory.name[:2], title, "\n\n".join(sections)))
    if not chapters:
        raise ValueError("Nessun capitolo trovato")
    return chapters


def lower_headings(content):
    """Inserisce i capitoli sotto il titolo del libro, preservando il codice."""
    lines = []
    fence = None
    for line in content.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            if re.fullmatch(r"\s*" + re.escape(fence) + r"\s*", line):
                fence = None
        elif marker:
            fence = marker.group(1)
        elif re.match(r"^#{1,5} ", line):
            line = "#" + line
        lines.append(line)
    return "\n".join(lines)


def plain_text(markdown):
    """Rimuove la sintassi editoriale, lasciando intatti esempi e diagrammi."""
    lines = []
    fence = None
    for line in markdown.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if fence:
            if re.fullmatch(r"\s*" + re.escape(fence) + r"\s*", line):
                fence = None
            else:
                lines.append(line)
            continue
        if marker:
            fence = marker.group(1)
            continue
        if re.fullmatch(r'<a id="[^"]+"></a>', line):
            continue
        line = re.sub(r"^#{1,6}\s+", "", line)
        line = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            lambda match: (
                f"{match.group(1)} ({match.group(2)})"
                if match.group(2).startswith(("https://", "http://"))
                else match.group(1)
            ),
            line,
        )
        line = line.replace("**", "").replace("`", "")
        line = re.sub(r"(?<!\w)\*([^*\n]+)\*(?!\w)", r"\1", line)
        lines.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"


def merge_chapters():
    repo_root = Path(__file__).resolve().parent.parent
    chapters = load_chapters(repo_root)
    preface = (repo_root / "PREFAZIONE.md").read_text(encoding="utf-8").strip()
    sections = [
        "# Guida al colloquio per Java Backend Developer",
        preface,
        f"## Indice\n\nL'edizione comprende {len(chapters)} capitoli.\n\n"
        + "\n".join(f"- [{title}](#capitolo-{number})" for number, title, _ in chapters),
    ]
    for number, _, content in chapters:
        sections.append(f'<a id="capitolo-{number}"></a>\n\n{lower_headings(content)}')
    markdown = "\n\n".join(sections) + "\n"
    outputs = {
        "guida-colloquio-completa.md": markdown,
        "guida-colloquio-completa.txt": plain_text(markdown),
    }
    for name, content in outputs.items():
        path = repo_root / name
        path.write_text(content, encoding="utf-8")
        print(f"Generato {name}: {len(chapters)} capitoli, {path.stat().st_size} byte")


if __name__ == "__main__":
    merge_chapters()
