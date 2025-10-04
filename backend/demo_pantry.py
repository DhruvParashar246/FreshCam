"""
Example usage of the Pantry API - can be run standalone
"""

from models.pantry_model import PantryModel, PantryItemCreate, calculate_expiry_date
from datetime import datetime
import json


def pretty_print(title, data):
    """Helper to print formatted output."""
    print("\n" + "="*60)
    print(f"📋 {title}")
    print("="*60)
    print(json.dumps(data, indent=2, default=str))


def demo_pantry_system():
    """Demonstrate the pantry system functionality."""
    
    print("\n🍌 FRESHCAM PANTRY SYSTEM DEMO")
    print("="*60)
    
    # 1. Add some items
    print("\n1️⃣ Adding items to pantry...")
    
    items_to_add = [
        {
            "fruit_name": "banana",
            "stage": 5,
            "confidence": 0.95,
            "notes": "Very ripe, use soon!"
        },
        {
            "fruit_name": "apple",
            "stage": 2,
            "confidence": 0.92,
            "notes": "Fresh from farmer's market"
        },
        {
            "fruit_name": "avocado",
            "stage": 4,
            "confidence": 0.88,
            "notes": "Perfect for guacamole"
        },
        {
            "fruit_name": "orange",
            "stage": 3,
            "confidence": 0.90,
            "notes": "Good for juice"
        },
        {
            "fruit_name": "tomato",
            "stage": 6,
            "confidence": 0.85,
            "notes": "Overripe, make sauce today!"
        }
    ]
    
    added_ids = []
    for item_data in items_to_add:
        item = PantryItemCreate(**item_data)
        item_id = PantryModel.create_item(item)
        added_ids.append(item_id)
        print(f"   ✅ Added {item_data['fruit_name']} (stage {item_data['stage']}) - ID: {item_id}")
    
    # 2. List all items
    print("\n2️⃣ Listing all pantry items...")
    all_items = PantryModel.get_all_items()
    
    print(f"\n   Found {len(all_items)} items in pantry:")
    for item in all_items:
        expiry = datetime.fromisoformat(item['expiry_date'])
        days_left = (expiry - datetime.now()).days
        urgency = "🔴" if days_left <= 1 else "🟡" if days_left <= 3 else "🟢"
        
        print(f"   {urgency} [{item['id']}] {item['fruit_name'].title()} "
              f"(stage {item['stage']}) - expires in {days_left} days")
    
    # 3. Get items expiring soon
    print("\n3️⃣ Items expiring within 3 days...")
    expiring = PantryModel.get_expiring_soon(days=3)
    
    if expiring:
        print(f"\n   ⚠️  WARNING: {len(expiring)} items need attention!")
        for item in expiring:
            print(f"   - {item['fruit_name'].title()} (ID: {item['id']})")
            print(f"     Stage: {item['stage']}, Confidence: {item['confidence']}")
            print(f"     Expires: {item['expiry_date']}")
            if item['notes']:
                print(f"     Note: {item['notes']}")
    else:
        print("   ✅ No items expiring soon!")
    
    # 4. Get specific item details
    print("\n4️⃣ Getting details for item ID 1...")
    item = PantryModel.get_item_by_id(1)
    if item:
        pretty_print("Item Details", item)
    
    # 5. Show expiry calculation logic
    print("\n5️⃣ Expiry calculation examples...")
    print("\n   How long will these last?")
    
    test_cases = [
        ("banana", 1, "Very unripe banana"),
        ("banana", 5, "Very ripe banana"),
        ("apple", 2, "Fresh apple"),
        ("avocado", 4, "Perfect avocado"),
        ("tomato", 6, "Overripe tomato"),
    ]
    
    for fruit, stage, description in test_cases:
        expiry = calculate_expiry_date(fruit, stage)
        expiry_date = datetime.fromisoformat(expiry)
        days = (expiry_date - datetime.now()).days
        
        print(f"   - {description} (stage {stage}): {days} days")
    
    # 6. Delete an item
    print("\n6️⃣ Deleting the overripe tomato (should be used already)...")
    if added_ids:
        deleted_id = added_ids[-1]  # Delete the last one (tomato)
        PantryModel.delete_item(deleted_id)
        print(f"   ✅ Deleted item {deleted_id}")
        
        # Show updated list
        updated_items = PantryModel.get_all_items()
        print(f"   Now have {len(updated_items)} items remaining")
    
    # 7. Summary stats
    print("\n7️⃣ Pantry Summary...")
    remaining_items = PantryModel.get_all_items()
    expiring_soon = PantryModel.get_expiring_soon(days=3)
    
    stats = {
        "total_items": len(remaining_items),
        "expiring_soon": len(expiring_soon),
        "fruit_types": list(set([item['fruit_name'] for item in remaining_items])),
        "average_confidence": round(
            sum([item['confidence'] for item in remaining_items]) / len(remaining_items), 2
        ) if remaining_items else 0
    }
    
    pretty_print("Pantry Statistics", stats)
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE!")
    print("="*60)


if __name__ == "__main__":
    print("\n🚀 Starting Pantry System Demo...")
    print("This will add, list, and manage items in your pantry database.")
    print("\nPress Ctrl+C to cancel, or Enter to continue...")
    
    try:
        input()
        demo_pantry_system()
        
        print("\n💡 Next steps:")
        print("   1. Start the API server: uvicorn app:app --reload")
        print("   2. Visit http://localhost:8000/docs for interactive API")
        print("   3. Run test_pantry_api.py for full endpoint testing")
        
    except KeyboardInterrupt:
        print("\n\n❌ Demo cancelled.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
