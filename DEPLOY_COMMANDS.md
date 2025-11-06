# Quick Deployment Commands

## Step 1: Commit Your Code

```bash
# Commit all files
git commit -m "Initial commit - Scripture search with semantic search"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `book-of-mormon-search`)
3. **DO NOT** initialize with README (we already have one)

## Step 3: Push to GitHub

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 4: Deploy on Railway

1. Visit https://railway.app
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access GitHub
5. Select your `book-of-mormon-search` repository
6. Click "Deploy Now"

## Step 5: Add Environment Variable

In Railway dashboard:
1. Click on your service
2. Go to "Variables" tab
3. Click "New Variable"
4. Add:
   - **Variable**: `OPENROUTER_API_KEY`
   - **Value**: Your actual OpenRouter API key
5. Click "Add"

## Step 6: Access Your App

1. Wait for deployment to complete (2-5 minutes)
2. Railway will show you the public URL
3. Click the URL to open your app
4. Test with a search query!

## Future Updates

After making changes to your code:

```bash
git add .
git commit -m "Description of changes"
git push
```

Railway will automatically redeploy!

## Need Help?

- See [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) for detailed instructions
- Check Railway logs for errors
- View deployment status in Railway dashboard
