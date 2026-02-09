#!/usr/bin/env python3
"""
Create the sku_measurements collection in the backend database.
Inserts one placeholder doc so the collection is visible in MongoDB Compass/UI
(empty collections often don't show). Uses .env: MONGO_URI, DATABASE_NAME, SKU_MEASUREMENTS_COLLECTION.
Run from newbackend: python seed_sku_measurements.py
"""
import sys
from pathlib import Path
from datetime import datetime, timezone

_script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_script_dir))

from dotenv import load_dotenv
load_dotenv(_script_dir / ".env")
load_dotenv()

import config
from pymongo import MongoClient

def main():
    coll_name = getattr(config, "SKU_MEASUREMENTS_COLLECTION", "sku_measurements")
    client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=15000)
    db = client[config.DATABASE_NAME]
    coll = db[coll_name]

    # Ensure collection exists and is visible (empty collections often hidden in DB UIs)
    if coll.count_documents({}) == 0:
        coll.insert_one({
            "sku_id": "_placeholder",
            "frame_width": 0,
            "lens_height": 0,
            "_comment": "Delete this doc after adding real SKU measurements",
        })
        print(f"Created collection '{coll_name}' and inserted placeholder doc (you can delete it later).")
    else:
        print(f"Collection '{coll_name}' already exists with {coll.count_documents({})} document(s).")

    print(f"Database: {config.DATABASE_NAME}")
    client.close()

if __name__ == "__main__":
    main()
