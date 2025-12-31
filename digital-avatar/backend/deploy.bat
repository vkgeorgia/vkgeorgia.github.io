@echo off
REM AI Avatar Backend Deployment Script for Windows
REM This script deploys the backend to Google Cloud Run

setlocal enabledelayedexpansion

echo === AI Avatar Backend Deployment ===
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: gcloud CLI is not installed
    exit /b 1
)

REM Check if docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker is not installed
    exit /b 1
)

REM Configuration
set /p GCP_PROJECT_ID="Enter GCP Project ID: "
set /p GEMINI_API_KEY="Enter Gemini API Key: "
set /p REGION="Enter Cloud Run region [us-central1]: "
if "%REGION%"=="" set REGION=us-central1

echo.
echo Configuration:
echo   Project ID: %GCP_PROJECT_ID%
echo   Region: %REGION%
echo   API Key: %GEMINI_API_KEY:~0,10%...
echo.

set /p CONFIRM="Continue with deployment? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Deployment cancelled.
    exit /b 0
)

REM Set GCP project
echo.
echo Setting GCP project...
gcloud config set project %GCP_PROJECT_ID%

REM Navigate to backend directory
cd /d %~dp0

REM Step 1: Sync knowledge base
echo.
echo Step 1/5: Syncing knowledge base...
if exist knowledge_base rmdir /s /q knowledge_base
mkdir knowledge_base
xcopy /s /e /i /y ..\..\knowledge-base\* knowledge_base\
echo [OK] Knowledge base synced

REM Step 2: Build Docker image
echo.
echo Step 2/5: Building Docker image...
set IMAGE_NAME=gcr.io/%GCP_PROJECT_ID%/ai-avatar:latest
docker build -t %IMAGE_NAME% .
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker build failed
    exit /b 1
)
echo [OK] Docker image built

REM Step 3: Configure Docker for GCR
echo.
echo Step 3/5: Configuring Docker authentication...
gcloud auth configure-docker gcr.io --quiet
echo [OK] Docker configured

REM Step 4: Push to Google Container Registry
echo.
echo Step 4/5: Pushing image to GCR...
docker push %IMAGE_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo Error: Docker push failed
    exit /b 1
)
echo [OK] Image pushed to GCR

REM Step 5: Deploy to Cloud Run
echo.
echo Step 5/5: Deploying to Cloud Run...
gcloud run deploy ai-avatar ^
  --image %IMAGE_NAME% ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --set-env-vars GEMINI_API_KEY=%GEMINI_API_KEY% ^
  --memory 512Mi ^
  --cpu 1 ^
  --max-instances 10 ^
  --timeout 300

if %ERRORLEVEL% NEQ 0 (
    echo Error: Cloud Run deployment failed
    exit /b 1
)

echo.
echo === Deployment Complete ===
echo.

REM Get service URL
for /f "tokens=*" %%i in ('gcloud run services describe ai-avatar --region %REGION% --format "value(status.url)"') do set SERVICE_URL=%%i
echo Service URL: %SERVICE_URL%
echo.
echo Test the service:
echo   curl %SERVICE_URL%/
echo.
echo View logs:
echo   gcloud run services logs read ai-avatar --region %REGION%
echo.

endlocal
