from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ValidationError, conlist
from typing import List, Optional, Dict
from datetime import datetime

app = FastAPI()

class Item(BaseModel):
    itemId: str
    name: str
    width: float
    depth: float
    height: float
    priority: int
    expiryDate: Optional[str] = None  # ISO format, optional
    usageLimit: Optional[int] = None
    preferredZone: str

class Container(BaseModel):
    containerId: str
    zone: str
    width: float
    depth: float
    height: float

class PlacementRequest(BaseModel):
    items: List[Item]
    containers: List[Container]

class PlacementResponse(BaseModel):
    recommendations: List[dict]  # Flexible structure

class RetrievalRequest(BaseModel):
    itemId: str

class RetrievalResponse(BaseModel):
    containerId: str
    x: float
    y: float
    z: float
    steps: int
    message: str

class RearrangementRequest(BaseModel):
    newItems: List[Item]
    existingItems: List[Item]  # Current state of items in containers
    containers: List[Container]

class RearrangementResponse(BaseModel):
    moves: List[dict]  # List of moves to perform

class WasteItem(BaseModel):
    itemId: str
    name: str
    width: float
    depth: float
    height: float
    expiryDate: Optional[str]
    usageLimit: Optional[int]

class WasteDisposalRequest(BaseModel):
    wasteItems: List[WasteItem]
    containers: List[Container] #available containers

class WasteDisposalResponse(BaseModel):
    instructions: List[dict]

class CargoReturnRequest(BaseModel):
    wasteItems: List[WasteItem]
    containers: List[Container]

class CargoReturnResponse(BaseModel):
    manifest: List[dict]
    spaceReclamationPlan: List[dict]

class LogActionRequest(BaseModel):
    action: str
    timestamp: datetime
    details: dict  # Flexible structure for action-specific details

def validate_iso_date(date_str: str) -> bool:
    """Validates ISO 8601 date format (YYYY-MM-DD)."""
    if not date_str:
        return True
    try:
        datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False

def calculate_arc_distance(angle, radius):
    """Calculates distance along an arc."""
    return (angle / 360) * 2 * math.pi * radius

def calculate_straight_line_distance(p1, p2):
    """Calculates straight-line distance between 3D points."""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)

import math

