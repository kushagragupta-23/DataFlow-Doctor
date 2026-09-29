$ErrorActionPreference = "Stop"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
if (!(Test-Path .env)) { Copy-Item .env.example .env }
Write-Host "Now run: ollama pull qwen3:8b"
Write-Host "Then run: ollama pull nomic-embed-text"
Write-Host "Then run: python ingest.py --reset"
