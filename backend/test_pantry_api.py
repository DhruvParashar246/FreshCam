"""
Test script for pantry endpoints.
Run the FastAPI server first: uvicorn app:app --reload
Then run this script: python test_pantry_api.py
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint."""
    print("\n🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_add_item():
    """Test adding items to pantry."""
    print("\n🍌 Testing add banana (stage 5 - very ripe)...")
    
    banana = {
        "fruit_name": "banana",
        "stage": 5,
        "confidence": 0.95,
        "notes": "From grocery store"
    }
    
    response = requests.post(f"{BASE_URL}/pantry/add", json=banana)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201
    
    print("\n🍎 Testing add apple (stage 2 - fresh)...")
    
    apple = {
        "fruit_name": "apple",
        "stage": 2,
        "confidence": 0.92,
        "notes": "Farmer's market"
    }
    
    response = requests.post(f"{BASE_URL}/pantry/add", json=apple)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201
    
    print("\n🥑 Testing add avocado (stage 4 - perfect)...")
    
    avocado = {
        "fruit_name": "avocado",
        "stage": 4,
        "confidence": 0.88,
        "image_path": "/uploads/avocado_123.jpg"
    }
    
    response = requests.post(f"{BASE_URL}/pantry/add", json=avocado)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201


def test_list_items():
    """Test listing all pantry items."""
    print("\n📋 Testing list all items...")
    
    response = requests.get(f"{BASE_URL}/pantry/list")
    print(f"Status: {response.status_code}")
    items = response.json()
    print(f"Found {len(items)} items:")
    for item in items:
        print(f"  - {item['fruit_name']} (stage {item['stage']}) - expires: {item['expiry_date']}")
    assert response.status_code == 200


def test_get_item_by_id():
    """Test getting a specific item."""
    print("\n🔍 Testing get item by ID (ID: 1)...")
    
    response = requests.get(f"{BASE_URL}/pantry/1")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_expiring_soon():
    """Test getting items expiring soon."""
    print("\n⚠️  Testing items expiring within 3 days...")
    
    response = requests.get(f"{BASE_URL}/pantry/expiring/soon?days=3")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_delete_item():
    """Test deleting an item."""
    print("\n🗑️  Testing delete item (ID: 1)...")
    
    response = requests.delete(f"{BASE_URL}/pantry/1")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Verify it's gone
    print("\n🔍 Verifying item is deleted...")
    response = requests.get(f"{BASE_URL}/pantry/1")
    print(f"Status: {response.status_code}")
    assert response.status_code == 404


def run_all_tests():
    """Run all test cases."""
    print("=" * 60)
    print("🧪 FRESHCAM PANTRY API TEST SUITE")
    print("=" * 60)
    
    try:
        test_health_check()
        test_add_item()
        test_list_items()
        test_get_item_by_id()
        test_expiring_soon()
        test_delete_item()
        test_list_items()  # Show final state
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the server.")
        print("Make sure the FastAPI server is running:")
        print("  cd backend")
        print("  uvicorn app:app --reload")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")


if __name__ == "__main__":
    run_all_tests()
