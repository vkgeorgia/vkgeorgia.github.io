# Docker Startup Helper
# This script helps start Docker Desktop and wait for the engine

Write-Host "=== Docker Startup Helper ===" -ForegroundColor Cyan
Write-Host ""

# Check if Docker Desktop is running
$dockerProcess = Get-Process "Docker Desktop" -ErrorAction SilentlyContinue

if (-not $dockerProcess) {
    Write-Host "Docker Desktop is not running. Starting..." -ForegroundColor Yellow
    
    # Try to find Docker Desktop executable
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    if (Test-Path $dockerPath) {
        Start-Process $dockerPath
        Write-Host "Docker Desktop started. Waiting for engine..." -ForegroundColor Green
    }
    else {
        Write-Host "Error: Docker Desktop not found at: $dockerPath" -ForegroundColor Red
        Write-Host "Please install Docker Desktop or update the path in this script." -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "Docker Desktop is already running." -ForegroundColor Green
}

# Wait for Docker daemon to be ready
Write-Host ""
Write-Host "Waiting for Docker Engine to start (this may take 30-60 seconds)..." -ForegroundColor Yellow

$maxAttempts = 30
$attempt = 0
$dockerReady = $false

while ($attempt -lt $maxAttempts -and -not $dockerReady) {
    $attempt++
    Write-Host "  Attempt $attempt/$maxAttempts..." -ForegroundColor DarkGray
    
    try {
        docker ps 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $dockerReady = $true
            Write-Host ""
            Write-Host "[OK] Docker Engine is ready!" -ForegroundColor Green
            break
        }
    }
    catch {
        # Ignore errors, keep trying
    }
    
    Start-Sleep -Seconds 2
}

if (-not $dockerReady) {
    Write-Host ""
    Write-Host "[FAIL] Docker Engine did not start in time." -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Open Docker Desktop manually"
    Write-Host "2. Check if there's an error message"
    Write-Host "3. Go to Settings -> General -> Use WSL 2 based engine (should be enabled)"
    Write-Host "4. Click 'Apply & Restart'"
    Write-Host "5. Wait 1-2 minutes and run this script again"
    Write-Host ""
    Write-Host "If problems persist, try:" -ForegroundColor Yellow
    Write-Host "  wsl --shutdown"
    Write-Host "  Then restart Docker Desktop"
    exit 1
}

Write-Host ""
Write-Host "=== Docker is Ready ===" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run: .\deploy.ps1" -ForegroundColor Cyan
Write-Host ""

# Show Docker info
Write-Host "Docker Info:" -ForegroundColor Cyan
docker version --format "  Version: {{.Server.Version}}"
docker info --format "  Containers: {{.ContainersRunning}} running, {{.ContainersStopped}} stopped"
