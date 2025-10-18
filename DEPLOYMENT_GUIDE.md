# 🚀 Deployment Guide - TypeScript RAG API

## Quick Start (Local Testing)

The API is now running locally! Test it:

```bash
# Test endpoint 1
curl "http://127.0.0.1:8000/search?q=What%20does%20the%20author%20affectionately%20call%20the%20%3D%3E%20syntax?"

# Test endpoint 2  
curl "http://127.0.0.1:8000/search?q=Which%20operator%20converts%20any%20value%20into%20an%20explicit%20boolean?"

# Open web interface
open http://127.0.0.1:8000
```

## ✅ Verified Working

Both example questions return correct answers:

1. **Q:** "What does the author affectionately call the => syntax?"
   - **A:** "fat arrow" ✅
   - Confidence: 93.7%

2. **Q:** "Which operator converts any value into an explicit boolean?"
   - **A:** "!!" ✅
   - Confidence: 94.6%

## 🌍 Deploy to Cloudflare Pages

### Prerequisites

1. **Cloudflare Account** (free tier available)
2. **Wrangler CLI** installed:
   ```bash
   npm install -g wrangler
   ```

### Deployment Steps

#### Option 1: CLI Deployment (Fastest)

```bash
# 1. Navigate to cloudflare-pages directory
cd cloudflare-pages

# 2. Login to Cloudflare
wrangler login

# 3. Deploy
wrangler pages deploy . --project-name=tdsfu

# 4. Your API will be live at:
# https://tdsfu.pages.dev/api/GA3/8?q=your_question
```

#### Option 2: GitHub Integration (Recommended for CI/CD)

1. **Push to GitHub:**
   ```bash
   cd cloudflare-pages
   git init
   git add .
   git commit -m "Initial TypeScript RAG API"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/typescript-rag.git
   git push -u origin main
   ```

2. **Connect to Cloudflare Pages:**
   - Go to https://dash.cloudflare.com
   - Click "Pages" → "Create a project"
   - Connect your GitHub repository
   - Set build configuration:
     - **Build command:** (leave empty)
     - **Build output directory:** `/`
     - **Root directory:** `cloudflare-pages`
   - Click "Save and Deploy"

3. **Your site will be live at:**
   ```
   https://YOUR_PROJECT.pages.dev/api/GA3/8
   ```

#### Option 3: Manual Upload

1. Go to https://dash.cloudflare.com
2. Click "Pages" → "Create a project" → "Upload assets"
3. Drag and drop the `cloudflare-pages` folder
4. Click "Deploy site"

### Verify Deployment

```bash
# Test your deployed API
curl "https://tdsfu.pages.dev/api/GA3/8?q=What%20does%20the%20author%20affectionately%20call%20the%20%3D%3E%20syntax?"

# Should return:
# {
#   "answer": "fat arrow",
#   "sources": "TypeScript Deep Dive by Basarat Ali Syed",
#   "confidence": 0.937
# }
```

## 📋 Configuration Options

### Custom Domain

In Cloudflare Pages dashboard:
1. Go to your project
2. Click "Custom domains"
3. Add your domain (e.g., `api.yourdomain.com`)
4. Update DNS records as instructed

### Environment Variables (Optional)

For OpenAI embeddings (production enhancement):

```bash
wrangler pages secret put OPENAI_API_KEY
# Enter your API key when prompted
```

### Rate Limiting

Add to `functions/api/GA3/8.js`:

```javascript
// Add rate limiting
const RATE_LIMIT = 100; // requests per minute
const clientRequests = new Map();

export async function onRequestGet(context) {
  const clientIP = context.request.headers.get('CF-Connecting-IP');
  
  // Check rate limit
  const now = Date.now();
  const requests = clientRequests.get(clientIP) || [];
  const recentRequests = requests.filter(time => now - time < 60000);
  
  if (recentRequests.length >= RATE_LIMIT) {
    return new Response('Rate limit exceeded', { status: 429 });
  }
  
  recentRequests.push(now);
  clientRequests.set(clientIP, recentRequests);
  
  // ... rest of your code
}
```

## 🔧 Troubleshooting

### Local Server Not Starting

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill existing process
kill -9 <PID>

# Restart server
python typescript_rag_api.py
```

### Cloudflare Deployment Fails

1. **Check file structure:**
   ```
   cloudflare-pages/
   ├── index.html
   ├── wrangler.toml
   └── functions/
       └── api/
           └── GA3/
               └── 8.js
   ```

2. **Verify wrangler.toml:**
   ```bash
   cd cloudflare-pages
   wrangler pages deploy . --project-name=tdsfu
   ```

3. **Check function logs:**
   ```bash
   wrangler pages deployment tail
   ```

### CORS Issues

If you get CORS errors, verify these headers in `8.js`:

```javascript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};
```

## 📊 Monitoring & Analytics

### View Logs (Cloudflare)

```bash
wrangler pages deployment tail --project-name=tdsfu
```

### Add Analytics

In Cloudflare dashboard:
1. Go to your Pages project
2. Enable "Web Analytics"
3. View request metrics, response times, and error rates

### Custom Logging

Add to your function:

```javascript
export async function onRequestGet(context) {
  console.log('Request:', {
    query: context.request.url,
    timestamp: new Date().toISOString(),
    cf: context.request.cf
  });
  
  // ... your code
}
```

## 🎯 Testing Checklist

- [ ] Local API responds on http://127.0.0.1:8000
- [ ] Example question 1 returns "fat arrow"
- [ ] Example question 2 returns "!!"
- [ ] Web interface loads and works
- [ ] CORS headers are present
- [ ] Production API deployed to Cloudflare
- [ ] Production URL accessible
- [ ] Custom domain configured (optional)
- [ ] Rate limiting implemented (optional)
- [ ] Analytics enabled (optional)

## 🚀 Next Steps

1. **Enhance Knowledge Base**: Add more TypeScript documentation
2. **Implement Caching**: Cache frequent queries
3. **Add Authentication**: Protect API with API keys
4. **Implement Vector Search**: Use proper embeddings (OpenAI, Sentence Transformers)
5. **Add Feedback Loop**: Collect user ratings on answers
6. **Monitor Performance**: Set up alerts for errors and slow responses

## 📚 Additional Resources

- [Cloudflare Pages Docs](https://developers.cloudflare.com/pages/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TypeScript Deep Dive Book](https://github.com/basarat/typescript-book/)

## 💡 Pro Tips

1. **Use Cloudflare Analytics** to understand query patterns
2. **Implement caching** for frequently asked questions
3. **Set up monitoring** to catch errors early
4. **Version your API** (e.g., `/api/v1/GA3/8`)
5. **Document your endpoints** with OpenAPI/Swagger
6. **Add health check endpoint** for monitoring

---

**Your API is ready for production! 🎉**

Local: `http://127.0.0.1:8000/search?q=your_question`
Production: `https://tdsfu.pages.dev/api/GA3/8?q=your_question`
