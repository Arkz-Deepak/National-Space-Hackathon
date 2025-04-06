from fastapi import FastAPI
from app.models import Item, Container
from app.utils import place_items, retrieve_item, simulate_days

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Cargo Manager API Running now 🚀"}

@app.post("/place/")
def place(item: Item):
    result = place_items(item)
    return result

@app.post("/retrieve/")
def retrieve(item_id: str):
    result = retrieve_item(item_id)
    return result

@app.post("/simulate/")
def simulate(days: int):
    result = simulate_days(days)
    return result
