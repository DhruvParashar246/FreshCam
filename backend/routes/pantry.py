from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from models.pantry_model import PantryModel, PantryItemCreate, PantryItem

router = APIRouter(prefix="/pantry", tags=["pantry"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_item(item: PantryItemCreate):
    """
    Add a new item to the pantry.
    
    Args:
        item: PantryItemCreate with fruit_name, stage, confidence, optional image_path and notes
        
    Returns:
        Created item with ID and calculated expiry date
    """
    try:
        item_id = PantryModel.create_item(item)
        created_item = PantryModel.get_item_by_id(item_id)
        
        return {
            "success": True,
            "message": "Item added to pantry",
            "item": created_item
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add item: {str(e)}"
        )


@router.get("/list", response_model=List[dict])
async def list_items():
    """
    Get all items in the pantry, ordered by expiry date.
    
    Returns:
        List of all pantry items
    """
    try:
        items = PantryModel.get_all_items()
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve items: {str(e)}"
        )


@router.get("/{item_id}")
async def get_item(item_id: int):
    """
    Get a specific pantry item by ID.
    
    Args:
        item_id: ID of the item to retrieve
        
    Returns:
        Pantry item details
    """
    try:
        item = PantryModel.get_item_by_id(item_id)
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve item: {str(e)}"
        )


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: int):
    """
    Delete an item from the pantry.
    
    Args:
        item_id: ID of the item to delete
        
    Returns:
        Success message
    """
    try:
        # Check if item exists first
        item = PantryModel.get_item_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        PantryModel.delete_item(item_id)
        
        return {
            "success": True,
            "message": f"Item {item_id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete item: {str(e)}"
        )


@router.get("/expiring/soon")
async def get_expiring_soon(days: int = 3):
    """
    Get items expiring within a specified number of days.
    
    Args:
        days: Number of days threshold (default: 3)
        
    Returns:
        List of items expiring soon
    """
    try:
        items = PantryModel.get_expiring_soon(days=days)
        
        return {
            "threshold_days": days,
            "count": len(items),
            "items": items
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve expiring items: {str(e)}"
        )
