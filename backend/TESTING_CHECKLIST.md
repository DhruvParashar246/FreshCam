# ✅ FreshCam Backend - Testing Checklist

## 🎯 Pre-Launch Checklist

### Environment Setup
- [ ] Python 3.7+ installed
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] No import errors when starting server

### Database
- [ ] `pantry_db.sqlite` created automatically on first run
- [ ] Database initialized successfully (check console output)
- [ ] Can view database file in `backend/db/` folder

### Server Startup
- [ ] Server starts without errors
- [ ] Running on http://0.0.0.0:8000
- [ ] No port conflicts
- [ ] Auto-reload working (saves trigger restart)

### API Endpoints (via Browser)
Visit http://localhost:8000/docs (Swagger UI)

- [ ] `/` - Root endpoint returns version info
- [ ] `/health` - Returns healthy status
- [ ] `/pantry/add` - Can add item via Swagger UI
- [ ] `/pantry/list` - Returns array of items
- [ ] `/pantry/{id}` - Returns single item
- [ ] `/pantry/{id}` (DELETE) - Deletes item
- [ ] `/pantry/expiring/soon` - Returns filtered items

### Functional Testing
- [ ] Add banana (stage 5) - calculates 2 day expiry
- [ ] Add apple (stage 2) - calculates 21 day expiry
- [ ] Add avocado (stage 4) - calculates 2 day expiry
- [ ] List all items - shows 3 items
- [ ] Get item by ID - returns correct item
- [ ] Get expiring soon (3 days) - shows banana & avocado
- [ ] Delete banana - removes from list
- [ ] List all - now shows 2 items

### Error Handling
- [ ] Get non-existent item (ID 999) - returns 404
- [ ] Delete non-existent item - returns 404
- [ ] Invalid fruit name - still works (uses default)
- [ ] Invalid stage (0 or 7) - still works (uses default 3 days)
- [ ] Missing required fields - returns validation error

### Data Validation
- [ ] Expiry dates are in future
- [ ] Expiry dates match expected shelf life
- [ ] Added dates are current time
- [ ] Confidence values are 0.0-1.0
- [ ] Stage values are 1-6
- [ ] All dates are ISO format

### Integration Points
- [ ] CORS allows requests from frontend
- [ ] JSON responses are properly formatted
- [ ] Error messages are clear and helpful
- [ ] HTTP status codes are correct (200, 201, 404, 500)

### Documentation
- [ ] README is clear and complete
- [ ] API reference is accurate
- [ ] Code examples work
- [ ] Architecture diagram makes sense

### Performance
- [ ] Requests respond quickly (< 100ms)
- [ ] Database queries are efficient
- [ ] No memory leaks during testing
- [ ] Can handle multiple concurrent requests

---

## 🧪 Test Script Checklist

Run: `python test_pantry_api.py`

Expected output:
```
🧪 FRESHCAM PANTRY API TEST SUITE
==================================================
🔍 Testing health check...
Status: 200
✓ Health check passed

🍌 Testing add banana (stage 5 - very ripe)...
Status: 201
✓ Banana added

🍎 Testing add apple (stage 2 - fresh)...
Status: 201
✓ Apple added

🥑 Testing add avocado (stage 4 - perfect)...
Status: 201
✓ Avocado added

📋 Testing list all items...
Status: 200
Found 3 items
✓ List items passed

🔍 Testing get item by ID (ID: 1)...
Status: 200
✓ Get item passed

⚠️ Testing items expiring within 3 days...
Status: 200
✓ Expiring items query passed

🗑️ Testing delete item (ID: 1)...
Status: 200
✓ Delete passed

🔍 Verifying item is deleted...
Status: 404
✓ Verification passed

==================================================
✅ ALL TESTS PASSED!
==================================================
```

- [ ] All tests pass
- [ ] No errors or warnings
- [ ] Response times acceptable
- [ ] Data is correct

---

## 🎬 Demo Script Checklist

Run: `python demo_pantry.py`

Expected behavior:
- [ ] Adds 5 items (banana, apple, avocado, orange, tomato)
- [ ] Shows all items with expiry dates
- [ ] Highlights items expiring soon
- [ ] Shows correct days remaining
- [ ] Displays item details
- [ ] Shows expiry calculation examples
- [ ] Deletes overripe tomato
- [ ] Shows updated pantry count
- [ ] Displays statistics

Expected statistics:
- [ ] Total items: 4 (after deleting tomato)
- [ ] Expiring soon: 2-3 items
- [ ] Fruit types: ["banana", "apple", "avocado", "orange"]
- [ ] Average confidence: ~0.90

