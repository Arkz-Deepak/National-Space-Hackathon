from app.models import Item
from datetime import datetime, timedelta

mock_db = {
    "items": [],
    "logs": [],
    "containers": []
}

def place_items(item: Item):
    mock_db["items"].append(item)
    return {"message": f"Item {item.id} placed"}

def retrieve_item(item_id: str):
    for item in mock_db["items"]:
        if item.id == item_id:
            item.current_uses += 1
            log = f"Retrieved {item.name} at {datetime.now()}"
            mock_db["logs"].append(log)
            return {"message": log}
    return {"error": "Item not found"}

def simulate_days(days: int):
    today = datetime.now()
    removed_items = []
    for item in mock_db["items"]:
        if item.expiry_date and item.expiry_date < today + timedelta(days=days):
            removed_items.append(item.id)
    return {"expired_items": removed_items}
