#!/usr/bin/env python3
"""Генерация всех PlantUML-диаграмм проекта WatchDog-MAS."""

import os
from pathlib import Path

from plantweb.render import render

DIAGRAMS_DIR = Path(__file__).resolve().parent
DIAGRAM_FILES = [
    "01_overall_interaction.puml",
    "02_coordinator_uml.puml",
    "03_auditor_uml.puml",
    "04_analyzator_uml.puml",
    "05_django_sequence.puml",
]


def render_diagram(puml_path: Path, output_format: str = "png") -> Path:
    """Рендерит один .puml файл в изображение."""
    content = puml_path.read_text(encoding="utf-8")
    output_bytes, fmt, engine, sha = render(
        content,
        engine="plantuml",
        format=output_format,
    )
    out_path = puml_path.with_suffix(f".{fmt}")
    out_path.write_bytes(output_bytes)
    return out_path


def main():
    generated = []
    failed = []

    for filename in DIAGRAM_FILES:
        puml_path = DIAGRAMS_DIR / filename
        if not puml_path.exists():
            print(f"  [SKIP] {filename} — файл не найден")
            failed.append(filename)
            continue
        try:
            out = render_diagram(puml_path)
            print(f"  [OK]   {filename} → {out.name}")
            generated.append(out.name)
        except Exception as e:
            print(f"  [FAIL] {filename} — {e}")
            failed.append(filename)

    print(f"\nСгенерировано: {len(generated)}, ошибок: {len(failed)}")
    if failed:
        print(f"Ошибки: {', '.join(failed)}")


if __name__ == "__main__":
    main()
