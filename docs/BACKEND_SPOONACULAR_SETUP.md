# FreshCam Backend - Spoonacular Integration

## What's New 🎉

The backend now has full **Spoonacular Food API** integration for smart recipe recommendations based on your pantry items!

### Features Added:

1. **Smart Pantry System**
   - Automatically saves scanned items with freshness data
   - Tracks ripeness stage (1-6 scale)
   - Calculates days until expiry
   - Shows which items are expiring soon

2. **Recipe Recommendations**
   - Get recipes based on what's in your pantry
   - Prioritizes items that are ripe or expiring soon
   - Uses Spoonacular's 500,000+ recipe database

3. **Auto-Save on Scan**
   - When you scan an avocado, it's automatically added to your pantry
   - Tracks: "avocado, stage 5, 3 days left"

---

## Setup Instructions

### 1. Get Spoonacular API Key (FREE!)

1. Go to https://spoonacular.com/food-api/console#Dashboard
2. Sign up for a free account
3. Copy your API key (you get **150 free requests/day**)

### 2. Configure Backend

Edit `backend/.env` and add your Spoonacular API key:

```env
ROBOFLOW_API_KEY=JrQNqqw3Sj1wzWj842i9
ROBOFLOW_URL=https://detect.roboflow.com

# Add your Spoonacular API key here:
SPOONACULAR_API_KEY=your_api_key_here
```

### 3. Install Dependencies

```bash
cd backend
..\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start the Backend

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

## API Endpoints

### 1. **POST /predict/** - Scan Food
Upload an image to analyze freshness and auto-save to pantry

**Query Parameters:**
- `auto_save` (bool, default=True): Automatically add to pantry

**Response:**
```json
{
  "item_name": "avocado",
  "freshness_stage": 5,
  "ripeness": "ripe",
  "confidence": 95.5,
  "saved_to_pantry": true,
  "pantry_item": {
    "id": 1,
    "name": "avocado",
    "freshness_stage": 5,
    "days_left": 3,
    "added_date": "2025-10-04",
    "expiry_date": "2025-10-07"
  }
}
```

---

### 2. **GET /pantry/** - View Pantry
Get all items in your pantry

**Response:**
```json
{
  "total_items": 3,
  "items": [
    {
      "id": 1,
      "name": "avocado",
      "freshness_stage": 5,
      "days_left": 3,
      "added_date": "2025-10-04",
      "expiry_date": "2025-10-07"
    }
  ]
}
```

---

### 3. **GET /pantry/expiring?days=3** - Expiring Soon
Get items expiring within N days

**Response:**
```json
{
  "expiring_count": 2,
  "days_threshold": 3,
  "items": [
    {
      "id": 2,
      "name": "banana",
      "freshness_stage": 6,
      "days_left": 1
    }
  ]
}
```

---

### 4. **GET /recipes/recommendations?number=10** - Get Recipes
Get recipe recommendations based on pantry items

**Query Parameters:**
- `number` (int, default=10): Number of recipes to return
- `days_threshold` (int, default=3): Prioritize items expiring within N days

**Response:**
```json
{
  "recipes": [
    {
      "id": 654959,
      "title": "Avocado Toast with Fried Egg",
      "image": "https://spoonacular.com/...",
      "usedIngredients": [
        {"name": "avocado", "amount": 1}
      ],
      "missedIngredients": [
        {"name": "bread", "amount": 2}
      ],
      "urgency_score": 1
    }
  ],
  "pantry_summary": {
    "total_items": 3,
    "expiring_soon": 2,
    "expiring_items": [
      {"name": "avocado", "days_left": 3, "freshness_stage": 5}
    ]
  }
}
```

---

### 5. **GET /recipes/by-ingredients?ingredients=avocado,banana** - Search Recipes
Search recipes by specific ingredients

**Response:**
```json
{
  "recipes": [...],
  "searched_ingredients": ["avocado", "banana"]
}
```

---

### 6. **GET /recipes/{recipe_id}** - Recipe Details
Get detailed information about a specific recipe

**Response:**
```json
{
  "id": 654959,
  "title": "Avocado Toast",
  "readyInMinutes": 10,
  "servings": 2,
  "instructions": "...",
  "extendedIngredients": [...]
}
```

---

### 7. **PATCH /pantry/{item_id}/consume** - Mark as Used
Mark an item as consumed

**Response:**
```json
{
  "message": "Item marked as consumed",
  "item_id": 1
}
```

---

### 8. **DELETE /pantry/{item_id}** - Remove Item
Delete an item from pantry

**Response:**
```json
{
  "message": "Item deleted from pantry",
  "item_id": 1
}
```

---

## How It Works

### Freshness Stage → Days Left Mapping

| Stage | Ripeness Level | Estimated Days Left |
|-------|----------------|---------------------|
| 1     | Unripe         | 14 days             |
| 2     | Slightly Unripe| 10 days             |
| 3     | Perfect        | 7 days              |
| 4     | Slightly Ripe  | 5 days              |
| 5     | Ripe           | 3 days              |
| 6     | Overripe       | 1 day               |

### Recipe Recommendation Logic

1. **Prioritizes Urgent Items**: Items with stage 5-6 or ≤3 days left
2. **Calculates Urgency Score**: How many urgent ingredients each recipe uses
3. **Sorts by Urgency**: Recipes using more expiring items appear first

### Example Workflow:

1. **Scan avocado** → Auto-saved as "avocado, stage 5, 3 days left"
2. **Scan banana** → Auto-saved as "banana, stage 6, 1 day left"
3. **Get recommendations** → Returns recipes like:
   - "Avocado Banana Smoothie" (urgency: 2) ⭐
   - "Guacamole" (urgency: 1)
   - "Banana Bread" (urgency: 1)

---

## Testing the API

### Option 1: Swagger UI
Visit http://localhost:8000/docs for interactive API testing

### Option 2: curl Examples

**Scan an item:**
```bash
curl -X POST "http://localhost:8000/predict/?auto_save=true" \
  -F "file=@path/to/image.jpg"
