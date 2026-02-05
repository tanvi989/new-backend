from typing import List, Dict, Any, Optional
from pymongo.database import Database
from pymongo.collection import Collection

# Base CDN URL for product images
BASE_IMAGE_URL = "https://cdn.eyemyeye.us/shared/images/products/"

class ProductService:
    def __init__(self, db: Database):
        self.db = db
        # Use the correct Django collection name
        self.collection: Collection = self.db["products"]

    def construct_image_url(self, skuid: str, position: int = 1) -> str:
        """Construct image URL based on skuid and position"""
        return f"{BASE_IMAGE_URL}{skuid}/{skuid}-{position}.jpg"

    def get_all_products(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        try:
            query = {}

            # --- Gender Filter ---
            if filters.get("gender") and filters["gender"] != "All":
                query["gender"] = {"$regex": f"^{filters['gender']}", "$options": "i"}

            # --- Price Filter ---
            if filters.get("price_min") is not None or filters.get("price_max") is not None:
                price_query = {}
                if filters.get("price_min") is not None:
                    price_query["$gte"] = float(filters["price_min"])
                if filters.get("price_max") is not None:
                    price_query["$lte"] = float(filters["price_max"])
                if price_query:
                    query["price"] = price_query

            # --- Shape Filter ---
            if filters.get("shape"):
                query["shape"] = {"$in": filters["shape"]}

            # --- Frame Colors (using frameColor field from Django model) ---
            if filters.get("colors"):
                color_regexes = [{"$regex": f"^{color}$", "$options": "i"} for color in filters["colors"]]
                if len(color_regexes) == 1:
                    query["frameColor"] = color_regexes[0]
                else:
                    query["$or"] = [{"frameColor": regex} for regex in color_regexes]

            # --- Material ---
            if filters.get("material"):
                material_regexes = [{"$regex": f"^{mat}$", "$options": "i"} for mat in filters["material"]]
                if len(material_regexes) == 1:
                    query["material"] = material_regexes[0]
                else:
                    query["$or"] = [{"material": regex} for regex in material_regexes]

            # --- Size ---
            if filters.get("size"):
                size_regexes = [{"$regex": f"^{size}$", "$options": "i"} for size in filters["size"]]
                if len(size_regexes) == 1:
                    query["size"] = size_regexes[0]
                else:
                    query["$or"] = [{"size": regex} for regex in size_regexes]

            # --- Brand ---
            if filters.get("brand"):
                brand_regexes = [{"$regex": f"^{brand}$", "$options": "i"} for brand in filters["brand"]]
                if len(brand_regexes) == 1:
                    query["brand"] = brand_regexes[0]
                else:
                    query["$or"] = [{"brand": regex} for regex in brand_regexes]

            # --- Style ---
            if filters.get("style"):
                style_regexes = [{"$regex": f"^{style}$", "$options": "i"} for style in filters["style"]]
                if len(style_regexes) == 1:
                    query["style"] = style_regexes[0]
                else:
                    query["$or"] = [{"style": regex} for regex in style_regexes]

            # --- Comfort (array field) ---
            if filters.get("comfort"):
                # Comfort is an array field, so we use $in to match any of the selected values
                query["comfort"] = {"$in": filters["comfort"]}

            # Only show active products
            query["is_active"] = True

            print(f"DEBUG: Product Query: {query}")
            with open("debug_queries.log", "a", encoding="utf-8") as f:
                f.write(f"Query: {query} | Filters: {filters}\n")

            # Execute Query with pagination
            limit = filters.get("limit", 20)
            page = filters.get("page", 1)
            
            cursor = self.collection.find(query)
            total_count = self.collection.count_documents(query)
            
            skip = (page - 1) * limit
            cursor = cursor.skip(skip).limit(limit)
            
            # Convert to list and process each product
            products = []
            for doc in cursor:
                # Convert ObjectId to string
                doc["id"] = str(doc["_id"])
                del doc["_id"]
                
                # Normalize field names for frontend
                doc["product_name"] = doc.get("name", "")
                doc["selling_price"] = doc.get("price", 0)
                doc["color"] = doc.get("frame_color", "")
                
                # Add colors array for frontend (convert single color to array)
                frame_color = doc.get("frame_color", "")
                if frame_color:
                    doc["colors"] = [frame_color]
                else:
                    doc["colors"] = []
                
                # Use images array from database if it exists, otherwise construct it
                if "images" in doc and doc["images"] and len(doc["images"]) > 0:
                    # Use existing images array from database
                    image_list = doc["images"]
                    doc["image"] = image_list[0] if image_list else ""
                else:
                    # Fallback: Construct image URLs if not in database
                    skuid = doc.get("skuid", "")
                    num_images = doc.get("no_of_images", 3)
                    
                    image_list = []
                    for i in range(1, min(num_images + 1, 4)):  # Max 3 images
                        image_list.append(self.construct_image_url(skuid, i))
                    
                    doc["images"] = image_list
                    doc["image"] = image_list[0] if image_list else ""
                
                # Keep naming_system and features (they vary by shape)
                # These are already in the document from MongoDB
                
                products.append(doc)

            return {
                "success": True,
                "data": products,
                "pagination": {
                    "total": total_count,
                    "page": page,
                    "limit": limit,
                    "pages": (total_count + limit - 1) // limit if limit > 0 else 0
                },
                "debug_info": {
                    "total_db_count": self.collection.count_documents({}),
                    "filters_applied": str(query),
                    "count_after_filter": total_count
                }
            }

        except Exception as e:
            print(f"ERROR: get_all_products failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "msg": str(e)
            }
