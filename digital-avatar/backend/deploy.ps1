# AI Avatar Backend Deployment Script for PowerShell
# This script deploys the backend to Google Cloud Run

param(
    [string]$ProjectId,
    [string]$ApiKey,
    [string]$Region = "us-central1"
)

# Colors
$ErrorColor = "Red"
$SuccessColor = "Green"
$InfoColor = "Yellow"

Write-Host "=== AI Avatar Backend Deployment ===" -ForegroundColor $SuccessColor
Write-Host ""

# Check if required commands are available
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "Error: gcloud CLI is not installed" -ForegroundColor $ErrorColor
    exit 1
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed" -ForegroundColor $ErrorColor
    exit 1
}

# Get configuration if not provided
if (-not $ProjectId) {
    $ProjectId = Read-Host "Enter GCP Project ID"
}

if (-not $ApiKey) {
    $ApiKey = Read-Host "Enter Gemini API Key"
}

if (-not $Region) {
    $Region = Read-Host "Enter Cloud Run region [us-central1]"
    if ([string]::IsNullOrWhiteSpace($Region)) {
        $Region = "us-central1"
    }
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor $InfoColor
Write-Host "  Project ID: $ProjectId"
Write-Host "  Region: $Region"
Write-Host "  API Key: $($ApiKey.Substring(0, [Math]::Min(10, $ApiKey.Length)))..."
Write-Host ""

$confirm = Read-Host "Continue with deployment? (y/n)"
if ($confirm -ne 'y' -and $confirm -ne 'Y') {
    Write-Host "Deployment cancelled."
    exit 0
}

# Set GCP project
Write-Host ""
Write-Host "Setting GCP project..." -ForegroundColor $InfoColor
$timer = [System.Diagnostics.Stopwatch]::StartNew()
try {
    $output = gcloud config set project $ProjectId 2>&1
    Write-Host "  $output" -ForegroundColor DarkGray
    $timer.Stop()
    Write-Host "[OK] Project set ($($timer.Elapsed.TotalSeconds.ToString('0.0'))s)" -ForegroundColor $SuccessColor
} catch {
    Write-Host "Error setting project: $_" -ForegroundColor $ErrorColor
    exit 1
}

# Navigate to script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Step 1: Sync knowledge base
Write-Host ""
Write-Host "Step 1/5: Syncing knowledge base..." -ForegroundColor $InfoColor
$timer = [System.Diagnostics.Stopwatch]::StartNew()
if (Test-Path "knowledge_base") {
    Remove-Item -Recurse -Force "knowledge_base"
}
New-Item -ItemType Directory -Path "knowledge_base" | Out-Null
Copy-Item -Recurse -Path "..\..\knowledge-base\*" -Destination "knowledge_base\"
$fileCount = (Get-ChildItem -Recurse "knowledge_base" -File).Count
$timer.Stop()
Write-Host "[OK] Knowledge base synced - $fileCount files ($($timer.Elapsed.TotalSeconds.ToString('0.0'))s)" -ForegroundColor $SuccessColor

# Step 2: Build Docker image
Write-Host ""
Write-Host "Step 2/5: Building Docker image (this may take 2-3 minutes)..." -ForegroundColor $InfoColor
$timer = [System.Diagnostics.Stopwatch]::StartNew()
$ImageName = "gcr.io/$ProjectId/ai-avatar:latest"
docker build -t $ImageName . 2>&1 | ForEach-Object {
    if ($_ -match "Step \d+/\d+") {
        Write-Host "  $_" -ForegroundColor DarkGray
    }
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker build failed" -ForegroundColor $ErrorColor
    exit 1
}
$timer.Stop()
Write-Host "[OK] Docker image built ($($timer.Elapsed.TotalSeconds.ToString('0.0'))s)" -ForegroundColor $SuccessColor

# Step 3: Configure Docker for GCR
Write-Host ""
Write-Host "Step 3/5: Configuring Docker authentication..." -ForegroundColor $InfoColor
$timer = [System.Diagnostics.Stopwatch]::StartNew()
$output = gcloud auth configure-docker gcr.io --quiet 2>&1
if ($output) {
    Write-Host "  $output" -ForegroundColor DarkGray
}
$timer.Stop()
Write-Host "[OK] Docker configured ($($timer.Elapsed.TotalSeconds.ToString('0.0'))s)" -ForegroundColor $SuccessColor

# Step 4: Push to Google Container Registry
Write-Host ""
Write-Host "Step 4/5: Pushing image to GCR (this may take 2-5 minutes)..." -ForegroundColor $InfoColor
$timer = [System.Diagnostics.Stopwatch]::StartNew()
docker push $ImageName 2>&1 | ForEach-Object {
    if ($_ -match "Pushed|Pushing|Waiting") {
        Write-Host "  $_" -ForegroundColor DarkGray
    }
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Docker push failed" -ForegroundColor $ErrorColor
    exit 1
}
$timer.Stop()
Write-Host "[OK] Image pushed to GCR ($($timer.Elapsed.TotalSeconds.ToString('0.0'))s)" -ForegroundColor $SuccessColor

# Step 5: Deploy to Cloud Run
Write-Host ""
Write-Host "Step 5/5: Deploying to Cloud Run..." -ForegroundColor $InfoColor
gcloud run deploy ai-avatar `
    --image $ImageName `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --set-env-vars GEMINI_API_KEY=$ApiKey `
    --memory 512Mi `
    --cpu 1 `
    --max-instances 10 `
    --timeout 300

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Cloud Run deployment failed" -ForegroundColor $ErrorColor
    exit 1
}

Write-Host ""
Write-Host "=== Deployment Complete ===" -ForegroundColor $SuccessColor
Write-Host ""

# Get service URL
$ServiceUrl = gcloud run services describe ai-avatar --region $Region --format "value(status.url)"
Write-Host "Service URL: $ServiceUrl" -ForegroundColor $SuccessColor
Write-Host ""
Write-Host "Test the service:"
Write-Host "  curl $ServiceUrl/"
Write-Host ""
Write-Host "View logs:"
Write-Host "  gcloud run services logs read ai-avatar --region $Region"
Write-Host ""
