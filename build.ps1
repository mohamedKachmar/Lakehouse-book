# Compile l'ouvrage en PDF via Docker (aucune installation LaTeX locale requise).
# Usage : .\build.ps1   ->  ouvrage\ouvrage.pdf
$ErrorActionPreference = "Stop"
docker run --rm -v "${PWD}/ouvrage:/work" -w /work texlive/texlive:latest sh -c "pdflatex -interaction=nonstopmode ouvrage && bibtex ouvrage; makeindex ouvrage; pdflatex -interaction=nonstopmode ouvrage && pdflatex -interaction=nonstopmode ouvrage"
if (Test-Path ouvrage\ouvrage.pdf) { Write-Host "OK : ouvrage\ouvrage.pdf" } else { Write-Error "PDF non généré" }
