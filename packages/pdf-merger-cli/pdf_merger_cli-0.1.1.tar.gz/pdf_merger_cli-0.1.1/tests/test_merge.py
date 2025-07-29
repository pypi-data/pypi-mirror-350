from pathlib import Path
from PyPDF2 import PdfReader, PdfMerger
import shutil

def test_merge(tmp_path):
    pdf1 = tmp_path / "a.pdf"
    pdf2 = tmp_path / "b.pdf"
    merged = tmp_path / "merged.pdf"

    merger = PdfMerger()
    merger.append(Path(__file__).parent / "resources/1page.pdf") 
    merger.write(str(pdf1))
    merger.close()

    merger = PdfMerger()
    merger.append(Path(__file__).parent / "resources/1page.pdf")
    merger.write(str(pdf2))
    merger.close()

    merger = PdfMerger()
    merger.append(str(pdf1))
    merger.append(str(pdf2))
    merger.write(str(merged))
    merger.close()

    reader = PdfReader(str(merged))
    assert len(reader.pages) == 2
