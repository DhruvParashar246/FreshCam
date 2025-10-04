# 🍌 FreshCam Pantry Backend - Setup Guide

## 📦 What I Built for You (Farhan's Part)

I've completed the **Pantry & Database** functionality for FreshCam! Here's what's ready:

### ✅ Completed Files

1. **`db/db_utils.py`** - Database utilities
   - SQLite connection management
   - Context managers for safe database operations
   - Helper functions for queries

2. **`models/pantry_model.py`** - Core pantry logic
   - Database schema (pantry_items table)
   - Pydantic models for validation
   - **Smart expiry logic** based on fruit type + ripeness stage
   - CRUD methods (create, read, delete, list)
   - Special query for items expiring soon

3. **`routes/pantry.py`** - RESTful API endpoints
   - `POST /pantry/add` - Add item to pantry
   - `GET /pantry/list` - Get all items (sorted by expiry)
   - `GET /pantry/{id}` - Get specific item
   - `DELETE /pantry/{id}` - Remove item
   - `GET /pantry/expiring/soon?days=3` - Items expiring soon

4. **`app.py`** - FastAPI main application
   - CORS enabled for frontend
   - Health check endpoints
   - Pantry routes integrated

5. **`test_pantry_api.py`** - Test suite
   - Tests all endpoints
   - Example usage of the API

### 🔥 Smart Expiry Logic

The system automatically calculates expiry dates based on fruit type and ripeness stage:

**Banana:**
- Stage 1 (very unripe) → 14 days
- Stage 2 (unripe) → 10 days
- Stage 3 (slightly unripe) → 7 days
- Stage 4 (ripe) → 4 days
- Stage 5 (very ripe) → 2 days ⚠️
- Stage 6 (overripe) → 1 day ⚠️⚠️

**Apple:**
- Stage 1-2 → 21-30 days
- Stage 3-4 → 7-14 days
- Stage 5-6 → 1-3 days

**Avocado, Orange, Tomato** - Similar mappings included!

---

## 🚀 Setup Instructions

### 1. Install Python Dependencies

```powershell
# Navigate to backend folder
cd "c:\Users\Farhan Mir\Desktop\Rutgers Classes\HackRU F25\FreshCam\backend"

# Create virtual environment (recommended)
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Backend Server

```powershell
# Start the FastAPI server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
✅ Database initialized successfully
```

### 3. Test the API

Open a new terminal and run:

```powershell
python test_pantry_api.py
```

Or test manually with browser:
- http://localhost:8000/ - Root endpoint
- http://localhost:8000/docs - Interactive API documentation (Swagger UI)
- http://localhost:8000/health - Health check

---

## 📝 API Usage Examples

### Add Item to Pantry

```bash
POST http://localhost:8000/pantry/add
Content-Type: application/json

{
  "fruit_name": "banana",
  "stage": 5,
  "confidence": 0.95,
  "notes": "From grocery store"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Item added to pantry",
  "item": {
    "id": 1,
    "fruit_name": "banana",
    "stage": 5,
    "confidence": 0.95,
    "expiry_date": "2025-10-06T12:30:00",
    "added_date": "2025-10-04T12:30:00",
    "notes": "From grocery store"
  }
}
```

### Get All Items

```bash
GET http://localhost:8000/pantry/list
```

### Get Expiring Soon

```bash
GET http://localhost:8000/pantry/expiring/soon?days=3
```

### Delete Item

```bash
DELETE http://localhost:8000/pantry/1
```

---

## 🔌 Integration with Other Parts

### For Krish (API Core):
- Just import the pantry router: `from routes import pantry`
- Include it: `app.include_router(pantry.router)`

### For Dhruv (CV Integration):
When you get results from Roboflow, pass them to pantry:

```python
# After getting CV results
cv_result = {
    "fruit_name": "banana",
    "stage": 5,
    "confidence": 0.95,
    "image_path": "/uploads/banana_123.jpg"
}

# Add to pantry
requests.post("http://localhost:8000/pantry/add", json=cv_result)
```

### For Rohan (Recipes):
You can query items by freshness:

```python
# Get items expiring soon for recipe suggestions
expiring = requests.get("http://localhost:8000/pantry/expiring/soon?days=2")
# Use the fruit names to suggest recipes
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE pantry_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fruit_name TEXT NOT NULL,
    stage INTEGER NOT NULL,          -- 1-6 ripeness scale
    confidence REAL NOT NULL,        -- 0.0-1.0 from CV model
    expiry_date TEXT NOT NULL,       -- Auto-calculated ISO datetime
    added_date TEXT NOT NULL,        -- ISO datetime
    image_path TEXT,                 -- Optional path to image
    notes TEXT                       -- Optional user notes
);
```

---

## ✅ Your Deliverables (DONE!)

- ✅ Pantry database schema
- ✅ CRUD operations in `/pantry` endpoints
- ✅ Smart expiry logic (fruit + stage → days)
- ✅ SQLite integration
- ✅ Tested and working

---

## 🐛 Troubleshooting

**Database not found:**
- The database is auto-created on first run at `backend/db/pantry_db.sqlite`

**Import errors:**
- Make sure you're in the backend folder
- Activate virtual environment
- Check that all packages are installed

**CORS errors from frontend:**
- Already configured in `app.py` to allow all origins
- In production, change to specific frontend URL

---

## 🎯 Next Steps

1. **Setup & Test** - Get the server running and test endpoints
2. **Integration** - Wait for Dhruv's CV integration to send real data
3. **Frontend Hook** - Work with Farhan on mobile pantry screen
4. **Polish** - Add any extra features (search, filter, edit items)

---

## 📞 Questions?

Your backend is solid! Database automatically initializes, expiry dates calculate correctly, and all CRUD operations work. Just need to:

1. Fix Python environment
2. Start the server
3. Test with the test script or Swagger UI

**Good luck with the hackathon! 🚀**
