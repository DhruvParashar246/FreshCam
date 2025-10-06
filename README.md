# FreshCam

A smart fruit freshness detection app that uses computer vision and AI to identify fruits and determine their ripeness.

## Features

- 🍎 **Fruit Identification**: Uses Google Gemini AI to accurately identify fruit types
- 🎯 **Ripeness Detection**: Computer vision model detects if fruit is unripe, ripe, or overripe
- 🔄 **AI Fallback**: Automatically uses Gemini AI as fallback when CV model fails, ensuring reliable results
- 📱 **Mobile App**: React Native/Expo frontend for easy photo capture
- ⚡ **FastAPI Backend**: High-performance API for image analysis

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```env
ROBOFLOW_URL=https://detect.roboflow.com
ROBOFLOW_API_KEY=your_roboflow_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Get your API keys:
- Roboflow: https://roboflow.com
- Google Gemini: https://makersuite.google.com/app/apikey

4. Run the backend:
```bash
python app.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the app:
```bash
npm start
```

4. Start the app:
```bash
npx expo start --tunnel
```

## How It Works

1. **Take a photo** of a fruit using the mobile app
2. **CV Model analyzes** the image for ripeness
3. **Gemini AI identifies** the fruit name (always)
4. **Fallback mechanism**: If CV model fails, Gemini AI analyzes ripeness
5. **Results returned**: fruit name, ripeness stage, and confidence score

## API Response Format

```json
{
  "fruit_name": "apple",
  "ripeness": "ripe",
  "confidence": 92.5,
  "source": "cv_model"
}
```

- `source` can be: `"cv_model"` or `"gemini_fallback"`
