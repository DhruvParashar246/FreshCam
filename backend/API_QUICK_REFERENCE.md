# 🔥 QUICK REFERENCE - Pantry API Endpoints

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1️⃣ Add Item to Pantry
```http
POST /pantry/add
```

**Request Body:**
```json
{
  "fruit_name": "banana",
  "stage": 5,
  "confidence": 0.95,
  "image_path": "/uploads/banana.jpg",  // optional
  "notes": "From store"                 // optional
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Item added to pantry",
  "item": {
    "id": 1,
    "fruit_name": "banana",
    "stage": 5,
    "confidence": 0.95,
    "expiry_date": "2025-10-06T10:30:00.123456",
    "added_date": "2025-10-04T10:30:00.123456",
    "image_path": "/uploads/banana.jpg",
    "notes": "From store"
  }
}
```

---

### 2️⃣ List All Items
```http
GET /pantry/list
```

**Response (200):**
```json
[
  {
    "id": 1,
    "fruit_name": "banana",
    "stage": 5,
    "confidence": 0.95,
    "expiry_date": "2025-10-06T10:30:00.123456",
    "added_date": "2025-10-04T10:30:00.123456",
    "image_path": null,
    "notes": null
  },
  {
    "id": 2,
    "fruit_name": "apple",
    "stage": 2,
    "confidence": 0.92,
    "expiry_date": "2025-10-25T11:00:00.123456",
    "added_date": "2025-10-04T11:00:00.123456",
    "image_path": null,
    "notes": "Farmer's market"
  }
]
```

---

### 3️⃣ Get Single Item
```http
GET /pantry/{item_id}
```

**Example:**
```http
GET /pantry/1
```

**Response (200):**
```json
{
  "id": 1,
  "fruit_name": "banana",
  "stage": 5,
  "confidence": 0.95,
  "expiry_date": "2025-10-06T10:30:00.123456",
  "added_date": "2025-10-04T10:30:00.123456",
  "image_path": null,
  "notes": null
}
```

**Response (404):**
```json
{
  "detail": "Item with ID 999 not found"
}
```

---

### 4️⃣ Delete Item
```http
DELETE /pantry/{item_id}
```

**Example:**
```http
DELETE /pantry/1
```

**Response (200):**
```json
{
  "success": true,
  "message": "Item 1 deleted successfully"
}
```

**Response (404):**
```json
{
  "detail": "Item with ID 999 not found"
}
```

---

### 5️⃣ Get Expiring Soon
```http
GET /pantry/expiring/soon?days={threshold}
```

**Example:**
```http
GET /pantry/expiring/soon?days=3
```

**Response (200):**
```json
{
  "threshold_days": 3,
  "count": 2,
  "items": [
    {
      "id": 1,
      "fruit_name": "banana",
      "stage": 5,
      "confidence": 0.95,
      "expiry_date": "2025-10-06T10:30:00.123456",
      "added_date": "2025-10-04T10:30:00.123456",
      "image_path": null,
      "notes": null
    },
    {
      "id": 3,
      "fruit_name": "avocado",
      "stage": 4,
      "confidence": 0.88,
      "expiry_date": "2025-10-06T12:00:00.123456",
      "added_date": "2025-10-04T12:00:00.123456",
      "image_path": null,
      "notes": null
    }
  ]
}
```

---

### 6️⃣ Health Check
```http
GET /health
```

**Response (200):**
```json
{
  "status": "healthy",
  "services": {
    "pantry": "active",
    "database": "connected"
  }
}
```

---

## 🎯 Ripeness Stages

| Stage | Description | Banana Example | Days Left |
|-------|-------------|----------------|-----------|
| 1 | Very unripe | Green | 14 days |
| 2 | Unripe | Mostly green | 10 days |
| 3 | Slightly unripe | Yellow-green | 7 days |
| 4 | Ripe | Yellow | 4 days |
| 5 | Very ripe | Yellow with spots | 2 days ⚠️ |
| 6 | Overripe | Brown spots | 1 day ⚠️⚠️ |

---

## 🧪 cURL Test Commands

```bash
# Health check
curl http://localhost:8000/health

# Add banana
curl -X POST http://localhost:8000/pantry/add \
  -H "Content-Type: application/json" \
  -d '{"fruit_name":"banana","stage":5,"confidence":0.95}'

# List all
curl http://localhost:8000/pantry/list

# Get item 1
curl http://localhost:8000/pantry/1

# Get expiring soon
curl "http://localhost:8000/pantry/expiring/soon?days=3"

# Delete item 1
curl -X DELETE http://localhost:8000/pantry/1
```

---

## 📱 JavaScript/React Native Example

```javascript
// api/endpoints.js
const BASE_URL = 'http://localhost:8000';

export const addToPantry = async (item) => {
  const response = await fetch(`${BASE_URL}/pantry/add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item)
  });
  return response.json();
};

export const getPantryItems = async () => {
  const response = await fetch(`${BASE_URL}/pantry/list`);
  return response.json();
};

export const getExpiringSoon = async (days = 3) => {
  const response = await fetch(`${BASE_URL}/pantry/expiring/soon?days=${days}`);
  return response.json();
};

export const deleteItem = async (id) => {
  const response = await fetch(`${BASE_URL}/pantry/${id}`, {
    method: 'DELETE'
  });
  return response.json();
};
```

---

## 🚀 Interactive API Docs

Once server is running, visit:

**Swagger UI:** http://localhost:8000/docs

Try all endpoints interactively with a nice UI! 🎨
