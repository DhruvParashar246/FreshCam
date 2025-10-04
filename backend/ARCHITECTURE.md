# 🏗️ FreshCam Backend Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRESHCAM BACKEND                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Mobile App (React Native)    Browser (Swagger UI)    Postman    │
│         │                            │                    │       │
│         └────────────────────────────┴────────────────────┘       │
│                                │                                  │
│                        HTTP/REST Requests                         │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                      API LAYER (app.py)                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  FastAPI Application                                              │
│  ├─ CORS Middleware (allows frontend access)                     │
│  ├─ Route Registration                                            │
│  └─ Error Handling                                                │
│                                                                   │
│  Endpoints:                                                       │
│  ├─ GET  /                    → Health check                      │
│  ├─ GET  /health              → Detailed status                   │
│  └─ /pantry/*                 → Pantry routes                     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                   ROUTES LAYER (routes/)                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  pantry.py (APIRouter)                                            │
│  ├─ POST   /pantry/add        → Add item to pantry               │
│  ├─ GET    /pantry/list       → Get all items                    │
│  ├─ GET    /pantry/{id}       → Get specific item                │
│  ├─ DELETE /pantry/{id}       → Delete item                      │
│  └─ GET    /pantry/expiring/soon → Items expiring soon           │
│                                                                   │
│  Each route:                                                      │
│  ├─ Validates input (Pydantic)                                   │
│  ├─ Calls model methods                                           │
│  ├─ Handles errors                                                │
│  └─ Returns JSON response                                         │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC (models/)                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  pantry_model.py                                                  │
│                                                                   │
│  Pydantic Models:                                                 │
│  ├─ PantryItemCreate  → Validation for new items                 │
│  └─ PantryItem        → Full item schema                         │
│                                                                   │
│  Shelf Life Map:                                                  │
│  ├─ banana:   stage 1→14d, stage 5→2d                            │
│  ├─ apple:    stage 1→30d, stage 5→3d                            │
│  ├─ avocado:  stage 1→7d,  stage 5→1d                            │
│  ├─ orange:   stage 1→21d, stage 5→3d                            │
│  └─ tomato:   stage 1→14d, stage 5→2d                            │
│                                                                   │
│  Functions:                                                       │
│  └─ calculate_expiry_date(fruit, stage) → ISO datetime           │
│                                                                   │
│  PantryModel Class:                                               │
│  ├─ create_item(item)         → Add to DB                        │
│  ├─ get_all_items()           → List all                         │
│  ├─ get_item_by_id(id)        → Get one                          │
│  ├─ delete_item(id)           → Remove                           │
│  └─ get_expiring_soon(days)   → Filter by date                   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER (db/)                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  db_utils.py                                                      │
│  ├─ get_db_connection()       → Create connection                │
│  ├─ get_db() context manager  → Transaction handling             │
│  ├─ init_db()                 → Create tables                    │
│  ├─ dict_from_row()           → Convert to dict                  │
│  └─ execute_query()           → Run SQL                          │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                     PERSISTENCE LAYER                             │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  pantry_db.sqlite (SQLite Database)                               │
│                                                                   │
│  Table: pantry_items                                              │
│  ├─ id              INTEGER PRIMARY KEY AUTOINCREMENT            │
│  ├─ fruit_name      TEXT NOT NULL                                │
│  ├─ stage           INTEGER NOT NULL (1-6)                       │
│  ├─ confidence      REAL NOT NULL (0.0-1.0)                      │
│  ├─ expiry_date     TEXT NOT NULL (ISO datetime)                 │
│  ├─ added_date      TEXT NOT NULL (ISO datetime)                 │
│  ├─ image_path      TEXT (optional)                              │
│  └─ notes           TEXT (optional)                              │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Example: Adding a Banana

```
1. CLIENT SIDE
   Mobile App captures photo of banana
   CV model predicts: { fruit: "banana", stage: 5, confidence: 0.95 }
   
   ↓ HTTP POST Request
   
2. API LAYER (app.py)
   FastAPI receives request at POST /pantry/add
   CORS middleware allows request
   Routes to pantry.router
   
   ↓ Call route handler
   
3. ROUTES LAYER (pantry.py)
   Validates request body with PantryItemCreate model
   Calls PantryModel.create_item(item)
   
   ↓ Execute business logic
   
4. BUSINESS LOGIC (pantry_model.py)
   calculate_expiry_date("banana", 5)
     → Looks up SHELF_LIFE_MAP["banana"][5] = 2 days
     → Returns "2025-10-06T12:00:00.123456"
   
   Creates item with calculated expiry date
   Calls execute_query() to insert
   
   ↓ Database operation
   
5. DATABASE LAYER (db_utils.py)
   Opens connection with get_db() context manager
   Executes INSERT query
   Commits transaction
   Returns new item ID
   
   ↓ Save to disk
   
6. PERSISTENCE (pantry_db.sqlite)
   Row inserted:
   {
     id: 1,
     fruit_name: "banana",
     stage: 5,
     confidence: 0.95,
     expiry_date: "2025-10-06T12:00:00.123456",
     added_date: "2025-10-04T12:00:00.123456",
     image_path: null,
     notes: null
   }
   
   ↓ Return success
   
7. RESPONSE CHAIN
   db_utils → returns ID
   pantry_model → queries for full item
   pantry.py → wraps in success response
   app.py → sends JSON response
   
   ↓ HTTP 201 Response
   
8. CLIENT RECEIVES
   {
     "success": true,
     "message": "Item added to pantry",
     "item": { ... }
   }
   
   Mobile app updates pantry list
   Shows "Expires in 2 days" warning ⚠️
```

---

## 🔗 Integration Points

### For Dhruv (CV Service)
```python
# In routes/predict.py

from models.pantry_model import PantryModel, PantryItemCreate

@router.post("/predict")
async def predict_freshness(image: UploadFile):
    # 1. Call Roboflow API
    cv_result = roboflow_predict(image)
    
    # 2. Classify stage
    stage = classify_stage(cv_result)
    
    # 3. Save image
    image_path = save_image(image)
    
    # 4. Add to pantry automatically
    pantry_item = PantryItemCreate(
        fruit_name=cv_result['class'],
        stage=stage,
        confidence=cv_result['confidence'],
        image_path=image_path
    )
    
    item_id = PantryModel.create_item(pantry_item)
    
    return {
        "prediction": cv_result,
        "pantry_item_id": item_id
    }
```

### For Rohan (Recipes)
```python
# In routes/recipes.py

from models.pantry_model import PantryModel

@router.get("/recipes/suggested")
async def get_suggested_recipes():
    # Get items expiring in 2 days
    expiring = PantryModel.get_expiring_soon(days=2)
    
    # Get fruit names
    fruits = [item['fruit_name'] for item in expiring]
    
    # Filter recipes
    recipes = filter_recipes_by_ingredients(fruits)
    
    return {
        "expiring_items": expiring,
        "suggested_recipes": recipes
    }
```

### For Krish (Mobile App)
```javascript
// In mobile/api/endpoints.js

export const scanAndAddToP pantry = async (imageUri) => {
  // 1. Upload to /predict
  const formData = new FormData();
  formData.append('image', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'photo.jpg'
  });
  
  const predictResult = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
  });
  
  const data = await predictResult.json();
  
  // Item automatically added to pantry!
  return data.pantry_item_id;
};

export const getPantryDashboard = async () => {
  const items = await fetch('http://localhost:8000/pantry/list');
  return await items.json();
};
```

---

## 📊 Database Schema Visualization

```
pantry_items
┌─────────────┬──────────────┬─────────────┬──────────────────────┐
│     id      │  fruit_name  │    stage    │     confidence       │
│  (INTEGER)  │    (TEXT)    │  (INTEGER)  │       (REAL)         │
│  PRIMARY    │  NOT NULL    │  NOT NULL   │      NOT NULL        │
│     KEY     │              │   (1-6)     │     (0.0-1.0)        │
├─────────────┼──────────────┼─────────────┼──────────────────────┤
│      1      │   "banana"   │      5      │        0.95          │
│      2      │   "apple"    │      2      │        0.92          │
│      3      │  "avocado"   │      4      │        0.88          │
└─────────────┴──────────────┴─────────────┴──────────────────────┘

┌──────────────────────────┬──────────────────────────┬─────────────┬──────────┐
│      expiry_date         │       added_date         │ image_path  │  notes   │
│        (TEXT)            │         (TEXT)           │   (TEXT)    │  (TEXT)  │
│      NOT NULL            │       NOT NULL           │  NULLABLE   │ NULLABLE │
│   (ISO datetime)         │    (ISO datetime)        │             │          │
├──────────────────────────┼──────────────────────────┼─────────────┼──────────┤
│ "2025-10-06T12:00:00"    │ "2025-10-04T12:00:00"    │    null     │   null   │
│ "2025-10-25T11:00:00"    │ "2025-10-04T11:00:00"    │    null     │ "Fresh!" │
│ "2025-10-06T13:30:00"    │ "2025-10-04T13:30:00"    │ "/img/3.jpg"│   null   │
└──────────────────────────┴──────────────────────────┴─────────────┴──────────┘
```

---

## 🎯 Summary

**You built:** A complete 3-layer architecture
1. **Routes** - HTTP endpoints
2. **Models** - Business logic
3. **Database** - Persistence

**It handles:**
- ✅ Input validation
- ✅ Smart expiry calculation
- ✅ CRUD operations
- ✅ Error handling
- ✅ Transaction safety

**It's ready for:**
- ✅ CV integration
- ✅ Frontend consumption
- ✅ Recipe filtering
- ✅ Production deployment

**Great architecture, Farhan! 🏗️**
