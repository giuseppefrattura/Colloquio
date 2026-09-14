#!/usr/bin/env python3
import os
import re
from datetime import datetime, timezone

def merge_chapters():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_txt = os.path.join(repo_root, "guida-colloquio-completa.txt")
    output_md = os.path.join(repo_root, "guida-colloquio-completa.md")

    # Trova tutte le cartelle che iniziano con due cifre numeriche (es. 01., 02., ..., 35.)
    dirs = [d for d in os.listdir(repo_root) if os.path.isdir(os.path.join(repo_root, d)) and re.match(r"^\d{2}\.", d)]
    dirs.sort()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    header = f"""================================================================================
GUIDA DI STUDIO COMPLETA — COLLOQUIO SENIOR JAVA BACKEND DEVELOPER
Generato automaticamente il: {now}
Totale capitoli inclusi: {len(dirs)}
================================================================================

INDICE DEI CAPITOLI:
"""
    for d in dirs:
        header += f"  - {d}\n"
    header += "\n" + "=" * 80 + "\n\n"

    merged_content = [header]

    for d in dirs:
        dir_path = os.path.join(repo_root, d)
        md_files = [f for f in os.listdir(dir_path) if f.endswith(".md")]
        if not md_files:
            continue
        
        # Prende il file principale markdown nella cartella
        md_file = sorted(md_files)[0]
        file_path = os.path.join(dir_path, md_file)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        chapter_separator = f"\n\n{'#' * 80}\n### CAPITOLO: {d}\n{'#' * 80}\n\n"
        merged_content.append(chapter_separator)
        merged_content.append(content)
        merged_content.append("\n\n")

    final_text = "".join(merged_content)

    # Scrive sia il file .txt che il file .md
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(final_text)

    with open(output_md, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"Unione completata con successo!")
    print(f"File TXT generato: {output_txt} ({os.path.getsize(output_txt)} bytes)")
    print(f"File MD generato:  {output_md} ({os.path.getsize(output_md)} bytes)")

if __name__ == "__main__":
    merge_chapters()
