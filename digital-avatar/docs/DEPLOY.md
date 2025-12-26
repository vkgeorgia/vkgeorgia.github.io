# Deploy to Google Cloud Run

## Prerequisites
1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Authenticate: `gcloud auth login`
3. Set project: `gcloud config set project YOUR_PROJECT_ID`

## Deployment Steps

### 1. Build and Deploy
```powershell
cd c:\GitHub\digital-avatar\backend

# Deploy to Cloud Run (will build automatically)
gcloud run deploy ai-avatar `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars GEMINI_API_KEY=your_api_key_here,GOOGLE_DRIVE_FOLDER_ID=1QBvZWfU3rPfm93UuYqipTaDxu_-o8pOZ
```

### 2. Note Your Service URL
After deployment, you'll see:
```
Service URL: https://ai-avatar-xxxxx-uc.a.run.app
```

### 3. Update Widget Configuration
Edit `frontend/widget.js` line 13 with your Cloud Run URL.

### 4. Test the Deployment
```powershell
# Test health endpoint
curl https://ai-avatar-xxxxx-uc.a.run.app/

# Test WebSocket (use browser)
# Open: https://ai-avatar-xxxxx-uc.a.run.app/static/index.html
```

## Environment Variables
Set these in Cloud Run:
- `GEMINI_API_KEY` - Your Gemini API key
- `GOOGLE_DRIVE_FOLDER_ID` - Your Drive folder ID

## Troubleshooting

### Build fails
- Check Dockerfile syntax
- Verify all files are copied correctly
- Check requirements.txt

### Service doesn't start
- Check Cloud Run logs: `gcloud run logs read ai-avatar`
- Verify environment variables are set
- Check PORT is 8080

### CORS errors
- Verify `vkgeorgia.github.io` is in allowed origins
- Check browser console for exact error

## Cost Estimation
- **Free tier**: 2 million requests/month
- **After free tier**: ~$0.40 per million requests
- **Typical usage**: Should stay within free tier

## Next Steps
After deployment:
1. Update `widget.js` with Cloud Run URL
2. Test widget locally
3. Add widget to GitHub Pages
4. Monitor usage in Cloud Console
