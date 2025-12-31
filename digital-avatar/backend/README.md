# Backend Deployment Scripts

This directory contains scripts for deploying the AI Avatar backend to Google Cloud Run.

## Prerequisites

1. **Google Cloud SDK** - [Install](https://cloud.google.com/sdk/docs/install)
2. **Docker** - [Install](https://docs.docker.com/get-docker/)
3. **Authenticated to GCP:**
   ```bash
   gcloud auth login
   ```

## Usage

### Linux/Mac

```bash
cd digital-avatar/backend
chmod +x deploy.sh
./deploy.sh
```

### Windows

```cmd
cd digital-avatar\backend
deploy.bat
```

## What the script does

1. **Syncs knowledge base** - Copies latest content from `knowledge-base/` to `backend/knowledge_base/`
2. **Builds Docker image** - Creates container with backend code and knowledge base
3. **Pushes to GCR** - Uploads image to Google Container Registry
4. **Deploys to Cloud Run** - Updates the running service with new image

## Configuration

The script will prompt for:
- **GCP Project ID** - Your Google Cloud project
- **Gemini API Key** - Your API key for Gemini AI
- **Region** - Cloud Run region (default: us-central1)

## After Deployment

The script will display:
- Service URL (e.g., `https://ai-avatar-xxx.run.app`)
- Test command
- Logs command

## Troubleshooting

**Permission denied:**
```bash
chmod +x deploy.sh
```

**Docker not running:**
```bash
# Start Docker Desktop or Docker daemon
```

**GCP authentication failed:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**Build fails:**
- Check Dockerfile syntax
- Ensure all files exist
- Verify Docker has enough disk space

## Manual Deployment

If the script fails, you can run commands manually:

```bash
# 1. Sync knowledge base
rm -rf knowledge_base
mkdir knowledge_base
cp -r ../../knowledge-base/* knowledge_base/

# 2. Build image
docker build -t gcr.io/YOUR_PROJECT_ID/ai-avatar:latest .

# 3. Push image
docker push gcr.io/YOUR_PROJECT_ID/ai-avatar:latest

# 4. Deploy
gcloud run deploy ai-avatar \
  --image gcr.io/YOUR_PROJECT_ID/ai-avatar:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_KEY
```

## See Also

- [DEPLOYMENT.md](../DEPLOYMENT.md) - Full deployment guide
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - System architecture
