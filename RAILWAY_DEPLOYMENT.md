# Railway Deployment Guide

This guide will help you deploy the Scripture Search app to Railway.

## Prerequisites

- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))
- OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

## Step 1: Prepare Your Repository

### 1.1 Initialize Git (if not already done)

```bash
git init
```

### 1.2 Add all files

```bash
git add .
```

### 1.3 Commit your code

```bash
git commit -m "Initial commit - Scripture search app"
```

### 1.4 Push to GitHub

Create a new repository on GitHub, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Railway

### 2.1 Create New Project

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub account
5. Select your scripture search repository

### 2.2 Configure Environment Variables

1. In your Railway project, click on your service
2. Go to the "Variables" tab
3. Add the following variable:
   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   ```

### 2.3 Deploy

Railway will automatically:
- Detect it's a Python project
- Install dependencies from `pyproject.toml`
- Use the `Procfile` to start the app
- Assign a public URL

## Step 3: Verify Deployment

1. Wait for deployment to complete (usually 2-5 minutes)
2. Click the generated URL (something like `your-app.up.railway.app`)
3. Test a search query
4. Verify all features work:
   - Example queries
   - Search functionality
   - Copy button
   - URL parameters
   - Statistics display

## Troubleshooting

### Build Fails

**Issue**: Build process fails or times out

**Solution**:
- Check the build logs in Railway dashboard
- Ensure all files are committed to git
- Verify `pyproject.toml` has all dependencies

### App Won't Start

**Issue**: App builds but doesn't start

**Solution**:
- Check that `OPENROUTER_API_KEY` is set in environment variables
- View logs in Railway dashboard
- Ensure PORT environment variable is being read (Railway sets this automatically)

### Data Files Missing

**Issue**: "File not found" errors for embeddings

**Solution**:
- Verify `data/` directory is committed to git
- Check that `.gitignore` doesn't exclude data files
- Ensure embedding files are under Railway's size limits

### Slow First Load

**Issue**: First request takes 30+ seconds

**Solution**:
- This is normal - Railway loads embeddings into memory on startup
- Subsequent requests will be fast
- Consider upgrading to Railway Pro for better performance

## Monitoring

### View Logs

```bash
# Install Railway CLI (optional)
npm i -g @railway/cli

# Login
railway login

# View logs
railway logs
```

### Check Metrics

In Railway dashboard:
- CPU usage
- Memory usage (expect ~500MB+ for embeddings)
- Request count
- Response times

## Updating Your App

### Deploy Changes

```bash
git add .
git commit -m "Your update message"
git push
```

Railway will automatically redeploy when you push to main.

## Cost Considerations

- **Railway**: Free tier includes 500 hours/month ($5 credit)
- **OpenRouter API**: Pay per API call for embeddings
  - ~$0.002 per search query (depends on model)
  - Monitor usage in OpenRouter dashboard

## Performance Tips

1. **Optimize Cold Starts**: Embeddings are loaded at startup (2-3 seconds)
2. **Cache Strategy**: Consider caching frequent queries
3. **Rate Limiting**: Already implemented (1 query/second)
4. **Scaling**: Railway auto-scales based on traffic

## Support

- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub issues: [Your repo issues page]
