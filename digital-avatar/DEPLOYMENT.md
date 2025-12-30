# Backend Deployment Guide

## Quick Deploy (Manual)

### Prerequisites
1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Authenticate: `gcloud auth login`
3. Set project: `gcloud config set project YOUR_PROJECT_ID`

### Deploy Steps

```bash
# 1. Navigate to backend directory
cd digital-avatar/backend

# 2. Sync knowledge base
rm -rf knowledge_base
mkdir knowledge_base
cp -r ../../knowledge-base/* knowledge_base/

# 3. Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/ai-avatar:latest .

# 4. Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/ai-avatar:latest

# 5. Deploy to Cloud Run
gcloud run deploy ai-avatar \
  --image gcr.io/YOUR_PROJECT_ID/ai-avatar:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Automatic Deploy (GitHub Actions)

### Setup

1. **Create Google Cloud Service Account:**
   ```bash
   gcloud iam service-accounts create github-actions \
     --display-name="GitHub Actions"
   ```

2. **Grant permissions:**
   ```bash
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   
   gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
     --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/iam.serviceAccountUser"
   ```

3. **Create and download key:**
   ```bash
   gcloud iam service-accounts keys create key.json \
     --iam-account=github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

4. **Add GitHub Secrets:**
   - Go to: https://github.com/vkgeorgia/vkgeorgia.github.io/settings/secrets/actions
   - Add secrets:
     - `GCP_SA_KEY` - Content of `key.json` file
     - `GCP_PROJECT_ID` - Your Google Cloud project ID
     - `GEMINI_API_KEY` - Your Gemini API key

### Trigger Deployment

**Automatic:**
- Push changes to `digital-avatar/backend/` or `knowledge-base/`
- Workflow runs automatically

**Manual:**
- Go to: https://github.com/vkgeorgia/vkgeorgia.github.io/actions
- Select "Deploy AI Avatar Backend to Cloud Run"
- Click "Run workflow"
- Choose branch (main or test-minima)
- Click "Run workflow"

---

## Local Testing

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variable
export GEMINI_API_KEY=your-key  # Windows: set GEMINI_API_KEY=your-key

# 4. Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Test
# Open http://localhost:8000
# WebSocket: ws://localhost:8000/ws/chat
```

---

## Verify Deployment

```bash
# Check Cloud Run service
gcloud run services describe ai-avatar --region us-central1

# View logs
gcloud run services logs read ai-avatar --region us-central1

# Test endpoint
curl https://YOUR_SERVICE_URL/
```

---

## Rollback

```bash
# List revisions
gcloud run revisions list --service ai-avatar --region us-central1

# Rollback to previous revision
gcloud run services update-traffic ai-avatar \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

---

## Troubleshooting

**Build fails:**
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Ensure knowledge_base directory exists

**Deploy fails:**
- Check GCP permissions
- Verify project ID and region
- Check Cloud Run quotas

**Service not responding:**
- Check logs: `gcloud run services logs read ai-avatar`
- Verify GEMINI_API_KEY is set
- Check knowledge base loaded correctly

---

## Cost Optimization

- Cloud Run charges only when serving requests
- Free tier: 2 million requests/month
- Minimize container size (use slim Python image)
- Set max instances to control costs

---

**Last Updated:** 2025-12-30
