# 📎 pdf-merger-cli

Simple CLI tool to merge PDF files in a single one. Support merge of entire directories and custom order.

## 📦 Installation

```bash
pip install pdf-merger-cli
```

## 🛠️ How to use

```bash
pdfmerge file1.pdf file2.pdf -o output.pdf
```

Even entire directories:

```bash
pdf-merge ./documenti/ -o merged.pdf
```

With manual ordering:

```bash
pdf-merge 3.pdf 1.pdf 2.pdf -o merged.pdf --ordered
```

## 🐍 Requirements

* Python ≥ 3.7