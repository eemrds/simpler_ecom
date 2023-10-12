from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

from generate_data import generate_data

generate_data()
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    """Get the database from the MongoDB connection"""
    client = MongoClient("mongodb://mongo:27017/")
    return client.simpledatabase


def query_db(filter={}, collection="products", db=None) -> List[dict]:
    """Query the database with a filter

    Args:
        filter: Filter for the query. Defaults to {}.
        collection: Collection to query. Defaults to "products".
        db: Database to query. Defaults to None.

    Returns:
        List of results
    """
    coll = db[collection]
    return list(coll.find(filter))


class Product(BaseModel):
    """Product model"""

    id: str
    amount_left: Optional[int]
    name: Optional[str]
    price: Optional[float]
    image_link: Optional[str]


class ProductList(BaseModel):
    """Product list model"""

    data: List[Product]


class ProductUpdate(BaseModel):
    """Product update model"""

    id: str


@app.get("/products", response_model=ProductList)
async def get_products(id: Optional[str] = None) -> ProductList:
    """Get all products or a single product by id

    Args:
        id: Product id. Defaults to None.

    Returns:
        List of products
    """
    filter = {}
    if id:
        filter = {"id": id}
    data_from_mongo = query_db(filter, db=get_db())
    for item in data_from_mongo:
        if "_id" in item:
            item["_id"] = str(item["_id"])
    return {"data": data_from_mongo}


@app.put("/products", response_model=dict)
async def update_product(product: ProductUpdate) -> Dict[str, Any]:
    """Update a product

    Args:
        product: Product to update

    Raises:
        HTTPException: If the product id is missing
    """
    print(product)
    if not product.id:
        raise HTTPException(status_code=400, detail="Missing 'id'")

    db = get_db()
    coll = db["products"]
    coll.update_one({"id": product.id}, {"$inc": {"amount_left": -1}})
    return {"message": "Stock decreased by 1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
