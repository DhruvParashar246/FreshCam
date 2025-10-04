from datetime import datetime, timedelta
from typing import Optional, Dict, List
from pydantic import BaseModel
from db.db_utils import execute_query, init_db


# Pydantic models for validation
class PantryItemCreate(BaseModel):
    fruit_name: str
    stage: int
    confidence: float
    image_path: Optional[str] = None
    notes: Optional[str] = None


class PantryItem(BaseModel):
    id: int
    fruit_name: str
    stage: int
    confidence: float
    expiry_date: str
    added_date: str
    image_path: Optional[str] = None
    notes: Optional[str] = None


# Shelf life mapping: {fruit_name: {stage: days_until_expiry}}
SHELF_LIFE_MAP = {
    "banana": {
        1: 14,  # Very unripe - 2 weeks
        2: 10,  # Unripe - 10 days
        3: 7,   # Slightly unripe - 1 week
        4: 4,   # Ripe - 4 days
        5: 2,   # Very ripe - 2 days
        6: 1,   # Overripe - 1 day
    },
    "apple": {
        1: 30,  # Very fresh - 1 month
        2: 21,  # Fresh - 3 weeks
        3: 14,  # Good - 2 weeks
        4: 7,   # Ripe - 1 week
        5: 3,   # Soft - 3 days
        6: 1,   # Bad spots - 1 day
    },
    "avocado": {
        1: 7,   # Hard - 1 week
        2: 5,   # Firm - 5 days
        3: 3,   # Almost ripe - 3 days
        4: 2,   # Perfect - 2 days
        5: 1,   # Very soft - 1 day
        6: 0,   # Overripe - use immediately
    },
    "orange": {
        1: 21,  # Fresh - 3 weeks
        2: 14,  # Good - 2 weeks
        3: 10,  # Ripe - 10 days
        4: 7,   # Soft - 1 week
        5: 3,   # Getting old - 3 days
        6: 1,   # Moldy spots - 1 day
    },
    "tomato": {
        1: 14,  # Green - 2 weeks
        2: 10,  # Turning - 10 days
        3: 7,   # Pink - 1 week
        4: 4,   # Ripe - 4 days
        5: 2,   # Very ripe - 2 days
        6: 1,   # Overripe - 1 day
    },
    # Default for unknown fruits
    "default": {
        1: 14,
        2: 10,
        3: 7,
        4: 4,
        5: 2,
        6: 1,
    }
}


def calculate_expiry_date(fruit_name: str, stage: int) -> str:
    """
    Calculate expiry date based on fruit type and ripeness stage.
    
    Args:
        fruit_name: Name of the fruit
        stage: Ripeness stage (1-6)
    
    Returns:
        Expiry date as ISO format string
    """
    fruit_name = fruit_name.lower()
    
    # Get shelf life for this fruit, or use default
    shelf_life_stages = SHELF_LIFE_MAP.get(fruit_name, SHELF_LIFE_MAP["default"])
    days_until_expiry = shelf_life_stages.get(stage, 3)  # Default to 3 days if stage not found
    
    expiry_date = datetime.now() + timedelta(days=days_until_expiry)
    return expiry_date.isoformat()


class PantryModel:
    """Model for managing pantry items in the database."""
    
    @staticmethod
    def create_item(item: PantryItemCreate) -> int:
        """
        Add a new item to the pantry.
        
        Args:
            item: PantryItemCreate object with item details
            
        Returns:
            ID of the newly created item
        """
        added_date = datetime.now().isoformat()
        expiry_date = calculate_expiry_date(item.fruit_name, item.stage)
        
        query = '''
            INSERT INTO pantry_items 
            (fruit_name, stage, confidence, expiry_date, added_date, image_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            item.fruit_name,
            item.stage,
            item.confidence,
            expiry_date,
            added_date,
            item.image_path,
            item.notes
        )
        
        item_id = execute_query(query, params)
        return item_id
    
    @staticmethod
    def get_all_items() -> List[Dict]:
        """
        Get all items from the pantry.
        
        Returns:
            List of pantry items as dictionaries
        """
        query = 'SELECT * FROM pantry_items ORDER BY expiry_date ASC'
        return execute_query(query, fetch_all=True)
    
    @staticmethod
    def get_item_by_id(item_id: int) -> Optional[Dict]:
        """
        Get a specific pantry item by ID.
        
        Args:
            item_id: ID of the item to retrieve
            
        Returns:
            Pantry item as dictionary or None if not found
        """
        query = 'SELECT * FROM pantry_items WHERE id = ?'
        return execute_query(query, (item_id,), fetch_one=True)
    
    @staticmethod
    def delete_item(item_id: int) -> bool:
        """
        Delete an item from the pantry.
        
        Args:
            item_id: ID of the item to delete
            
        Returns:
            True if deleted, False otherwise
        """
        query = 'DELETE FROM pantry_items WHERE id = ?'
        execute_query(query, (item_id,))
        return True
    
    @staticmethod
    def get_expiring_soon(days: int = 3) -> List[Dict]:
        """
        Get items expiring within a certain number of days.
        
        Args:
            days: Number of days threshold
            
        Returns:
            List of items expiring soon
        """
        threshold_date = (datetime.now() + timedelta(days=days)).isoformat()
        query = '''
            SELECT * FROM pantry_items 
            WHERE expiry_date <= ? 
            ORDER BY expiry_date ASC
        '''
        return execute_query(query, (threshold_date,), fetch_all=True)


# Initialize database on module import
init_db()
