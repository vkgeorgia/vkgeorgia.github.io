# Quick Deployment Test Script
# This script tests if gcloud and docker are working correctly

Write-Host "=== Testing Deployment Prerequisites ===" -ForegroundColor Green
Write-Host ""

# Test 1: Check gcloud
Write-Host "Test 1: Checking gcloud..." -ForegroundColor Yellow
try {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    Write-Host "[OK] gcloud found: $gcloudVersion" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] gcloud not found or not working" -ForegroundColor Red
    exit 1
}

# Test 2: Check Docker
Write-Host ""
Write-Host "Test 2: Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "[OK] Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] Docker not found or not working" -ForegroundColor Red
    exit 1
}

# Test 3: Check Docker daemon
Write-Host ""
Write-Host "Test 3: Checking Docker daemon..." -ForegroundColor Yellow
try {
    docker ps 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Docker daemon is running" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] Docker daemon is not running. Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[FAIL] Cannot connect to Docker daemon" -ForegroundColor Red
    exit 1
}

# Test 4: Check gcloud auth
Write-Host ""
Write-Host "Test 4: Checking gcloud authentication..." -ForegroundColor Yellow
try {
    $account = gcloud config get-value account 2>&1
    if ($account -and $account -ne "(unset)") {
        Write-Host "[OK] Authenticated as: $account" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Not authenticated. Run: gcloud auth login" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARN] Could not check authentication" -ForegroundColor Yellow
}

# Test 5: Check current project
Write-Host ""
Write-Host "Test 5: Checking current GCP project..." -ForegroundColor Yellow
try {
    $project = gcloud config get-value project 2>&1
    if ($project -and $project -ne "(unset)") {
        Write-Host "[OK] Current project: $project" -ForegroundColor Green
    } else {
        Write-Host "[WARN] No project set" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[WARN] Could not check project" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== All Tests Passed ===" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run: .\deploy.ps1" -ForegroundColor Cyan
