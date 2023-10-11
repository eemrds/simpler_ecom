import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os
from dotenv import load_dotenv

from generate_data import generate_data
from pymongo import MongoClient
from bson.objectid import ObjectId

generate_data()
load_dotenv()


class SimpleAPI(BaseHTTPRequestHandler):
    def query_db(self, filter={}, collection="products"):
        client = MongoClient("mongodb://mongo:27017/")
        db = client.simpledatabase
        coll = db[collection]
        return list(coll.find(filter))

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        filter = {}

        if "id" in query_components:
            product_id = query_components["id"][0]
            filter = {"id": product_id}
            data_from_mongo = self.query_db(filter)

            if isinstance(data_from_mongo, dict):
                data_from_mongo["_id"] = str(data_from_mongo["_id"])
        else:
            data_from_mongo = self.query_db(filter)
            for item in data_from_mongo:
                if "_id" in item:
                    item["_id"] = str(item["_id"])

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        response = {"message": "Data fetched", "data": data_from_mongo}
        self.wfile.write(json.dumps(response, default=str).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_PUT(self):
        length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(length)
        post_data = json.loads(post_data.decode("utf-8"))

        # Check for required fields
        if "id" not in post_data:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Missing 'id'"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        product_id = post_data["id"]

        # Connect to MongoDB
        client = MongoClient("mongodb://mongo:27017/")
        db = client.simpledatabase
        coll = db["products"]

        coll.update_one({"id": product_id}, {"$inc": {"amount_left": -1}})

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        response = {"message": "Stock decreased by 1"}
        self.wfile.write(json.dumps(response).encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, SimpleAPI)
    print("Running server...")
    httpd.serve_forever()
