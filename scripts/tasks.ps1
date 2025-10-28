<#
Simple PowerShell helper tasks for the flask-docker project.
Usage examples:
  .\scripts\tasks.ps1 -Task build
  .\scripts\tasks.ps1 -Task up
  .\scripts\tasks.ps1 -Task down
  .\scripts\tasks.ps1 -Task test-unit
  .\scripts\tasks.ps1 -Task test-integration
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("build","up","down","logs","test-unit","test-integration","initdb","run-all")]
    [string]$Task
)

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
Set-Location $ProjectRoot

function Build-Images {
    docker-compose build --no-cache
}

function Up-Detached {
    docker-compose up --build -d
}

function Down-All {
    docker-compose down
}

function Show-Logs {
    docker-compose logs -f
}

function Run-UnitTests {
    $venvPython = Join-Path $ProjectRoot "app\.venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Host "Virtualenv not found. Creating at app/.venv and installing requirements..."
        python -m venv "$ProjectRoot\app\.venv"
        & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pip install --upgrade pip
        & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pip install -r "$ProjectRoot\app\requirements.txt"
    }
    & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pytest -q app/tests/test_app.py
}

function Run-IntegrationTest {
    Up-Detached
    Start-Sleep -Seconds 8
    $venvPython = Join-Path $ProjectRoot "app\.venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Host "Virtualenv not found. Creating at app/.venv and installing requirements..."
        python -m venv "$ProjectRoot\app\.venv"
        & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pip install --upgrade pip
        & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pip install -r "$ProjectRoot\app\requirements.txt"
    }
    & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pytest -q app/tests/test_integration.py
    Down-All
}

function Run-All {
    # Start the stack with an explicit compose file and project name, wait for /health, run integration test, then tear down.
    $composeFile = Join-Path $ProjectRoot "docker-compose.yml"
    Write-Host "Starting Compose stack (project: flaskfinal)..."
    docker compose -f "$composeFile" -p flaskfinal up --build -d

    # Wait up to 60s for /health to report status=ok
    $end = (Get-Date).AddSeconds(60)
    $ready = $false
    while ((Get-Date) -lt $end -and -not $ready) {
        try {
            $r = Invoke-RestMethod -Uri http://localhost:5000/health -TimeoutSec 3
            if ($r.status -eq 'ok') { $ready = $true; break }
        } catch {
            # ignore and retry
        }
        Start-Sleep -Seconds 1
    }

    if (-not $ready) {
        Write-Host "Service did not become ready within 60s. Showing logs..."
        docker compose -f "$composeFile" -p flaskfinal logs --no-color --tail 200
        docker compose -f "$composeFile" -p flaskfinal down
        exit 2
    }

    # Ensure venv and run the same integration pytest
    $venvPython = Join-Path $ProjectRoot "app\.venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Host "Virtualenv not found. Creating at app/.venv and installing requirements..."
        python -m venv "$ProjectRoot\app\.venv"
        & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pip install --upgrade pip
        & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pip install -r "$ProjectRoot\app\requirements.txt"
    }
    & "$ProjectRoot\app\.venv\Scripts\python.exe" -m pytest -q app/tests/test_integration.py

    docker compose -f "$composeFile" -p flaskfinal logs --no-color --tail 200
    docker compose -f "$composeFile" -p flaskfinal down
}

function Run-InitDb {
    docker-compose run --rm initdb
}

switch ($Task) {
    "build" { Build-Images }
    "up" { Up-Detached }
    "down" { Down-All }
    "logs" { Show-Logs }
    "test-unit" { Run-UnitTests }
    "test-integration" { Run-IntegrationTest }
    "initdb" { Run-InitDb }
}
