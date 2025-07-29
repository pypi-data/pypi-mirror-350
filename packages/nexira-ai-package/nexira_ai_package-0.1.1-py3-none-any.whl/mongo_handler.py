from pymongo import MongoClient, AsyncMongoClient
from typing import Optional, List, Dict, Any
import logging
import datetime
import atexit
from src.app_config import app_config
from src.chat_history.schema import (
    ConversationInfor,
    UserThread
)

class AsyncBaseMongoDBHandler:
    def __init__(self, db_name: str, collection_name: str):
        self.client = None
        self.db = None
        self.collection = None
        self.db_name = db_name
        self.collection_name = collection_name

    async def connect_to_database(self):
        """Establish a connection to MongoDB."""
        try:
            if not all([app_config.MONGODB_URI, self.db_name, self.collection_name]):
                raise ValueError(
                    "❌ MongoDB credentials are missing. Check your configuration."
                )

            if not self.client:
                self.client = AsyncMongoClient(app_config.MONGODB_URI)
                self.db = self.client[self.db_name]
                self.collection = self.db[self.collection_name]
                print("✅ MongoDB connection established.")

        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            self.close_connection()

    async def insert_one(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a single document into MongoDB."""
        if self.collection is None:
            print("No database connection")
            return {"status": "error", "message": "No database connection"}

        print("--------------------------------")
        print(data)
        try:
            result = await self.collection.insert_one(data)
            inserted_doc = await self.collection.find_one({"_id": result.inserted_id})
            print("✅ Document inserted successfully.")
            return {
                "status": "success",
                "message": "Document inserted successfully",
                "data": inserted_doc,
            }
        except Exception as e:
            print(f"❌ Error inserting document: {e}")
            return {"status": "error", "message": str(e)}

    async def insert_many(self, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Insert multiple documents into MongoDB."""
        if self.collection is None:
            return {"status": "error", "message": "No database connection"}

        try:
            result = await self.collection.insert_many(data_list)
            print(f"✅ {len(result.inserted_ids)} documents inserted successfully.")
            return {
                "status": "success",
                "message": f"{len(result.inserted_ids)} documents inserted successfully",
                "inserted_ids": result.inserted_ids,
            }
        except Exception as e:
            print(f"❌ Error inserting documents: {e}")
            return {"status": "error", "message": str(e)}

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document in MongoDB."""
        if self.collection is None:
            return None

        try:
            document = await self.collection.find_one(query)
            return document
        except Exception as e:
            print(f"❌ Error finding document: {e}")
            return None

    async def find_many(self, query: Dict[str, Any], limit: int = 0) -> List[Dict[str, Any]]:
        """Find multiple documents in MongoDB."""
        # import pdb; pdb.set_trace()
        # if not self.collection:
        #     return []
        # import pdb; pdb.set_trace()

        try:
            cursor = await self.collection.find(query)
            if limit > 0:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error finding documents: {e}")
            return []

    async def update_one(
        self, query: Dict[str, Any], update_data: Dict[str, Any], upsert: bool = False
    ) -> Dict[str, Any]:
        """Update a single document in MongoDB."""
        if self.collection is None:
            return {"status": "error", "message": "No database connection"}

        try:
            result = await self.collection.update_one(query, update_data, upsert=upsert)
            if result.modified_count > 0:
                print("✅ Document updated successfully.")
                return {
                    "status": "success",
                    "message": "Document updated successfully",
                    "modified_count": result.modified_count,
                }
            else:
                print("ℹ️ No document was updated.")
                return {
                    "status": "info",
                    "message": "No document was updated",
                    "modified_count": 0,
                }
        except Exception as e:
            print(f"❌ Error updating document: {e}")
            return {"status": "error", "message": str(e)}

    async def delete_one(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a single document from MongoDB."""
        if self.collection is None:
            return {"status": "error", "message": "No database connection"}

        try:
            result = await self.collection.delete_one(query)
            if result.deleted_count > 0:
                print("✅ Document deleted successfully.")
                return {
                    "status": "success",
                    "message": "Document deleted successfully",
                    "deleted_count": result.deleted_count,
                }
            else:
                print("ℹ️ No document was deleted.")
                return {
                    "status": "info",
                    "message": "No document was deleted",
                    "deleted_count": 0,
                }
        except Exception as e:
            print(f"❌ Error deleting document: {e}")
            return {"status": "error", "message": str(e)}

    async def delete_many(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Delete multiple documents from MongoDB."""
        if self.collection is None:
            return {"status": "error", "message": "No database connection"}

        try:
            result = await self.collection.delete_many(query)
            print(f"✅ {result.deleted_count} documents deleted successfully.")
            return {
                "status": "success",
                "message": f"{result.deleted_count} documents deleted successfully",
                "deleted_count": result.deleted_count,
            }
        except Exception as e:
            print(f"❌ Error deleting documents: {e}")
            return {"status": "error", "message": str(e)}

    async def close_connection(self):
        """Close the MongoDB connection."""
        try:
            if self.client:
                self.client.close()
                self.client = None
                self.db = None
                self.collection = None
                print("🔒 MongoDB connection closed.")
        except Exception as e:
            print(f"⚠️ Error closing MongoDB connection: {e}")

    async def __aenter__(self):
        await self.connect_to_database()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_connection()

class BaseMongoDBHandler:
    def __init__(self, db_name: str, collection_name: str):
        """Initialize MongoDB connection."""
        self.client = None
        self.db = None
        self.collection = None
        self.db_name = db_name
        self.collection_name = collection_name
        atexit.register(self.close_connection)

    def connect_to_database(self):
        """Establish a connection to MongoDB."""
        try:
            if not all([app_config.MONGODB_URI, self.db_name, self.collection_name]):
                raise ValueError(
                    "❌ MongoDB credentials are missing. Check your configuration."
                )

            if not self.client:
                self.client = MongoClient(app_config.MONGODB_URI)
                self.db = self.client[self.db_name]
                self.collection = self.db[self.collection_name]
                print("✅ MongoDB connection established.")

        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            self.close_connection()

    def insert_one(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a single document into MongoDB."""
        if not self.collection:
            return {"status": "error", "message": "No database connection"}

        try:
            result = self.collection.insert_one(data)
            inserted_doc = self.collection.find_one({"_id": result.inserted_id})
            print("✅ Document inserted successfully.")
            return {
                "status": "success",
                "message": "Document inserted successfully",
                "data": inserted_doc,
            }
        except Exception as e:
            print(f"❌ Error inserting document: {e}")
            return {"status": "error", "message": str(e)}

    def insert_many(self, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Insert multiple documents into MongoDB."""
        if not self.collection:
            return {"status": "error", "message": "No database connection"}

        try:
            result = self.collection.insert_many(data_list)
            print(f"✅ {len(result.inserted_ids)} documents inserted successfully.")
            return {
                "status": "success",
                "message": f"{len(result.inserted_ids)} documents inserted successfully",
                "inserted_ids": result.inserted_ids,
            }
        except Exception as e:
            print(f"❌ Error inserting documents: {e}")
            return {"status": "error", "message": str(e)}

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document in MongoDB."""
        if not self.collection:
            return None

        try:
            document = self.collection.find_one(query)
            return document
        except Exception as e:
            print(f"❌ Error finding document: {e}")
            return None

    def find_many(self, query: Dict[str, Any], limit: int = 0) -> List[Dict[str, Any]]:
        """Find multiple documents in MongoDB."""
        # import pdb; pdb.set_trace()
        # if not self.collection:
        #     return []
        # import pdb; pdb.set_trace()

        try:
            cursor = self.collection.find(query)
            if limit > 0:
                cursor = cursor.limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error finding documents: {e}")
            return []

    def update_one(
        self, query: Dict[str, Any], update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a single document in MongoDB."""
        if not self.collection:
            return {"status": "error", "message": "No database connection"}

        try:
            result = self.collection.update_one(query, {"$set": update_data})
            if result.modified_count > 0:
                print("✅ Document updated successfully.")
                return {
                    "status": "success",
                    "message": "Document updated successfully",
                    "modified_count": result.modified_count,
                }
            else:
                print("ℹ️ No document was updated.")
                return {
                    "status": "info",
                    "message": "No document was updated",
                    "modified_count": 0,
                }
        except Exception as e:
            print(f"❌ Error updating document: {e}")
            return {"status": "error", "message": str(e)}

    def delete_one(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Delete a single document from MongoDB."""
        if not self.collection:
            return {"status": "error", "message": "No database connection"}

        try:
            result = self.collection.delete_one(query)
            if result.deleted_count is not None and result.deleted_count > 0:
                print("✅ Document deleted successfully.")
                return {
                    "status": "success",
                    "message": "Document deleted successfully",
                    "deleted_count": result.deleted_count,
                }
            else:
                print("ℹ️ No document was deleted.")
                return {
                    "status": "info",
                    "message": "No document was deleted",
                    "deleted_count": 0,
                }
        except Exception as e:
            print(f"❌ Error deleting document: {e}")
            return {"status": "error", "message": str(e)}

    def delete_many(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Delete multiple documents from MongoDB."""
        if not self.collection:
            return {"status": "error", "message": "No database connection"}

        try:
            result = self.collection.delete_many(query)
            print(f"✅ {result.deleted_count} documents deleted successfully.")
            return {
                "status": "success",
                "message": f"{result.deleted_count} documents deleted successfully",
                "deleted_count": result.deleted_count,
            }
        except Exception as e:
            print(f"❌ Error deleting documents: {e}")
            return {"status": "error", "message": str(e)}

    def close_connection(self):
        """Close the MongoDB connection."""
        try:
            if self.client:
                self.client.close()
                self.client = None
                self.db = None
                self.collection = None
                print("🔒 MongoDB connection closed.")
        except Exception as e:
            print(f"⚠️ Error closing MongoDB connection: {e}")

    def __enter__(self):
        """Context manager entry."""
        self.connect_to_database()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_connection()

