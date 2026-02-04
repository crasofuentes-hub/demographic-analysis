# Build instructions (Pandoc)

## arXiv / generic PDF
pandoc paper/manuscript.md -o paper/manuscript.pdf

## LaTeX (generic)
pandoc paper/manuscript.md -s -o paper/manuscript.tex

## IEEE-like (basic)
pandoc paper/manuscript.md -s --pdf-engine=xelatex -o paper/manuscript_ieee.pdf

## Elsevier-like (basic)
pandoc paper/manuscript.md -s --pdf-engine=xelatex -o paper/manuscript_elsevier.pdf
