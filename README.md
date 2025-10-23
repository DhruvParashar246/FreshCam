# FreshCam
FreshCam 🍎🥦

AI-powered produce analysis app that helps users identify fruit & vegetable ripeness, accessibility features for color-blind users, and nutrition insights.

🚀 Overview

FreshCam combines Computer Vision and backend engineering to make produce shopping smarter.

Custom-trained CNN (Roboflow dataset) achieving 90% classification accuracy.

FastAPI inference pipeline optimized for 30% faster predictions.

React Native (Expo) frontend for mobile image capture and results display.

Gemini API integration for instant nutrition insights.

Accessibility features to support color-blind users.

🛠️ Tech Stack

Frontend: React Native (Expo), TypeScript
Backend: FastAPI, Python, Docker
ML: CNN (Roboflow), NumPy, Pandas
APIs: Gemini API, Firebase (optional integration)
DevOps: Docker Compose, GitHub Actions

✨ Features

📷 Upload or capture produce images for instant ripeness analysis.

🧠 ML-powered classification with 90%+ accuracy.

⚡ Optimized inference pipeline (30% faster).

🌱 Nutrition insights powered by Gemini.

🎨 Accessibility support for color-blind users.

📂 Project Structure
backend/        → FastAPI app with routes & ML services  
frontend/       → React Native mobile app (Expo)  
docs/           → Documentation & diagrams  
docker-compose.yml → Deployment-ready setup  

▶️ Getting Started
Backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload

Frontend
cd frontend
npm install
npx expo start

📊 Impact

Improved ML inference speed by 30%.

Enabled color-blind accessibility, empowering more inclusive shopping.

Designed to reduce food waste by helping users shop smarter.