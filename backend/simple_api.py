from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

from generate_data import generate_data  # Ensure this import is correct

# Run the data generation and load environment variables
generate_data()
load_dotenv()

# Setup the FastAPI app and allow all origins for CORS
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    client = MongoClient("mongodb://mongo:27017/")
    return client.simpledatabase


def query_db(filter={}, collection="products", db=None):
    coll = db[collection]
    return list(coll.find(filter))


class Product(BaseModel):
    id: str
    amount_left: Optional[int]


class ProductList(BaseModel):
    data: List[Product]


@app.get("/products", response_model=ProductList)
async def get_products(id: Optional[str] = None):
    filter = {}
    if id:
        filter = {"id": id}
    data_from_mongo = query_db(filter, db=get_db())
    for item in data_from_mongo:
        if "_id" in item:
            item["_id"] = str(item["_id"])
    return {"data": data_from_mongo}


@app.put("/products", response_model=dict)
async def update_product(product: Product):
    if not product.id:
        raise HTTPException(status_code=400, detail="Missing 'id'")

    db = get_db()
    coll = db["products"]
    coll.update_one({"id": product.id}, {"$inc": {"amount_left": -1}})
    return {"message": "Stock decreased by 1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
