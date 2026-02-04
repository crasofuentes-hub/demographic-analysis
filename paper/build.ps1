param(
  [ValidateSet("pdf","tex")] [string] $Target = "pdf"
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$md = "paper/manuscript.md"
$meta = "paper/metadata.yaml"

if (!(Get-Command pandoc -ErrorAction SilentlyContinue)) {
  Write-Host "pandoc no está instalado o no está en PATH. Solo se prepararon los archivos. Instala pandoc para compilar." -ForegroundColor Yellow
  exit 0
}

if ($Target -eq "pdf") {
  pandoc $md $meta -o "paper/manuscript.pdf"
  Write-Host "Generado: paper/manuscript.pdf"
} else {
  pandoc $md $meta -s -o "paper/manuscript.tex"
  Write-Host "Generado: paper/manuscript.tex"
}
