# Development Guide - When to Restart

## 📋 Quick Answer

### Backend Changes → **YES, RESTART REQUIRED** ✅
### Frontend Changes → **NO, AUTO-RELOADS** ⚡ (with Expo/Metro)

---

## Backend (Python/FastAPI)

### ✅ **RESTART REQUIRED** when you change:
- ✅ Python files (`.py`)
- ✅ Routes (`routes/*.py`)
- ✅ Services (`services/*.py`)
- ✅ `app.py`
- ✅ Environment variables (`.env`)
- ✅ Dependencies (`requirements.txt` - also need to reinstall)

### How to Restart Backend:

#### Option 1: Stop and Start (Recommended)
```bash
# In the terminal running the backend:
Press Ctrl+C to stop

# Then restart:
cd backend
python app.py
```

#### Option 2: Kill by Port (if stuck)
```powershell
# Find process on port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual number)
taskkill /PID <PID> /F

# Restart
cd backend
python app.py
```

### Backend is Running When You See:
```
⚠️ Roboflow API key not configured - will use Gemini for all predictions
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## Frontend (React Native/Expo)

### ⚡ **NO RESTART NEEDED** - Auto-reloads for:
- ⚡ TypeScript/JavaScript files (`.ts`, `.tsx`, `.js`)
- ⚡ Components
- ⚡ Screens/Routes
- ⚡ Styles
- ⚡ Most configuration changes

Metro bundler watches for changes and **hot reloads automatically**!

### ⚠️ **RESTART RECOMMENDED** for:
- Configuration files (`app.json`, `package.json`)
- Native dependencies (after `npm install`)
- Major structural changes

### How to Restart Frontend:

#### If Already Running:
```bash
# In the Expo terminal:
Press 'r' to reload
# OR
Press Ctrl+C to stop, then:
npx expo start --tunnel
```

#### Fresh Start:
```bash
cd frontend
npx expo start --tunnel
```

### Frontend is Running When You See:
```
Starting Metro Bundler
Tunnel connected.
Tunnel ready.
[QR CODE]
› Metro waiting on exp://...
```

---

## Common Scenarios

### 1️⃣ "I added a new API endpoint"
- ✅ **Backend**: Restart required
- ⚡ **Frontend**: No restart (unless you change config)

**Steps:**
1. Stop backend (Ctrl+C)
2. Restart: `python app.py`
3. Frontend auto-reloads when you save files

---

### 2️⃣ "I changed a UI component"
- ✅ **Backend**: No action needed
- ⚡ **Frontend**: Automatically reloads!

**Steps:**
1. Just save the file
2. Metro detects changes and reloads
3. Check your phone - should update automatically

---

### 3️⃣ "I updated environment variables (.env)"
- ✅ **Backend**: Restart required
- ⚡ **Frontend**: Usually no restart (unless env vars used in app.json)

**Steps:**
1. Update `.env` file
2. Stop backend (Ctrl+C)
3. Restart: `python app.py`

---

### 4️⃣ "I installed a new npm package"
- ✅ **Backend**: No action needed
- ⚡ **Frontend**: Restart Expo

**Steps:**
```bash
cd frontend
npm install <package>
# Stop Expo (Ctrl+C)
npx expo start --tunnel
```

---

### 5️⃣ "I installed a new Python package"
- ✅ **Backend**: Restart required
- ⚡ **Frontend**: No action needed

**Steps:**
```bash
cd backend
pip install <package>
# Add to requirements.txt if not already there
# Stop backend (Ctrl+C)
python app.py
```

---

### 6️⃣ "App is stuck or not responding"

#### Backend Issues:
```bash
# Check if backend is running:
curl http://localhost:8000/

# If no response, restart backend
cd backend
python app.py
```

#### Frontend Issues:
```bash
# In Expo terminal:
Press 'r' to reload

# If that doesn't work:
Press Ctrl+C
npx expo start --tunnel --clear  # Clear cache
```

---

## 🎯 Pro Tips

### Backend Development
1. **Keep the terminal visible** - watch for errors in real-time
2. **Check logs** - errors appear in the terminal where you ran `python app.py`
3. **Test endpoints** - Use http://localhost:8000/docs for interactive testing
4. **Port conflicts** - If port 8000 is busy, kill the process or change port

### Frontend Development
1. **Hot reload is your friend** - Save files and changes appear instantly
2. **Shake phone** - Opens dev menu on physical device
3. **Press 'r'** - Manually reload if something seems off
4. **Clear cache** - If weird bugs: `npx expo start --clear`

---

## Current Project Setup

### Backend Running:
- **URL**: `http://localhost:8000` or `http://0.0.0.0:8000`
- **API Docs**: http://localhost:8000/docs
- **Endpoints**: `/predict`, `/recipes`

### Frontend Running:
- **Mode**: Tunnel (for network reliability)
- **Access**: Scan QR code with Expo Go app
- **Hot Reload**: Enabled automatically

---

## Emergency Restart (Everything)

If nothing works, full restart:

```bash
# Terminal 1 - Backend
cd backend
# Ctrl+C if running
python app.py

# Terminal 2 - Frontend  
cd frontend
# Ctrl+C if running
npx expo start --tunnel --clear
```

Wait for both to fully start, then test!

---

## Summary Table

| Change Type | Backend Restart? | Frontend Restart? |
|-------------|------------------|-------------------|
| Python code | ✅ YES | ❌ NO |
| Routes/Services | ✅ YES | ❌ NO |
| .env file | ✅ YES | ❌ NO |
| TypeScript/JSX | ❌ NO | ⚡ Auto-reload |
| Components | ❌ NO | ⚡ Auto-reload |
| Styles | ❌ NO | ⚡ Auto-reload |
| package.json | ❌ NO | ✅ YES |
| requirements.txt | ✅ YES (+ reinstall) | ❌ NO |
| app.json | ❌ NO | ⚠️ Recommended |

✅ = Restart required
⚡ = Automatic reload
❌ = No action needed
⚠️ = Recommended but not always required