@app.post("/api/placement")
async def get_placement_recommendations(placement_request: PlacementRequest):
    """
    Recommends where to place new cargo items.
    """
    try:
        items = placement_request.items
        containers = placement_request.containers

        if not items or not containers:
            raise HTTPException(status_code=400, detail="Both 'items' and 'containers' are required.")

        for item in items:
            if not (0 <= item.priority <= 100):
                raise HTTPException(status_code=400, detail=f"Item {item.itemId} priority must be 0-100.")
            if item.expiryDate and not validate_iso_date(item.expiryDate):
                raise HTTPException(status_code=400, detail=f"Item {item.itemId} expiryDate invalid ISO format.")

        recommendations = []
        for item in items:
            placed = False
            for container in containers:
                # Basic placement logic (replace with your algorithm)
                if container.zone == item.preferredZone:
                    recommendations.append({
                        "itemId": item.itemId,
                        "containerId": container.containerId,
                        "message": f"Place in {container.zone} (Container {container.containerId})",
                        "x": 0,
                        "y": 0,
                        "z": 0,
                    })
                    placed = True
                    break
            if not placed:
                if containers:
                    recommendations.append({
                        "itemId": item.itemId,
                        "containerId": containers[0].containerId,
                        "message": f"Place in {containers[0].zone} (Container {containers[0].containerId}) - Preferred zone unavailable",
                        "x": 0,
                        "y": 0,
                        "z": 0,
                    })
                else:
                    recommendations.append({
                        "itemId": item.itemId,
                        "containerId": None,
                        "message": "No suitable container available",
                        "x": None,
                        "y": None,
                        "z": None,
                    })

        return PlacementResponse(recommendations=recommendations)

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/retrieval")
async def get_retrieval_instructions(retrieval_request: RetrievalRequest):
    """
    Provides instructions for retrieving a specific item.
    """
    try:
        item_id = retrieval_request.itemId
        #  Add logic to find the item and calculate retrieval steps
        #  This is a placeholder
        if item_id == "001":
            response = RetrievalResponse(
                containerId="contA",
                x=10,
                y=10,
                z=0,
                steps=0,
                message="Retrieve from Container A, position (10,10,0).  No obstructions.",
            )
        elif item_id == "002":
            response = RetrievalResponse(
                containerId="contB",
                x=20,
                y=30,
                z=10,
                steps=2,
                message="Retrieve from Container B, position (20,30,10). 2 items need to be moved.",
            )
        else:
            raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found.")
        return response

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/api/rearrangement")
async def get_rearrangement_plan(rearrangement_request: RearrangementRequest):
    """
    Provides a plan for rearranging items to optimize space.
    """
    try:
        new_items = rearrangement_request.newItems
        existing_items = rearrangement_request.existingItems
        containers  = rearrangement_request.containers
        # Implement rearrangement logic here
        # This is a placeholder
        if not new_items:
            raise HTTPException(status_code=400, detail="New Items list cannot be empty")

        moves = []
        for item in new_items:
            moves.append({
                "itemId": item.itemId,
                "fromContainer": "contA",  #  Determine from which container
                "toContainer": "contB",    #  Determine to which container
                "message": f"Move {item.name} from Container A to Container B to make space.",
            })
        response = RearrangementResponse(moves=moves)
        return response

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/api/waste_disposal")
async def get_waste_disposal_plan(waste_disposal_request: WasteDisposalRequest):
    """
    Provides a plan for disposing of waste items.
    """
    try:
        waste_items = waste_disposal_request.wasteItems
        containers = waste_disposal_request.containers
        # Implement waste disposal logic
        # This is a placeholder
        if not waste_items:
            raise HTTPException(status_code=400, detail="Waste items list cannot be empty")
        if not containers:
            raise HTTPException(status_code=400, detail="Containers list cannot be empty")
        instructions = []
        for item in waste_items:
            instructions.append({
                "itemId": item.itemId,
                "containerId": containers[0].containerId,  #  send to first container
                "message": f"Move waste item {item.name} to {containers[0].containerId} for disposal.",
            })
        response = WasteDisposalResponse(instructions=instructions)
        return response
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@app.post("/api/cargo_return")
async def get_cargo_return_plan(cargo_return_request: CargoReturnRequest):
    """
    Provides a plan for returning cargo and reclaiming space.
    """
    try:
        waste_items = cargo_return_request.wasteItems
        containers = cargo_return_request.containers
        # Implement cargo return planning logic
        # This is a placeholder
        manifest = []
        space_reclamation_plan = []
        total_weight = 0
        for item in waste_items:
            #  weight needs to be added to the Item class.
            item_weight = 1  # Placeholder
            total_weight += item_weight
            manifest.append({
                "itemId": item.itemId,
                "name": item.name,
                "weight": item_weight,
                "containerId": containers[0].containerId, #send to first container

            })
        if total_weight > 1000: #example weight limit
             raise HTTPException(status_code=400, detail="Total weight exceeds limit for undocking")

        space_reclamation_plan.append({
            "containerId": containers[0].containerId,
            "message": f"Remove all items from {containers[0].containerId} after waste removal.",
        })
        response = CargoReturnResponse(manifest=manifest, spaceReclamationPlan=space_reclamation_plan)
        return response

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/log_action")
async def log_action(log_action_request: LogActionRequest):
    try:
        action = log_action_request.action
        timestamp = log_action_request.timestamp
        details = log_action_request.details
        print(f"Logging action: {action} at {timestamp} with details: {details}") 

        return {"message": "Action logged successfully."}

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 
