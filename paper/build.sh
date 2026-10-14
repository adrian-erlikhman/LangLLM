#!/usr/bin/env bash
# Build paper/main.pdf (pdfLaTeX + BibTeX). Run from anywhere.
set -euo pipefail
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
bibtex main >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex | grep -E "Output written" || true
grep -E "LaTeX Warning|Overfull" main.log || true