```

**Get pantry:**
```bash
curl http://localhost:8000/pantry/
```

**Get recipe recommendations:**
```bash
curl http://localhost:8000/recipes/recommendations?number=5
```

---

## Database Schema

The pantry database (`backend/db/pantry_db.sqlite`) has this structure:

```sql
CREATE TABLE pantry_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    freshness_stage INTEGER NOT NULL,
    confidence REAL,
    days_left INTEGER,
    added_date TEXT NOT NULL,
    expiry_date TEXT,
    image_path TEXT,
    consumed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## Files Added/Modified

### New Files:
- `backend/services/spoonacular_service.py` - Spoonacular API integration
- `backend/db/db_utils.py` - Pantry database utilities
- `backend/models/pantry_model.py` - Pydantic models
- `backend/.env` - Environment configuration

### Modified Files:
- `backend/app.py` - Added recipes router + CORS
- `backend/routes/predict.py` - Auto-save to pantry
- `backend/routes/pantry.py` - Full pantry CRUD
- `backend/routes/recipes.py` - Recipe endpoints
- `backend/services/cv_service.py` - Enhanced to return item name + stage
- `backend/requirements.txt` - Added python-dotenv

---

## Next Steps for Mobile App

To integrate with the mobile app, you'll need to:

1. **Update API calls** to use the new response format
2. **Add pantry screen** to view saved items
3. **Add recipes screen** to show recommendations
4. **Show days left** on each scanned item

Example mobile API call:
```javascript
const response = await axios.post(
  `${BASE_URL}/predict/`,
  formData,
  { params: { auto_save: true } }
);

console.log(response.data.pantry_item.days_left); // "3 days left"
```

---

## Troubleshooting

### "SPOONACULAR_API_KEY not found"
- Make sure you added your API key to `.env`
- Restart the backend server

### "Failed to fetch recipes"
- Check your API key is valid
- Check you haven't exceeded the 150 requests/day limit
- Check your internet connection

### "No items in pantry"
- Scan some food first using POST /predict/
- Or manually add items using POST /pantry/

---

Enjoy your smart pantry! 🥑🍌🍎
