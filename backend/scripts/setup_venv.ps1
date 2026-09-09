# PowerShell helper: cria venv e instala requirements
param(
    [string]$venvName = ".venv"
)
python -m venv $venvName
& "$venvName\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Venv '$venvName' criado e dependências instaladas." -ForegroundColor Green
