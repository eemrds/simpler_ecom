from pymongo import MongoClient


INITIAL_DATA = [
    {
        "id": "1",
        "name": "Laptop",
        "price": 1000,
        "amount_left": 10,
        "image_link": "laptop.jpg",
    },
    {
        "id": "2",
        "name": "Phone",
        "price": 500,
        "amount_left": 20,
        "image_link": "phone.jpg",
    },
    {
        "id": "3",
        "name": "TV",
        "price": 1500,
        "amount_left": 5,
        "image_link": "tv.jpg",
    },
    {
        "id": "4",
        "name": "Headphones",
        "price": 100,
        "amount_left": 50,
        "image_link": "headphones.jpg",
    },
]


def generate_data():
    client = MongoClient("mongodb://mongo:27017/")
    db = client["simpledatabase"]
    collection = db["products"]

    if collection.count_documents({}) == 0:
        collection.insert_many(INITIAL_DATA)
        print("Inserted initial data into database.")
    else:
        print("Already Exists. Skipped Generation")
