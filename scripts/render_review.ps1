param([Parameter(Mandatory=$true)][string]$Docx)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$InputFile = Join-Path $Root $Docx
$ReviewDir = Join-Path $Root "output/review"
New-Item -ItemType Directory -Force -Path $ReviewDir | Out-Null
$Soffice = (Get-Command soffice -ErrorAction SilentlyContinue)
if (-not $Soffice) { throw "LibreOffice soffice not found in PATH. Install LibreOffice or use Microsoft Word to export PDF for page inspection." }
& soffice --headless --convert-to pdf --outdir $ReviewDir $InputFile
Write-Host "Check the PDF page by page:" (Join-Path $ReviewDir (([IO.Path]::GetFileNameWithoutExtension($Docx)) + ".pdf"))
