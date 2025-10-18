#!/bin/bash

# 🚀 TypeScript RAG API - Quick Deploy Script
# This script helps you deploy to various platforms

echo "🚀 TypeScript RAG API Deployment Helper"
echo "========================================"
echo ""
echo "Choose a deployment platform:"
echo ""
echo "1) Cloudflare Pages (Recommended - FREE, Global CDN)"
echo "2) Railway.app (FREE - Easy Python hosting)"
echo "3) Fly.io (FREE tier - Global deployment)"
echo "4) Render.com (FREE - Simple setup)"
echo "5) Manual Cloudflare Worker (Copy-paste deployment)"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
  1)
    echo ""
    echo "📦 Deploying to Cloudflare Pages..."
    echo ""
    
    # Check if wrangler is installed
    if ! command -v wrangler &> /dev/null; then
        echo "Installing Wrangler CLI..."
        npm install -g wrangler
    fi
    
    # Login
    echo "Logging in to Cloudflare..."
    wrangler login
    
    # Deploy
    echo "Deploying to Cloudflare Pages..."
    cd cloudflare-pages
    wrangler pages deploy . --project-name=typescript-rag
    
    echo ""
    echo "✅ Deployment complete!"
    echo "🌐 Your public URL: https://typescript-rag.pages.dev/api/GA3/8"
    echo ""
    echo "Test it:"
    echo "curl 'https://typescript-rag.pages.dev/api/GA3/8?q=What%20does%20the%20author%20affectionately%20call%20the%20%3D%3E%20syntax?'"
    ;;
    
  2)
    echo ""
    echo "🚂 Deploying to Railway.app..."
    echo ""
    
    # Check if railway CLI is installed
    if ! command -v railway &> /dev/null; then
        echo "Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    # Login
    echo "Logging in to Railway..."
    railway login
    
    # Initialize and deploy
    echo "Initializing Railway project..."
    railway init
    
    echo "Deploying..."
    railway up
    
    echo ""
    echo "✅ Deployment complete!"
    echo "🌐 Get your URL from Railway dashboard: https://railway.app/dashboard"
    echo ""
    echo "Your endpoint will be: https://your-app.railway.app/search"
    ;;
    
  3)
    echo ""
    echo "✈️  Deploying to Fly.io..."
    echo ""
    
    # Check if fly CLI is installed
    if ! command -v fly &> /dev/null; then
        echo "Installing Fly CLI..."
        curl -L https://fly.io/install.sh | sh
        export FLYCTL_INSTALL="/Users/$USER/.fly"
        export PATH="$FLYCTL_INSTALL/bin:$PATH"
    fi
    
    # Login
    echo "Logging in to Fly.io..."
    fly auth login
    
    # Launch
    echo "Launching on Fly.io..."
    fly launch --now
    
    echo ""
    echo "✅ Deployment complete!"
    echo "🌐 Your public URL: https://typescript-rag-api.fly.dev/search"
    ;;
    
  4)
    echo ""
    echo "🎨 Deploying to Render.com..."
    echo ""
    echo "Render requires web-based deployment. Follow these steps:"
    echo ""
    echo "1. Visit: https://render.com"
    echo "2. Sign up/Login with GitHub"
    echo "3. Click 'New +' → 'Web Service'"
    echo "4. Connect this repository: https://github.com/sathish-k7/Tools_in_DS"
    echo "5. Configure:"
    echo "   - Name: typescript-rag-api"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Start Command: python typescript_rag_api.py"
    echo "   - Environment: Python 3"
    echo "6. Click 'Create Web Service'"
    echo ""
    echo "Your URL will be: https://typescript-rag-api.onrender.com/search"
    echo ""
    read -p "Press Enter to open Render.com in browser..."
    open "https://render.com"
    ;;
    
  5)
    echo ""
    echo "📋 Manual Cloudflare Worker Deployment"
    echo ""
    echo "Follow these steps:"
    echo ""
    echo "1. Visit: https://dash.cloudflare.com"
    echo "2. Go to 'Workers & Pages' → 'Create Application'"
    echo "3. Click 'Create Worker'"
    echo "4. Give it a name (e.g., 'typescript-rag')"
    echo "5. Click 'Deploy'"
    echo "6. Click 'Edit Code'"
    echo "7. Replace all code with the content from: standalone-worker.js"
    echo "8. Click 'Save and Deploy'"
    echo ""
    echo "Your URL will be: https://typescript-rag.YOUR_SUBDOMAIN.workers.dev"
    echo ""
    echo "📄 Opening standalone-worker.js for you to copy..."
    
    if command -v code &> /dev/null; then
        code standalone-worker.js
    else
        cat standalone-worker.js
    fi
    
    read -p "Press Enter to open Cloudflare dashboard..."
    open "https://dash.cloudflare.com"
    ;;
    
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac

echo ""
echo "🎉 Deployment process initiated!"
echo ""
echo "📚 Documentation:"
echo "  - PUBLIC_DEPLOYMENT.md - Full deployment guide"
echo "  - DEPLOYMENT_GUIDE.md - Detailed instructions"
echo "  - QUICKSTART.md - Quick reference"
echo ""
echo "🧪 Test your deployment:"
echo "  curl 'YOUR_URL?q=What%20does%20the%20author%20affectionately%20call%20the%20%3D%3E%20syntax?'"
echo ""
