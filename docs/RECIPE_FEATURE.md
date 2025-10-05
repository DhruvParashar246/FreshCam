# Recipe & Food Safety Feature Documentation

## Overview

FreshCam now includes AI-powered recipe suggestions and food safety information to help reduce food waste! Using Google Gemini 2.0 Flash, the app analyzes your fruit and provides:

- 🍳 **Recipe suggestions** optimized for ripeness level
- ✅ **Food safety assessment** (safe to eat or not)
- 📅 **Shelf life estimation** (days until discard)
- 💡 **Storage tips** to maximize freshness

---

## API Endpoints

### 1. `/predict` - Basic + Optional Recipes

**POST** `/predict?include_recipes=true`

Upload a fruit image and get ripeness detection + optional recipe suggestions.

#### Request:
```bash
curl -X POST "http://localhost:8000/predict?include_recipes=true" \
  -F "file=@banana.jpg"
```

#### Response (with `include_recipes=true`):
```json
{
  "fruit_name": "banana",
  "ripeness": "overripe",
  "confidence": 88.5,
  "source": "gemini_primary",
  "is_safe_to_eat": true,
  "days_until_discard": 2,
  "storage_tips": "Store overripe bananas in the freezer for smoothies or baking. They can last months frozen.",
  "recipes": [
    {
      "name": "Banana Bread",
      "difficulty": "easy",
      "prep_time": "15 minutes",
      "cook_time": "60 minutes",
      "why_this_ripeness": "Overripe bananas are perfect for banana bread - they're sweeter and mash easily",
      "ingredients": [
        "3 overripe bananas, mashed",
        "1/3 cup melted butter",
        "1 cup sugar",
        "..."
      ],
      "instructions": "1. Preheat oven to 350°F. 2. Mix butter and mashed bananas..."
    },
    {
      "name": "Banana Smoothie",
      "difficulty": "very easy",
      "prep_time": "3 minutes",
      "cook_time": "0 minutes",
      "why_this_ripeness": "Very ripe bananas add natural sweetness",
      "ingredients": ["2 overripe bananas", "1 cup milk", "..."],
      "instructions": "1. Blend all ingredients..."
    }
  ]
}
```

#### Response (without recipes - default):
```json
{
  "fruit_name": "banana",
  "ripeness": "overripe",
  "confidence": 88.5,
  "source": "gemini_primary"
}
```

---

### 2. `/recipes` - Dedicated Recipe Endpoint

**POST** `/recipes`

Upload a fruit image to get comprehensive recipe and safety information.

#### Request:
```bash
curl -X POST "http://localhost:8000/recipes" \
  -F "file=@strawberry.jpg"
```

#### Response:
```json
{
  "fruit_name": "strawberry",
  "ripeness": "ripe",
  "is_safe_to_eat": true,
  "days_until_discard": 3,
  "storage_tips": "Store unwashed strawberries in the refrigerator. Wash just before eating to prevent mold.",
  "recipes": [
    {
      "name": "Fresh Strawberry Salad",
      "difficulty": "easy",
      "prep_time": "10 minutes",
      "cook_time": "0 minutes",
      "why_this_ripeness": "Ripe strawberries are perfect for fresh eating",
      "ingredients": ["..."],
      "instructions": "..."
    }
  ]
}
```

---

## How It Works

### Flow Diagram

```
User uploads fruit image
        ↓
Gemini identifies fruit name
        ↓
Gemini/CV detects ripeness
        ↓
┌───────────────────────┐
│ If recipes requested  │
└───────────────────────┘
        ↓
Gemini analyzes:
  - Food safety
  - Shelf life
  - Storage tips
  - Recipe suggestions
        ↓
Return comprehensive response
```

### Ripeness-Optimized Recipes

The AI provides different recipes based on ripeness:

| Ripeness | Recipe Type | Examples |
|----------|-------------|----------|
| **Unripe** | Recipes for firm fruits OR ripening tips | Green smoothies, Pickled fruits, How to ripen |
| **Ripe** | Peak freshness recipes | Fresh salads, Fruit tarts, Eating fresh |
| **Overripe** | Waste-reduction recipes | Banana bread, Smoothies, Jams, Baking |

