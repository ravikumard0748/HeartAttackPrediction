#!/bin/bash

# Heart Attack Prediction System - Deployment Script
# This script prepares the project for Netlify deployment

echo "🚀 Preparing Heart Attack Prediction System for deployment..."

# Create dist directory
echo "📁 Creating dist directory..."
mkdir -p dist

# Copy HTML templates to dist
echo "📄 Copying HTML files..."
cp templates/*.html dist/

# Copy static files to dist
echo "🎨 Copying static files..."
cp -r static dist/

# Copy model file to dist
echo "🤖 Copying ML model..."
cp finalfinalmodel.joblib dist/

# Copy netlify functions
echo "⚡ Setting up serverless functions..."
mkdir -p dist/.netlify
cp -r netlify dist/.netlify/

echo "✅ Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Connect your repository to Netlify"
echo "3. Set build command: npm run build"
echo "4. Set publish directory: dist"
echo "5. Configure environment variables in Netlify dashboard"
echo ""
echo "🌐 Your app will be available at: https://your-site-name.netlify.app"
