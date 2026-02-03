"""
Migrate gaMultilens database from OLD Atlas account to NEW Atlas account.
Uses pymongo (no mongodump/mongorestore required).
"""
import sys
from pymongo import MongoClient

OLD_URI = "mongodb+srv://vacanzidev_db_user:Fxrzcgx34bTWNcIE@gamultilens.tuzaora.mongodb.net/gaMultilens?retryWrites=true&w=majority"
NEW_URI = "mongodb+srv://technology_db_user:1Eo32ibs60JolBr9@gamultilens.pjo8s8q.mongodb.net/gaMultilens?retryWrites=true&w=majority"
DB_NAME = "gaMultilens"

def main():
    print("Connecting to OLD cluster (source)...")
    try:
        old_client = MongoClient(OLD_URI, serverSelectionTimeoutMS=15000)
        old_client.server_info()
        old_db = old_client[DB_NAME]
    except Exception as e:
        print(f"ERROR: Could not connect to OLD cluster: {e}")
        sys.exit(1)

    print("Connecting to NEW cluster (destination)...")
    try:
        new_client = MongoClient(NEW_URI, serverSelectionTimeoutMS=15000)
        new_client.server_info()
        new_db = new_client[DB_NAME]
    except Exception as e:
        print(f"ERROR: Could not connect to NEW cluster: {e}")
        sys.exit(1)

    collections = old_db.list_collection_names()
    print(f"Found {len(collections)} collections: {collections}")

    for coll_name in collections:
        if coll_name.startswith("system."):
            continue
        old_coll = old_db[coll_name]
        new_coll = new_db[coll_name]
        count = old_coll.count_documents({})
        print(f"  Copying '{coll_name}' ({count} documents)...")
        if count == 0:
            continue
        docs = list(old_coll.find({}))
        if docs:
            new_coll.insert_many(docs)
        print(f"    -> Done: {coll_name}")

    print("Migration complete.")
    old_client.close()
    new_client.close()

if __name__ == "__main__":
    main()
