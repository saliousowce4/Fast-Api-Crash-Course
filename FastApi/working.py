from typing import Optional

from fastapi import FastAPI, Query, HTTPException, status
from pydantic.main import BaseModel
from sqlalchemy import update

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get("/")
def home():
    return {"data": "hello"}


inventory = {
    1: {
        "name": "Milk",
        "price": 200,
        "brand": "regular"
    }
}


@app.get("/get-item/{item_id}/{price}")
def get_item(item_id: int, price: int):
    return inventory[item_id]


@app.get("/get_by_name/{item_id}")
def get_by_name(*, item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exists")
    inventory[item_id] = item
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found")

    if item.name is not None:
        inventory[item_id].name = item.name

    if item.price is not None:
        inventory[item_id].price = item.price

    if item.brand is not None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int = Query(..., description="The ID of item to delete")):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID not found")

    del inventory[item_id]
    return {"Success": "Item deleted"}