---

## 🔧 Manual Testing Steps

### Test 1: Add Item
```bash
curl -X POST http://localhost:8000/pantry/add \
  -H "Content-Type: application/json" \
  -d '{
    "fruit_name": "banana",
    "stage": 5,
    "confidence": 0.95,
    "notes": "Test banana"
  }'
```

Expected: 201 response with item details

### Test 2: List Items
```bash
curl http://localhost:8000/pantry/list
```

Expected: Array with 1+ items

### Test 3: Get Specific Item
```bash
curl http://localhost:8000/pantry/1
```

Expected: Single item object

### Test 4: Get Expiring Soon
```bash
curl "http://localhost:8000/pantry/expiring/soon?days=3"
```

Expected: Object with threshold_days, count, and items array

### Test 5: Delete Item
```bash
curl -X DELETE http://localhost:8000/pantry/1
```

Expected: Success message

### Test 6: Verify Deletion
```bash
curl http://localhost:8000/pantry/1
```

Expected: 404 error

---

## 🐛 Troubleshooting Checklist

### Server Won't Start
- [ ] Check Python version (3.7+)
- [ ] Verify virtual environment activated
- [ ] Install dependencies again
- [ ] Check port 8000 not in use
- [ ] Look for syntax errors in code

### Import Errors
- [ ] Activate virtual environment
- [ ] Run `pip install -r requirements.txt`
- [ ] Check Python path
- [ ] Restart terminal/IDE

### Database Errors
- [ ] Check `db/pantry_db.sqlite` exists
- [ ] Delete database file and restart (recreates)
- [ ] Check file permissions
- [ ] Verify SQLite installed

### API Errors
- [ ] Check request format (JSON)
- [ ] Verify Content-Type header
- [ ] Check required fields present
- [ ] Review error message
- [ ] Check server logs

### CORS Errors (from frontend)
- [ ] Verify CORS middleware in app.py
- [ ] Check allow_origins setting
- [ ] Use correct URL (http://localhost:8000)
- [ ] Check browser console for details

---

## 📝 Pre-Demo Checklist

### 1 Hour Before Demo
- [ ] Server is running
- [ ] Database is populated with example data
- [ ] All endpoints tested
- [ ] Swagger UI loads correctly
- [ ] No errors in console

### 30 Minutes Before
- [ ] Clear old data (optional fresh start)
- [ ] Add 3-5 example items with varied stages
- [ ] Test complete flow (add → list → delete)
- [ ] Prepare talking points

### 5 Minutes Before
- [ ] Server is responding
- [ ] Swagger UI is open in browser
- [ ] Example cURL commands ready
- [ ] Team knows their integration points

### During Demo
- [ ] Show Swagger UI documentation
- [ ] Add item via API (show expiry calculation)
- [ ] List items (show sorting by expiry)
- [ ] Show expiring soon feature
- [ ] Explain integration points

---

## 🎯 Integration Ready Checklist

### For Dhruv (CV)
- [ ] Shared API documentation
- [ ] Explained PantryItemCreate model
- [ ] Showed how to add items after CV prediction
- [ ] Tested with mock CV data

### For Krish (Mobile)
- [ ] Shared API endpoints list
- [ ] Provided JavaScript/React Native examples
- [ ] Explained response formats
- [ ] Tested CORS from mobile simulator

### For Rohan (Recipes)
- [ ] Explained get_expiring_soon() method
- [ ] Showed how to query pantry items
- [ ] Discussed recipe filtering logic
- [ ] Tested recipe API integration

---

## ✅ Final Sign-Off

Before marking "DONE":

- [ ] ✅ All core endpoints working
- [ ] ✅ All tests passing
- [ ] ✅ Documentation complete
- [ ] ✅ Team briefed on integration
- [ ] ✅ Demo prepared
- [ ] ✅ Code committed to repo
- [ ] ✅ Ready for hackathon presentation

---

## 🏆 Success Criteria

You're ready when:

1. **Server runs cleanly** - No errors, starts on localhost:8000
2. **All endpoints work** - Can add, list, get, delete items
3. **Expiry logic works** - Dates calculate correctly by fruit+stage
4. **Tests pass** - test_pantry_api.py succeeds
5. **Demo ready** - Can show live API in Swagger UI
6. **Team ready** - Others know how to integrate

---

**When all boxes checked → You're done! 🎉**

**Go help the team with frontend/integration!**
