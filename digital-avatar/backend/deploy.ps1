# Deploy script for Google Cloud Run
# Usage: .\deploy.ps1

Write-Host "Deploying AI Avatar to Google Cloud Run..." -ForegroundColor Green

# Check if gcloud is installed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "Error: gcloud CLI not found. Please install Google Cloud SDK." -ForegroundColor Red
    Write-Host "Download from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Check if .env file exists
if (-not (Test-Path "../.env")) {
    Write-Host "Error: .env file not found in parent directory" -ForegroundColor Red
    exit 1
}

# Load environment variables
Get-Content "../.env" | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Variable -Name $name -Value $value -Scope Script
    }
}

# Prompt for project ID if not set
if (-not $env:GCP_PROJECT_ID) {
    $projectId = Read-Host "Enter your Google Cloud Project ID"
} else {
    $projectId = $env:GCP_PROJECT_ID
}

Write-Host "Using project: $projectId" -ForegroundColor Cyan

# Set project
gcloud config set project $projectId

# Deploy
Write-Host "Deploying to Cloud Run..." -ForegroundColor Cyan

# Sync knowledge base into backend/knowledge_base for deployment
$kbSource = Join-Path $PSScriptRoot "..\\knowledge-base"
$kbDest = Join-Path $PSScriptRoot "knowledge_base"
if (Test-Path $kbSource) {
    New-Item -ItemType Directory -Force -Path $kbDest | Out-Null
    Copy-Item -Path (Join-Path $kbSource "*") -Destination $kbDest -Recurse -Force
    Write-Host "Knowledge base synced to backend/knowledge_base" -ForegroundColor Green
} else {
    Write-Host "Warning: knowledge-base folder not found; local KB won't be bundled." -ForegroundColor Yellow
}

gcloud run deploy ai-avatar `
    --source . `
    --platform managed `
    --region us-central1 `
    --allow-unauthenticated `
    --set-env-vars "GEMINI_API_KEY=$GEMINI_API_KEY,GOOGLE_DRIVE_FOLDER_ID=$GOOGLE_DRIVE_FOLDER_ID"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nDeployment successful!" -ForegroundColor Green
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Note the Service URL from above" -ForegroundColor White
    Write-Host "2. Update frontend/widget.js with the URL" -ForegroundColor White
    Write-Host "3. Add widget to your GitHub Pages site" -ForegroundColor White
} else {
    Write-Host "`nDeployment failed. Check the error messages above." -ForegroundColor Red
}
