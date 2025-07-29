import typer
from pathlib import Path
from PyPDF2 import PdfMerger
from typing import List

app = typer.Typer()

@app.command()
def merge(
    input_paths: List[Path] = typer.Argument(..., help="Paths PDF to merge"),
    output_path: Path = typer.Option(..., "--output", "-o", help="Output file"),
    ordered: bool = typer.Option(False, "--ordered", "-r", help="Use input order or alphabetical")
):
    """Merge multiple PDF files into a single PDF file."""
    merger = PdfMerger()
    all_paths = []

    for path in input_paths:
        path = path.resolve()
        if path.is_dir():
            all_paths.extend(sorted(path.glob("*.pdf")))
        elif path.is_file():
            all_paths.append(path)
        else:
            typer.echo(f"❌ Path not found: {path}")
            raise typer.Exit(1)

    if not ordered:
        all_paths = sorted(all_paths, key=lambda p: p.name)

    for path in all_paths:
        merger.append(str(path))

    merger.write(str(output_path))
    merger.close()
    typer.echo(f"✅ Created {output_path}")

if __name__ == "__main__":
    app()