---

## Response Fields

### Core Fields (always included)
- `fruit_name` (string): Name of the fruit
- `ripeness` (string): "unripe", "ripe", or "overripe"
- `confidence` (number): Confidence percentage (0-100)
- `source` (string): "cv_model" or "gemini_primary"

### Recipe Fields (when requested)
- `is_safe_to_eat` (boolean): Whether the fruit is safe to consume
- `days_until_discard` (number): Estimated days before it should be thrown out (0-14)
- `storage_tips` (string): Best practices for storing the fruit
- `recipes` (array): List of recipe objects

### Recipe Object Structure
```json
{
  "name": "Recipe Name",
  "difficulty": "very easy | easy | medium | hard",
  "prep_time": "X minutes",
  "cook_time": "X minutes",
  "why_this_ripeness": "Explanation of why this recipe suits the ripeness",
  "ingredients": ["ingredient 1", "ingredient 2", "..."],
  "instructions": "Step-by-step instructions"
}
```

---

## Food Safety Guidelines

The AI follows these safety criteria:

✅ **Safe to Eat**:
- Firm texture, good color
- Minor bruising or soft spots
- Appropriate ripeness for consumption

❌ **Unsafe to Eat**:
- Visible mold growth
- Rotten smell
- Extensive decay
- Fermented (when unintended)

📅 **Days Until Discard**:
- Conservative estimates for food safety
- Based on current ripeness and typical shelf life
- Assumes proper storage conditions

---

## Use Cases

### 1. **Reduce Food Waste**
"I have overripe bananas - what can I make?"
→ Get banana bread, smoothie, and frozen treat recipes

### 2. **Meal Planning**
"These strawberries are ripe - how long do I have?"
→ Learn you have 3 days and get recipe ideas

### 3. **Food Safety**
"Is this fruit still good to eat?"
→ Get a clear yes/no answer with reasoning

### 4. **Storage Optimization**
"How should I store this to make it last?"
→ Receive specific storage tips

---

## Frontend Integration Examples

### Basic Detection (Fast)
```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/predict', {
  method: 'POST',
  body: formData
});

const data = await response.json();
// { fruit_name, ripeness, confidence }
```

### With Recipes (Comprehensive)
```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/predict?include_recipes=true', {
  method: 'POST',
  body: formData
});

const data = await response.json();
// { fruit_name, ripeness, is_safe_to_eat, recipes, ... }
```

### Dedicated Recipe Endpoint
```javascript
const formData = new FormData();
formData.append('file', imageFile);

const response = await fetch('http://localhost:8000/recipes', {
  method: 'POST',
  body: formData
});

const recipes = await response.json();
// Full recipe and safety information
```

---

## Testing

### Manual Testing
1. Start the backend:
   ```bash
   cd backend
   python app.py
   ```

2. Test with curl:
   ```bash
   # Basic prediction
   curl -X POST http://localhost:8000/predict -F "file=@images/ripe_banana.jpg"
   
   # With recipes
   curl -X POST "http://localhost:8000/predict?include_recipes=true" \
        -F "file=@images/overripe_banana.jpg"
   
   # Dedicated recipes endpoint
   curl -X POST http://localhost:8000/recipes -F "file=@images/ripe_strawberry.jpg"
   ```

3. Use the interactive docs:
   - Go to http://localhost:8000/docs
   - Try the endpoints with the "Try it out" button

---

## Performance Notes

- **Basic prediction**: ~1-2 seconds
- **With recipes**: ~3-5 seconds (additional Gemini API call)
- **Dedicated recipes endpoint**: ~3-5 seconds

Recommendation: Use basic prediction for real-time scanning, fetch recipes on-demand when user wants them.

---

## Error Handling

The API handles errors gracefully:

```json
{
  "error": "Description of what went wrong"
}
```

Common errors:
- No file uploaded
- Empty file
- Gemini API timeout
- Failed to parse response
- Image processing error
