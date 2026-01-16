#!/bin/bash

# AI Avatar Backend Deployment Script
# This script deploys the backend to Google Cloud Run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== AI Avatar Backend Deployment ===${NC}"
echo ""

# Check if required commands are available
command -v gcloud >/dev/null 2>&1 || { echo -e "${RED}Error: gcloud CLI is not installed${NC}"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo -e "${RED}Error: Docker is not installed${NC}"; exit 1; }

# Configuration
read -p "Enter GCP Project ID: " GCP_PROJECT_ID
read -p "Enter Gemini API Key: " GEMINI_API_KEY
read -p "Enter Cloud Run region [us-central1]: " REGION
REGION=${REGION:-us-central1}

echo ""
echo -e "${YELLOW}Configuration:${NC}"
echo "  Project ID: $GCP_PROJECT_ID"
echo "  Region: $REGION"
echo "  API Key: ${GEMINI_API_KEY:0:10}..."
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

# Set GCP project
echo -e "${YELLOW}Setting GCP project...${NC}"
gcloud config set project $GCP_PROJECT_ID

# Navigate to backend directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Step 1: Sync knowledge base
echo ""
echo -e "${YELLOW}Step 1/5: Syncing knowledge base...${NC}"
rm -rf knowledge_base
mkdir knowledge_base
cp -r ../../knowledge-base/* knowledge_base/
cp -r ../../_projects knowledge_base/projects/
echo -e "${GREEN}✓ Knowledge base synced${NC}"

# Step 1.5: Copy root markdown files (M-Shape context)
echo ""
echo -e "${YELLOW}Step 1.5/5: Copying root context files...${NC}"
cp ../../profile.md .
cp ../../business-challenges.md .
cp ../../index.md .
echo -e "${GREEN}✓ Root files copied${NC}"

# Step 2: Build Docker image
echo ""
echo -e "${YELLOW}Step 2/5: Building Docker image...${NC}"
IMAGE_NAME="gcr.io/$GCP_PROJECT_ID/ai-avatar:latest"
docker build --platform linux/amd64 -t $IMAGE_NAME .
echo -e "${GREEN}✓ Docker image built${NC}"

# Step 3: Configure Docker for GCR
echo ""
echo -e "${YELLOW}Step 3/5: Configuring Docker authentication...${NC}"
gcloud auth configure-docker gcr.io --quiet
echo -e "${GREEN}✓ Docker configured${NC}"

# Step 4: Push to Google Container Registry
echo ""
echo -e "${YELLOW}Step 4/5: Pushing image to GCR...${NC}"
docker push $IMAGE_NAME
echo -e "${GREEN}✓ Image pushed to GCR${NC}"

# Step 5: Deploy to Cloud Run
echo ""
echo -e "${YELLOW}Step 5/5: Deploying to Cloud Run...${NC}"
gcloud run deploy ai-avatar \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300

echo ""
echo -e "${GREEN}=== Deployment Complete ===${NC}"
echo ""

# Get service URL
SERVICE_URL=$(gcloud run services describe ai-avatar --region $REGION --format 'value(status.url)')
echo -e "${GREEN}Service URL: $SERVICE_URL${NC}"
echo ""
echo "Test the service:"
echo "  curl $SERVICE_URL/"
echo ""
echo "View logs:"
echo "  gcloud run services logs read ai-avatar --region $REGION"
echo ""
