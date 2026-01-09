# app.py
import re
import traceback
import logging
import sys
import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict, List
from fastapi import FastAPI, Request, Form, HTTPException, Depends, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from pymongo import MongoClient
from bson import ObjectId
import jwt
from google.cloud import storage

# ---------- LOGGING CONFIGURATION ----------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Force flush output immediately
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

logger.info("=" * 80)
logger.info("🚀 MULTIFOLKS BACKEND STARTING...")
logger.info("=" * 80)

# ---------- CONFIG ----------
import config  # Must contain: MONGO_URI, DATABASE_NAME, COLLECTION_NAME, SECRET_KEY, HOST, PORT

# ---------- APP ----------
app = FastAPI(title="Multifolks Login API (Fixed with Multi-Route Support)")

logger.info("✅ FastAPI app initialized")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "multifolks.hiremyrecruiter.com",
        "email.multifolks.com",
        "https://mvp.multifolks.com"
        
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("✅ CORS middleware configured")

# ---------- REQUEST LOGGING MIDDLEWARE ----------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    
    # Log incoming request
    logger.info(f"🔵 INCOMING: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        # Log response
        status_emoji = "✅" if response.status_code < 400 else "❌"
        logger.info(f"{status_emoji} RESPONSE: {request.method} {request.url.path} - Status: {response.status_code} - Duration: {duration:.3f}s")
        
        return response
    except Exception as e:
        duration = (datetime.now() - start_time).total_seconds()
        logger.error(f"❌ ERROR: {request.method} {request.url.path} - {str(e)} - Duration: {duration:.3f}s")
        raise

logger.info("✅ Request logging middleware configured")

# ---------- AUTH / HASH ----------
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# ---------- DATABASE ----------
db_connected = False
client = None
db = None
users_collection = None

logger.info("📦 Connecting to MongoDB...")

try:
    client = MongoClient(
        config.MONGO_URI,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        retryWrites=True
    )
    db = client[config.DATABASE_NAME]
    users_collection = db[config.COLLECTION_NAME]
    client.server_info()  # Triggers connection test
    logger.info("✅ Connected to MongoDB Atlas")
    logger.info(f"📊 Database: {config.DATABASE_NAME}")
    logger.info(f"👥 Collection: {config.COLLECTION_NAME}")
    db_connected = True
except Exception as e:
    logger.error(f"❌ MongoDB connection failed: {e}")
    db_connected = False

# ---------- OPTIONAL SERVICES ----------
payment_service = None
cart_service = None
delivery_service = None
notification_service = None
product_service = None  # Added ProductService
order_service = None  # Added OrderService

logger.info("🔧 Loading optional services...")

try:
    from payment_service import StripePaymentService
    from cart_service import CartService
    from delivery_service import DeliveryService
    from notification_service import MSG91Service
    from product_service import ProductService # Import
    from order_service import OrderService  # Import OrderService
    logger.info("✅ Service modules imported successfully")
except Exception as e:
    logger.warning(f"⚠️  Optional services not available: {e}")
    StripePaymentService = CartService = DeliveryService = MSG91Service = ProductService = OrderService = None

if db_connected:
    try:
        if StripePaymentService:
            payment_service = StripePaymentService(db)
            logger.info("✅ Payment service initialized")
        if CartService:
            cart_service = CartService(db)
            logger.info("✅ Cart service initialized")
        if ProductService:
            product_service = ProductService(db) # Initialize
            logger.info("✅ Product service initialized")
        if OrderService:
            order_service = OrderService(db)  # Initialize OrderService
            logger.info("✅ Order service initialized")

        delivery_config = {
            'BLUEDART_BASE_URL': getattr(config, 'BLUEDART_BASE_URL', None),
            'BLUEDART_CUSTOMER_CODE': getattr(config, 'BLUEDART_CUSTOMER_CODE', None),
            'BLUEDART_LOGIN_ID': getattr(config, 'BLUEDART_LOGIN_ID', None),
            'BLUEDART_LICENSE_KEY': getattr(config, 'BLUEDART_LICENSE_KEY', None),
            'WAREHOUSE_PINCODE': getattr(config, 'WAREHOUSE_PINCODE', None),
            'WAREHOUSE_ADDRESS': getattr(config, 'WAREHOUSE_ADDRESS', None),
        }
        if DeliveryService:
            delivery_service = DeliveryService(db, delivery_config)
        if MSG91Service:
            notification_service = MSG91Service()
        print("External services initialized")
    except Exception as e:
        print("Failed to initialize external services:", e)

# ... (Existing Code) ...

# ---------- PRODUCT ENDPOINTS ----------
@app.get("/api/v1/products/all")
async def get_all_products(
    gender: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    shape: Optional[List[str]] = Query(None),
    colors: Optional[List[str]] = Query(None),
    material: Optional[List[str]] = Query(None),
    collections: Optional[List[str]] = Query(None),
    comfort: Optional[List[str]] = Query(None),
    size: Optional[List[str]] = Query(None),
    brand: Optional[List[str]] = Query(None),
    style: Optional[List[str]] = Query(None),
    limit: Optional[int] = None
):
    if not product_service:
        raise HTTPException(status_code=503, detail="Product service unavailable")
    
    filters = {
        "gender": gender,
        "price_min": price_min,
        "price_max": price_max,
        "shape": shape,
        "colors": colors,
        "material": material,
        "collections": collections,
        "comfort": comfort,
        "size": size,
        "brand": brand,
        "style": style,
        "limit": limit
    }
    
    # Filter out None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    return product_service.get_all_products(filters)

# ---------- HELPERS ----------
UK_MOBILE_PATTERN = re.compile(r"^(\+447\d{9}|07\d{9})$")
# ... (Rest of file) ...

def is_valid_uk_mobile(number: str) -> bool:
    if not number:
        return False
    number = number.strip().replace(" ", "")
    return bool(UK_MOBILE_PATTERN.match(number))

def normalize_mobile(number: str) -> str:
    if not number:
        return ""
    s = number.strip().replace(" ", "")
    if s.startswith("+44"):
        return s
    if s.startswith("0"):
        return "+44" + s[1:]
    if s.startswith("7") and len(s) == 10:
        return "+44" + s
    return s

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def generate_jwt_token(user_id: str, email: str) -> str:
    payload = {
        "user_id": str(user_id),
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")
    return token.decode("utf-8") if isinstance(token, bytes) else token

def decode_jwt_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])

# ---------- TOKEN DEPENDENCY ----------
# ---------- TOKEN DEPENDENCY ----------
def verify_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    request: Request = None
):
    # Check for Guest ID first if no credentials
    if not credentials:
        guest_id = request.headers.get("X-Guest-ID")
        if guest_id:
            print(f"Guest access with ID: {guest_id}")
            return {"_id": guest_id, "email": "guest@multifolks.com", "is_guest": True}
        raise HTTPException(status_code=401, detail="Missing authentication credentials")

    try:
        token = credentials.credentials
        # print(f"Verifying token: {token[:20]}...")  # Log first 20 chars
        payload = decode_jwt_token(token)
        # print(f"Token payload: {payload}")
        email: str = payload.get("email")
        if not email:
            print("ERROR: No email in token payload")
            raise HTTPException(status_code=401, detail="Invalid token payload")

        if not db_connected:
            raise HTTPException(status_code=503, detail="Database not connected")

        user = users_collection.find_one({"email": email})
        if not user:
            print(f"ERROR: User not found for email: {email}")
            raise HTTPException(status_code=401, detail="User not found")

        # print(f"Token verified successfully for user: {email}")
        return user
    except jwt.ExpiredSignatureError:
        print("ERROR: Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        print(f"ERROR: Invalid token - {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print("Token verification error:", e)
        raise HTTPException(status_code=500, detail="Token verification failed")

# ---------- MODELS ----------
class LoginRequest(BaseModel):
    username: EmailStr
    password: str

class LoginResponse(BaseModel):
    success: bool
    status: int
    msg: str
    data: dict

class UpdateProfileRequest(BaseModel):
    model_config = {"extra": "allow"}  # Allow extra fields for flexibility
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile: Optional[str] = None
    contact_number: Optional[str] = None  # Alternative field name
    country_code: Optional[int] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    birth_month: Optional[str] = None
    birth_year: Optional[str] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    shop_address: Optional[str] = None
    store_id: Optional[str] = None
    retail_shop_name: Optional[str] = None
    bank_details: Optional[str] = None
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None

class CreatePaymentSessionRequest(BaseModel):
    order_id: str
    amount: float
    currency: str = "GBP"
    metadata: Optional[Dict[str, Any]] = None

class CheckPincodeRequest(BaseModel):
    pincode: str

class CreateShipmentRequest(BaseModel):
    order_id: str
    customer_details: Dict[str, Any]

class MergeGuestCartRequest(BaseModel):
    guest_id: str

# ---------- LOGIN HELPER ----------
async def login_user_by_email(email: str, password: str):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database not connected")
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail={"success": False, "status": 4001, "msg": "Invalid username or password"})
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail={"success": False, "status": 4002, "msg": "Account deactivated"})
    if not verify_password(password, user.get("password", "")):
        raise HTTPException(status_code=400, detail={"success": False, "status": 4001, "msg": "Invalid password"})

    users_collection.update_one({"_id": user["_id"]}, {"$set": {"updateTime": datetime.now(timezone.utc)}})
    token = generate_jwt_token(str(user["_id"]), user["email"])
    return {
        "success": True,
        "status": 200,
        "msg": "Welcome back! You are successfully logged in",
        "data": {
            "first_name": user.get("firstName", ""),
            "last_name": user.get("lastName", ""),
            "email": user["email"],
            "mobile": str(user.get("primaryContact", "")),
            "mobile_international": user.get("international_mobile", ""),
            "is_verified": user.get("is_verified", False),
            "refer_code": user.get("my_code", ""),
            "id": str(user["_id"]),
            "token": token,
            "is_new_user": False
        }
    }

@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def v1_login(login_request: LoginRequest):
    return await login_user_by_email(login_request.username, login_request.password)

@app.get("/api/v1/accounts/check-email")
async def check_email(email: str):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    exists = users_collection.find_one({"email": email}) is not None
    return {"success": True, "data": {"is_registered": exists}}

# ---------- UNIFIED AUTH WITH MULTI-ROUTE SUPPORT ----------
@app.post("/api/v1/auth/simple-register")
@app.post("/api/v1/auth/login")
@app.post("/api/v1/auth/unified")
@app.post("/api/v1/auth/auth")
async def unified_auth(
    request: Request,
    username: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    mobile: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    country_code: str = Form("44"),
    is_subscribed_whatsapp: bool = Form(True),
    otp: Optional[str] = Form(None),  # Added for your payload
):
    try:
        current_path = request.url.path
        print(f"Request matched route: {current_path}")  # Debug log

        # Safe JSON fallback (only if Content-Type matches, with try-catch)
        content_type = request.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            try:
                body = await request.json()
                username = body.get("username", username)
                first_name = body.get("first_name", first_name)
                last_name = body.get("last_name", last_name)
                email = body.get("email", email)
                mobile = body.get("mobile", mobile)
                password = body.get("password", password)
                country_code = body.get("country_code", country_code)
                is_subscribed_whatsapp = body.get("is_subscribed_whatsapp", is_subscribed_whatsapp)
                otp = body.get("otp", otp)
            except Exception as json_err:
                print(f"JSON parse failed (likely not JSON): {json_err}")
                # Fall back to form data (already parsed)

        # Route-specific logic
        is_register_route = "/simple-register/" in current_path or "/unified" in current_path or "/auth/" in current_path
        is_login_route = "/login/" in current_path

        # Login path (for /login/ route, or if username provided)
        if username and password and is_login_route:
            return await login_user_by_email(username, password)

        # Registration path (for /simple-register/, /unified, /auth/)
        if is_register_route:
            print(f"\n{'='*60}")
            print(f"📝 REGISTRATION REQUEST RECEIVED")
            print(f"{'='*60}")
            if not all([first_name, mobile, password]):
                raise HTTPException(status_code=400, detail={"success": False, "status": 4000, "msg": "Missing required fields for registration"})
            
            # Optional OTP validation (if provided)
            if otp and otp != "0000":  # Example: validate against stored OTP
                raise HTTPException(status_code=400, detail={"success": False, "status": 4005, "msg": "Invalid OTP"})

            if not is_valid_uk_mobile(mobile):
                raise HTTPException(status_code=400, detail={"success": False, "status": 4004, "msg": "Invalid UK mobile number. Use +447XXXXXXXXX or 07XXXXXXXXX"})

            email_to_use = email.strip() if email and email.strip() else None
            mobile_digits = re.sub(r"\D", "", mobile)

            if not email_to_use:
                email_to_use = f"dummy_{mobile_digits}@multifolks.us"

            # Check for duplicates
            existing = users_collection.find_one({
                "$or": [
                    {"email": email_to_use},
                    {"primaryContact": {"$in": [mobile_digits, int(mobile_digits)] if mobile_digits.isdigit() else [mobile_digits]}}
                ]
            })
            if existing:
                raise HTTPException(status_code=400, detail={"success": False, "status": 4003, "msg": "Account already exists. Please login."})

            international_mobile = normalize_mobile(mobile)
            primary_contact = int(mobile_digits) if mobile_digits.isdigit() else mobile_digits

            user_doc = {
                "firstName": first_name.strip(),
                "lastName": last_name.strip() if last_name else "",
                "email": email_to_use,
                "primaryContact": primary_contact,
                "international_mobile": international_mobile,
                "password": hash_password(password),
                "country_code": int(country_code),
                "subscription": True,
                "subscriptions": {"whatsapp": is_subscribed_whatsapp},
                "is_guest_user": False,
                "verify": 0,
                "dnd": 1,
                "my_code": "",
                "additional_features": {"is_email_set": bool(email_to_use and "@" in email_to_use)},
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
                "billing_address": "",
                "shipping_address": "",
                "updateTime": datetime.now(timezone.utc),
            }

            result = users_collection.insert_one(user_doc)
            token = generate_jwt_token(str(result.inserted_id), email_to_use)
            
            print(f"✅ User created successfully: {email_to_use}")
            print(f"   User ID: {result.inserted_id}")
            print(f"   Name: {first_name} {last_name}")

            # Send welcome email
            print(f"\n📧 ATTEMPTING TO SEND WELCOME EMAIL")
            print(f"   Notification service available: {notification_service is not None}")
            
            if notification_service:
                try:
                    user_name = f"{first_name} {last_name}".strip()
                    print(f"   Sending to: {email_to_use}")
                    print(f"   User name: {user_name}")
                    
                    result_email = notification_service.send_welcome_email(email_to_use, user_name, password)
                    
                    print(f"   Email send result: {result_email}")
                    if result_email.get('success'):
                        print(f"   ✅ Welcome email sent successfully!")
                        unique_id = result_email.get('data', {}).get('data', {}).get('unique_id', 'N/A')
                        print(f"   MSG91 Unique ID: {unique_id}")
                    else:
                        print(f"   ❌ Welcome email failed: {result_email.get('msg')}")
                        
                except Exception as e:
                    print(f"   ❌ Exception sending welcome email: {e}")
                    import traceback
                    print(f"   Traceback: {traceback.format_exc()}")
            else:
                print(f"   ⚠️  Notification service not initialized!")
            
            print(f"{'='*60}\n")

            return {
                "success": True,
                "status": 2019,
                "msg": "Registration successful",
                "data": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email_to_use,
                    "mobile": international_mobile,
                    "mobile_international": international_mobile,
                    "is_verified": False,
                    "refer_code": "",
                    "id": str(result.inserted_id),
                    "token": token,
                    "is_new_user": True
                }
            }

        # Fallback if route doesn't match expected logic
        raise HTTPException(status_code=400, detail={"success": False, "status": 4000, "msg": "Invalid request for this endpoint"})

    except HTTPException:
        raise
    except Exception as e:
        print("Unified auth error:", e)
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={"success": False, "status": 4011, "msg": f"Authentication failed due to server error: {str(e)}"}
        )

# ---------- PROFILE ----------
@app.get("/api/profile")
async def get_profile(current_user: dict = Depends(verify_token)):
    return {
        "success": True,
        "data": {
            "id": str(current_user["_id"]),
            "first_name": current_user.get("firstName", ""),
            "last_name": current_user.get("lastName", ""),
            "email": current_user.get("email", ""),
            "contact_number": str(current_user.get("primaryContact", "")),  # Added for frontend compatibility
            "mobile": str(current_user.get("primaryContact", "")),
            "mobile_international": current_user.get("international_mobile", ""),
            "is_verified": current_user.get("is_verified", False),
            "country_code": current_user.get("country_code", 44),
            # Add DOB and gender fields
            "birth_date": current_user.get("birthDate", ""),
            "birth_month": current_user.get("birthMonth", ""),
            "birth_year": current_user.get("birthYear", ""),
            "gender": current_user.get("gender", ""),
            # Add address fields
            "billing_address": current_user.get("billing_address", ""),
            "shipping_address": current_user.get("shipping_address", ""),
        }
    }

@app.put("/api/v1/user/profile")
async def v1_update_profile(request: UpdateProfileRequest, current_user: dict = Depends(verify_token)):
    update_data = {}
    try:
        if request.first_name is not None:
            update_data["firstName"] = request.first_name
        if request.last_name is not None:
            update_data["lastName"] = request.last_name
        # Handle mobile/contact_number (frontend might send either)
        mobile_value = request.mobile or request.contact_number
        if mobile_value is not None:
            if not is_valid_uk_mobile(mobile_value):
                raise HTTPException(status_code=400, detail={"success": False, "status": 4004, "msg": "Invalid UK mobile number"})
            digits = re.sub(r"\\D", "", mobile_value)
            update_data["primaryContact"] = int(digits) if digits.isdigit() else digits
            cc = request.country_code if request.country_code is not None else current_user.get("country_code", 44)
            update_data["international_mobile"] = normalize_mobile(mobile_value)  # Use normalize for UK
            update_data["country_code"] = int(cc)
        elif request.country_code is not None:
            update_data["country_code"] = int(request.country_code)
        
        # Add DOB and gender
        if request.gender is not None:
            update_data["gender"] = request.gender
        if request.birth_date is not None:
            update_data["birthDate"] = request.birth_date
        if request.birth_month is not None:
            update_data["birthMonth"] = request.birth_month
        if request.birth_year is not None:
            update_data["birthYear"] = request.birth_year
            # Mark profile setup as complete when DOB is provided
            update_data["profileSetupComplete"] = True
        
        # Add address fields
        if request.billing_address is not None:
            update_data["billing_address"] = request.billing_address
        if request.shipping_address is not None:
            update_data["shipping_address"] = request.shipping_address
        if request.address is not None:
            update_data["address"] = request.address
        
        # Add email if provided
        if request.email is not None:
            update_data["email"] = request.email
        
        # Add optional business fields (for future use)
        if request.shop_address is not None:
            update_data["shop_address"] = request.shop_address
        if request.store_id is not None:
            update_data["store_id"] = request.store_id
        if request.retail_shop_name is not None:
            update_data["retail_shop_name"] = request.retail_shop_name
        if request.bank_details is not None:
            update_data["bank_details"] = request.bank_details
        if request.gst_number is not None:
            update_data["gst_number"] = request.gst_number
        if request.pan_number is not None:
            update_data["pan_number"] = request.pan_number

        if update_data:
            users_collection.update_one({"_id": current_user["_id"]}, {"$set": {**update_data, "updateTime": datetime.now(timezone.utc)}})
            updated_user = users_collection.find_one({"_id": current_user["_id"]})
            return {
                "success": True,
                "msg": "Profile updated successfully",
                "data": {
                    "first_name": updated_user.get("firstName", ""),
                    "last_name": updated_user.get("lastName", ""),
                    "email": updated_user.get("email", ""),
                    "mobile": str(updated_user.get("primaryContact", "")),
                    "mobile_international": updated_user.get("international_mobile", ""),
                    "country_code": updated_user.get("country_code", 44),
                }
            }
        return {"success": False, "msg": "No data to update"}
    except HTTPException:
        raise
    except Exception as e:
        print("update_profile error:", e)
        raise HTTPException(status_code=500, detail="Failed to update profile")

# ---------- USER PRESCRIPTIONS ----------
@app.get("/api/v1/user/prescriptions")
async def get_user_prescriptions(current_user: dict = Depends(verify_token)):
    """Get all saved prescriptions for the current user"""
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    try:
        user_id = str(current_user['_id'])
        
        # Get prescriptions from user document
        prescriptions = current_user.get('prescriptions', [])
        
        logger.info(f"📋 Fetching prescriptions for user {user_id}")
        logger.info(f"   Found {len(prescriptions)} prescriptions")
        
        # Log prescription details for debugging
        for i, pres in enumerate(prescriptions):
            logger.info(f"   Prescription {i+1}: type={pres.get('type')}, has_image={bool(pres.get('image_url'))}, name={pres.get('name')}")
        
        return {
            "success": True,
            "data": prescriptions
        }
    except Exception as e:
        logger.error(f"Error fetching prescriptions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch prescriptions")

# ---------- PRESCRIPTION IMAGE UPLOAD TO GCS ----------
@app.post("/api/v1/prescriptions/upload-image")
async def upload_prescription_image(
    file: UploadFile = File(...),
    user_id: Optional[str] = Form(None),
    guest_id: Optional[str] = Form(None),
    product_id: Optional[str] = Form(None),  # NEW: Link prescription to product
    request: Request = None
):
    """
    Upload prescription image to Google Cloud Storage
    Returns the public URL of the uploaded image
    
    If product_id is provided, stores prescription as pending for that product
    (will be automatically included when adding product to cart)
    """
    try:
        logger.info(f"📤 Prescription upload request - File: {file.filename}, Content-Type: {file.content_type}, User ID: {user_id}, Guest ID: {guest_id}")
        
        # Validate file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp", "application/pdf"]
        if file.content_type not in allowed_types:
            logger.error(f"❌ Invalid file type: {file.content_type}")
            raise HTTPException(status_code=400, detail=f"Invalid file type '{file.content_type}'. Allowed: {', '.join(allowed_types)}")
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        identifier = user_id if user_id else guest_id if guest_id else unique_id
        
        filename = f"{timestamp}_{unique_id}.{file_extension}"
        gcs_path = f"prescriptions/{identifier}/{filename}"
        
        logger.info(f"📝 Generated GCS path: {gcs_path}")
        
        # Initialize GCS client
        gcs_credentials_path = os.path.join(os.path.dirname(__file__), "gcs-service-account.json")
        logger.info(f"🔑 Looking for GCS credentials at: {gcs_credentials_path}")
        
        if not os.path.exists(gcs_credentials_path):
            logger.error(f"❌ GCS credentials file not found at: {gcs_credentials_path}")
            raise HTTPException(status_code=500, detail="GCS credentials not found. Please contact support.")
        
        logger.info(f"✓ GCS credentials file found")
        
        try:
            storage_client = storage.Client.from_service_account_json(gcs_credentials_path)
            logger.info(f"✓ GCS client initialized")
        except Exception as gcs_error:
            logger.error(f"❌ Failed to initialize GCS client: {str(gcs_error)}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize cloud storage: {str(gcs_error)}")
        
        bucket = storage_client.bucket("myapp-image-bucket-001")
        blob = bucket.blob(gcs_path)
        
        # Upload file
        logger.info(f"⬆️  Uploading file to GCS...")
        file_content = await file.read()
        file_size = len(file_content)
        logger.info(f"📦 File size: {file_size} bytes ({file_size / 1024:.2f} KB)")
        
        if file_size == 0:
            logger.error(f"❌ File is empty")
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        blob.upload_from_string(file_content, content_type=file.content_type)
        logger.info(f"✓ File uploaded to GCS successfully")
        
        # Generate public URL
        public_url = f"https://storage.googleapis.com/myapp-image-bucket-001/{gcs_path}"
        
        logger.info(f"✅ Prescription image uploaded successfully: {public_url}")
        
        # If product_id provided and user is authenticated, store as pending prescription
        response_data = {
            "success": True,
            "url": public_url,
            "filename": filename,
            "path": gcs_path
        }
        
        # Determine which user ID to use (authenticated user takes priority)
        final_user_id = None
        authenticated_user = None
        
        # Try to get authenticated user from token (optional)
        try:
            auth_header = request.headers.get("Authorization") if request else None
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                payload = decode_jwt_token(token)
                email = payload.get("email")
                if email and db_connected:
                    authenticated_user = users_collection.find_one({"email": email})
                    if authenticated_user:
                        final_user_id = str(authenticated_user['_id'])
                        logger.info(f"✅ Using authenticated user ID: {final_user_id}")
        except Exception as e:
            # Auth is optional for this endpoint
            logger.debug(f"Optional auth check failed: {e}")
        
        if not final_user_id and user_id:
            final_user_id = user_id
            logger.info(f"✅ Using form user_id: {final_user_id}")
        
        if product_id and final_user_id and db_connected:
            try:
                prescription_data = {
                    'mode': 'upload',
                    'gcs_url': public_url,
                    'blob_name': gcs_path,
                    'fileName': file.filename,
                    'fileType': file.content_type,
                    'fileSize': file_size,
                    'uploadedAt': datetime.now(timezone.utc).isoformat()
                }
                
                # Convert user_id to ObjectId if it's a string
                try:
                    user_obj_id = ObjectId(final_user_id) if isinstance(final_user_id, str) else final_user_id
                except:
                    # If conversion fails, try to find user by email or other identifier
                    logger.warning(f"⚠️  Could not convert {final_user_id} to ObjectId")
                    user_obj_id = final_user_id
                
                # Store as pending prescription for this product
                update_result = users_collection.update_one(
                    {"_id": user_obj_id},
                    {
                        "$set": {
                            f"pending_prescriptions.{product_id}": prescription_data,
                            "updateTime": datetime.now(timezone.utc)
                        }
                    }
                )
                
                if update_result.matched_count > 0:
                    logger.info(f"✅ Prescription stored as pending for product {product_id}")
                    response_data["message"] = "Prescription uploaded and will be included when adding to cart"
                else:
                    logger.warning(f"⚠️  User not found, prescription uploaded but not linked to product")
            except Exception as e:
                logger.warning(f"⚠️  Failed to store pending prescription: {e}")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error uploading prescription image: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

class SavePrescriptionRequest(BaseModel):
    type: str  # 'upload', 'photo', 'manual'
    data: Dict[str, Any]
    name: str = "My Prescription"
    image_url: Optional[str] = None
    guest_id: Optional[str] = None

@app.post("/api/v1/user/prescriptions")
async def save_user_prescription(request: SavePrescriptionRequest, current_user: dict = Depends(verify_token)):
    """Save a new prescription to user's profile"""
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    try:
        user_id = current_user['_id']
        
        # Create prescription document
        prescription = {
            "type": request.type,
            "data": request.data,
            "name": request.name,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Add image_url if provided (for upload/photo types)
        if request.image_url:
            prescription["image_url"] = request.image_url
        
        # Add prescription to user's prescriptions array
        users_collection.update_one(
            {"_id": user_id},
            {
                "$push": {"prescriptions": prescription},
                "$set": {"updateTime": datetime.now(timezone.utc)}
            }
        )
        
        logger.info(f"✅ Prescription saved for user {user_id}: type={request.type}, has_image={bool(request.image_url)}")
        
        return {
            "success": True,
            "message": "Prescription saved successfully",
            "data": prescription
        }
    except Exception as e:
        logger.error(f"Error saving prescription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save prescription")

# ---------- CART ENDPOINTS (INTEGRATED!) ----------
@app.get("/api/v1/cart")
async def get_cart(current_user: dict = Depends(verify_token)):
    print(f"DEBUG: app.py - get_cart called for user {current_user['_id']}")
    print(f"DEBUG: app.py - get_cart called for user {current_user['_id']}")
    if not cart_service:
        print("DEBUG: app.py - cart_service is None")
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    
    print(f"DEBUG: app.py - calling cart_service.get_cart_summary")
    result = cart_service.get_cart_summary(str(current_user['_id']))
    print(f"DEBUG: app.py - result: {result}")
    return result

@app.post("/api/v1/cart/add")
async def add_to_cart(request: Request, current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    data = await request.json()
    
    # Check if there's a pending prescription for this product_id
    product_id = data.get('product_id') or data.get('product', {}).get('products', {}).get('skuid') or data.get('product', {}).get('products', {}).get('id')
    if product_id and db_connected:
        # Check user document for pending prescription with this product_id
        user = users_collection.find_one({"_id": current_user['_id']})
        if user:
            pending_prescriptions = user.get('pending_prescriptions', {})
            # Try both string and ObjectId key formats
            prescription_data = pending_prescriptions.get(str(product_id)) or pending_prescriptions.get(product_id)
            
            if prescription_data:
                logger.info(f"📋 Found pending prescription for product {product_id}, including in cart item")
                # Include prescription in cart item data (only if not already present)
                if 'prescription' not in data or not data.get('prescription'):
                    data['prescription'] = prescription_data
                    logger.info(f"✅ Added pending prescription to cart item")
                
                # Clear pending prescription after adding to cart
                users_collection.update_one(
                    {"_id": current_user['_id']},
                    {"$unset": {f"pending_prescriptions.{product_id}": ""}}
                )
                logger.info(f"✅ Cleared pending prescription for product {product_id}")
    
    return cart_service.add_to_cart(str(current_user['_id']), data)

@app.put("/api/v1/cart/quantity")
async def update_quantity(cart_id: int, quantity: int, current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")
    return cart_service.update_quantity(str(current_user['_id']), cart_id, quantity)

@app.delete("/api/v1/cart/item/{cart_id}")
async def remove_item(cart_id: int, current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    return cart_service.remove_item(str(current_user['_id']), cart_id)

@app.delete("/api/v1/cart/clear")
async def clear_cart(current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    return cart_service.clear_cart(str(current_user['_id']))

class ApplyCouponRequest(BaseModel):
    code: str

class UpdateShippingRequest(BaseModel):
    method_id: str

@app.post("/api/v1/cart/coupon")
async def apply_coupon(request: ApplyCouponRequest, current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    return cart_service.apply_coupon(str(current_user['_id']), request.code)

@app.delete("/api/v1/cart/coupon")
async def remove_coupon(current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    return cart_service.remove_coupon(str(current_user['_id']))

@app.put("/api/v1/cart/shipping")
async def update_shipping(request: UpdateShippingRequest, current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    return cart_service.update_shipping_method(str(current_user['_id']), request.method_id)

class UpdateLensRequest(BaseModel):
    cart_id: int
    lens_data: Dict[str, Any]

class UpdatePrescriptionRequest(BaseModel):
    cart_id: int
    prescription_data: Dict[str, Any]

@app.put("/api/v1/cart/lens")
async def update_cart_lens(request: UpdateLensRequest, current_user: dict = Depends(verify_token)):
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    return cart_service.update_lens(str(current_user['_id']), request.cart_id, request.lens_data)

@app.put("/api/v1/cart/prescription")
async def update_cart_prescription(
    request: Request,
    cart_id: int = Form(...),
    mode: str = Form("upload"),
    prescription_data: Optional[str] = Form(None),
    current_user: dict = Depends(verify_token)
):
    """
    Update cart with prescription - supports both file upload and manual entry
    
    For file upload (mode='upload'):
        - prescription_file: File to upload
        - Uploads to GCS and stores URL
    
    For manual entry (mode='manual'):
        - prescription_data: JSON string with prescription details
    """
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    
    try:
        from prescription_gcs_service import upload_prescription_to_gcs
        
        # Handle file upload mode
        if mode == "upload":
            # Get file from request
            form_data = await request.form()
            file = form_data.get('prescription_file')
            
            if not file:
                raise HTTPException(status_code=400, detail="No prescription file provided")
            
            # Upload to GCS
            upload_result = upload_prescription_to_gcs(
                file.file,
                str(current_user['_id']),
                cart_id,
                file.filename  # Pass filename explicitly
            )
            
            if not upload_result['success']:
                raise HTTPException(
                    status_code=500,
                    detail=upload_result.get('error', 'Failed to upload prescription')
                )
            
            # Prepare prescription data with GCS URL
            prescription_dict = {
                'mode': 'upload',
                'gcs_url': upload_result['gcs_url'],
                'blob_name': upload_result['blob_name'],
                'fileName': file.filename,
                'fileType': upload_result['format'],
                'fileSize': upload_result['size'],
                'uploadedAt': upload_result['uploaded_at']
            }
            
            # Update cart
            result = cart_service.update_prescription(
                str(current_user['_id']),
                cart_id,
                prescription_dict
            )
            
            # Add GCS URL to response
            if result.get('success'):
                result['gcs_url'] = upload_result['gcs_url']
            
            return result
            
        elif mode == "manual":
            # Handle manual prescription entry
            if not prescription_data:
                raise HTTPException(status_code=400, detail="prescription_data required for manual mode")
            
            import json
            prescription_dict = json.loads(prescription_data) if isinstance(prescription_data, str) else prescription_data
            prescription_dict['mode'] = 'manual'
            
            return cart_service.update_prescription(
                str(current_user['_id']),
                cart_id,
                prescription_dict
            )
        else:
            raise HTTPException(status_code=400, detail=f"Invalid mode: {mode}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating prescription: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to update prescription: {str(e)}")


class MergeGuestCartRequest(BaseModel):
    guest_id: str

@app.post("/api/v1/cart/merge-guest-cart")
async def merge_guest_cart(request: MergeGuestCartRequest, current_user: dict = Depends(verify_token)):
    """
    Merge guest cart items into authenticated user's cart after login.
    This endpoint is called by the frontend after successful authentication.
    """
    if not cart_service:
        raise HTTPException(status_code=503, detail="Cart service unavailable")
    
    try:
        logger.info(f"🔄 Merging guest cart {request.guest_id} into user {current_user['_id']}")
        
        # Get guest cart items
        guest_cart = cart_service.get_cart_summary(request.guest_id)
        
        if not guest_cart.get('success') or not guest_cart.get('cart'):
            logger.info(f"✅ No items in guest cart {request.guest_id} to merge")
            return {"success": True, "message": "No items to merge", "items_merged": 0}
        
        guest_items = guest_cart['cart']  # Changed from 'items' to 'cart'
        user_id = str(current_user['_id'])
        items_merged = 0
        
        logger.info(f"📦 Found {len(guest_items)} items in guest cart to merge")
        
        # Add each guest item to user's cart
        for item in guest_items:
            try:
                # Prepare item data for adding to cart
                item_data = {
                    'product_id': item.get('product', {}).get('products', {}).get('skuid') or item.get('product', {}).get('products', {}).get('id'),
                    'name': item.get('product', {}).get('products', {}).get('name'),
                    'image': item.get('product', {}).get('products', {}).get('image'),
                    'price': item.get('product', {}).get('products', {}).get('list_price', 0),
                    'quantity': item.get('quantity', 1),
                    'product': item.get('product'),
                    'lens': item.get('lens'),
                    'prescription': item.get('prescription'),
                    'flag': item.get('flag', 'normal')
                }
                
                logger.info(f"   Adding item: {item_data.get('name')} (qty: {item_data.get('quantity')})")
                cart_service.add_to_cart(user_id, item_data)
                items_merged += 1
            except Exception as e:
                logger.error(f"❌ Failed to merge item: {e}")
                continue
        
        # Clear guest cart after successful merge
        try:
            cart_service.clear_cart(request.guest_id)
            logger.info(f"🗑️  Cleared guest cart {request.guest_id}")
        except Exception as e:
            logger.warning(f"⚠️  Failed to clear guest cart: {e}")
        
        logger.info(f"✅ Successfully merged {items_merged} items from guest cart")
        return {
            "success": True,
            "message": f"Successfully merged {items_merged} items",
            "items_merged": items_merged
        }
        
    except Exception as e:
        logger.error(f"❌ Error merging guest cart: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to merge cart: {str(e)}")


# ---------- ORDER ENDPOINTS ----------
class CreateOrderRequest(BaseModel):
    cart_items: List[Dict[str, Any]]
    payment_data: Dict[str, Any]
    shipping_address: str
    billing_address: str
    metadata: Optional[Dict[str, Any]] = None

@app.post("/api/v1/orders")
async def create_order(request: CreateOrderRequest, current_user: dict = Depends(verify_token)):
    """
    Create a new order
    
    Request body:
    {
        "cart_items": [...],  # Cart items from cart service
        "payment_data": {
            "pay_mode": "Stripe / Online",
            "payment_status": "Success",
            "transaction_id": "txn_xxx",
            "payment_intent_id": "pi_xxx",
            "is_partial": false
        },
        "shipping_address": "123 Main St, London, UK",
        "billing_address": "123 Main St, London, UK",
        "metadata": {}  # Optional
    }
    """
    if not order_service:
        raise HTTPException(status_code=503, detail="Order service unavailable")
    
    try:
        user_id = str(current_user['_id'])
        user_email = current_user.get('email', '')
        
        # Get discount and shipping from cart
        discount_amount = 0.0
        shipping_cost = 0.0
        if cart_service:
            cart_res = cart_service.get_cart_summary(user_id)
            if cart_res.get('success'):
                discount_amount = float(cart_res.get('discount_amount', 0))
                shipping_cost = float(cart_res.get('shipping_cost', 0))
        
        result = order_service.create_order(
            user_id=user_id,
            user_email=user_email,
            cart_items=request.cart_items,
            payment_data=request.payment_data,
            shipping_address=request.shipping_address,
            billing_address=request.billing_address,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
            metadata=request.metadata
        )
        
        # Send order confirmation email
        if result.get('success') and notification_service:
            try:
                user_name = f"{current_user.get('firstName', '')} {current_user.get('lastName', '')}".strip() or "Customer"
                order_id = result.get('order_id', 'N/A')
                # Calculate total from cart items
                total = sum(item.get('total_price', 0) for item in request.cart_items)
                notification_service.send_order_confirmation(
                    user_email, 
                    order_id, 
                    f"£{total:.2f}",
                    user_name
                )
                print(f"DEBUG: Sent order confirmation email to {user_email}")
            except Exception as e:
                print(f"WARNING: Failed to send order confirmation email: {e}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error creating order: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@app.get("/api/v1/orders")
async def get_user_orders(current_user: dict = Depends(verify_token)):
    """
    Get all orders for the authenticated user
    """
    if not order_service:
        raise HTTPException(status_code=503, detail="Order service unavailable")
    
    try:
        user_id = str(current_user['_id'])
        result = order_service.get_user_orders(user_id)
        return result
        
    except Exception as e:
        logger.error(f"❌ Error fetching orders: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch orders: {str(e)}")

@app.get("/api/v1/orders/{order_id}")
async def get_order_details(order_id: str, current_user: dict = Depends(verify_token)):
    """
    Get details for a specific order
    """
    if not order_service:
        raise HTTPException(status_code=503, detail="Order service unavailable")
    
    try:
        user_id = str(current_user['_id'])
        result = order_service.get_order_by_id(order_id, user_id)
        
        if not result.get('success'):
            raise HTTPException(status_code=404, detail="Order not found")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch order: {str(e)}")

@app.get("/api/v1/orders/thank-you/{order_id}")
async def get_thank_you_data(order_id: str, current_user: dict = Depends(verify_token)):
    """
    Get order data for thank you page
    This endpoint is used by OrderView.tsx
    """
    if not order_service:
        raise HTTPException(status_code=503, detail="Order service unavailable")
    
    try:
        user_id = str(current_user['_id'])
        result = order_service.get_order_by_id(order_id, user_id)
        
        if not result.get('success'):
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Return in the format expected by frontend
        return {
            "status": True,
            "order": result.get('order'),
            "shipping_address": result.get('order', {}).get('shipping_address'),
            "billing_address": result.get('order', {}).get('billing_address')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching thank you data for order {order_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch order data: {str(e)}")


# ---------- PAYMENT ENDPOINTS ----------

@app.post("/api/v1/payment/create-session")
async def create_payment_session(request: CreatePaymentSessionRequest, current_user: dict = Depends(verify_token)):
    """
    Create Stripe Checkout Session AND Create Pending Order
    
    Request:
    - order_id: str (Frontend generated, will be replaced/mapped to backend ID)
    - amount: float
    - metadata: dict (contains address, customer_id, etc.)
    """
    if not payment_service or not order_service:
        raise HTTPException(status_code=503, detail="Payment or Order service unavailable")
    
    try:
        user_id = str(current_user['_id'])
        user_email = current_user.get('email', '')
        
        # 1. Prepare Order Data
        # Parse items from metadata if possible, otherwise use empty list (simulated)
        # Ideally frontend should send items, but CreatePaymentSessionRequest might not have them
        # We'll try to get items from cart service if not in metadata
        
        items = []
        discount_amount = 0.0  # Initialize discount
        shipping_cost = 0.0  # Initialize shipping
        if cart_service:
             # Fetch current cart items to save in order
             logger.info(f"🛒 Fetching cart for user {user_id}")
             cart_res = cart_service.get_cart_summary(user_id)
             logger.info(f"🛒 Cart response success: {cart_res.get('success')}")
             if cart_res.get('success'):
                 items = cart_res.get('cart', [])  # Fixed: cart_service returns 'cart', not 'items'
                 discount_amount = float(cart_res.get('discount_amount', 0))  # Get discount from cart
                 shipping_cost = float(cart_res.get('shipping_cost', 0))  # Get shipping from cart
                 
                 logger.info(f"📦 Cart items count: {len(items)}")
                 logger.info(f"💰 Cart pricing - Discount: £{discount_amount}, Shipping: £{shipping_cost}")
                 
                 # Warn if shipping or discount are zero
                 if shipping_cost == 0:
                     logger.warning(f"⚠️  Shipping cost is £0 for user {user_id}")
                     logger.warning(f"   Cart has shipping_method: {cart_res.get('shipping_method')}")
                     logger.warning(f"   Subtotal: £{cart_res.get('subtotal', 0)} (Free shipping threshold: £75)")
                     if cart_res.get('subtotal', 0) > 75:
                         logger.info(f"   ✅ Free shipping applied (subtotal > £75)")
                 
                 if discount_amount == 0:
                     logger.warning(f"⚠️  Discount is £0 for user {user_id}")
                     logger.warning(f"   Cart has coupon: {cart_res.get('coupon')}")
                     if not cart_res.get('coupon'):
                         logger.info(f"   ℹ️  No coupon applied - this is normal if user didn't enter a code")
                 
                 # Log each cart item's pricing details
                 for idx, item in enumerate(items):
                     logger.info(f"  Item {idx + 1}: {item.get('product', {}).get('products', {}).get('name', 'Unknown')}")
                     logger.info(f"    Frame Price: £{item.get('product', {}).get('products', {}).get('list_price', 0)}")
                     logger.info(f"    Lens Price: £{item.get('lens', {}).get('selling_price', 0)}")
                     logger.info(f"    Tint Price: £{item.get('lens', {}).get('tint_price', 0)}")
                     logger.info(f"    Coating Price: £{item.get('lens', {}).get('coating_price', 0)}")
                     logger.info(f"    Quantity: {item.get('quantity', 1)}")
        
        # Parse address
        import json
        address_shipping = ""
        address_billing = ""
        metadata = request.metadata or {}
        
        if 'address' in metadata:
            try:
                addr_data = json.loads(metadata['address']) if isinstance(metadata['address'], str) else metadata['address']
                # Format address string
                if isinstance(addr_data, dict):
                    parts = [
                        addr_data.get('addressLine'),
                        addr_data.get('city'),
                        addr_data.get('state'),
                        addr_data.get('zip'),
                        addr_data.get('country')
                    ]
                    address_shipping = ", ".join([p for p in parts if p])
                    address_billing = address_shipping # Assume same for now
            except:
                pass
        
        logger.info(f"📍 Shipping Address: {address_shipping}")
        logger.info(f"📍 Billing Address: {address_billing}")
                
        # 2. Create Order in Database (Status: Pending)
        logger.info(f"🔨 Creating order with {len(items)} items, discount: £{discount_amount}, shipping: £{shipping_cost}")
        order_res = order_service.create_order(
            user_id=user_id,
            user_email=user_email,
            cart_items=items,
            payment_data={
                "pay_mode": "Stripe / Online",
                "payment_status": "Pending", 
                "is_partial": False
            },
            shipping_address=address_shipping,
            billing_address=address_billing,
            discount_amount=discount_amount,  # Pass discount to order
            shipping_cost=shipping_cost,  # Pass shipping to order
            metadata=metadata
        )

        
        if not order_res.get('success'):
             raise HTTPException(status_code=500, detail="Failed to create pending order")
        
        # Use the Backend Generated Order ID
        backend_order_id = order_res['order_id']
        
        # 3. Create Stripe Session
        session_res = payment_service.create_checkout_session(
            order_id=backend_order_id,
            amount=request.amount,
            user_email=user_email,
            user_id=user_id,
            metadata={
                **metadata,
                "backend_order_id": backend_order_id # Ensure webhook uses this
            }
        )
        
        return session_res
        
    except Exception as e:
        logger.error(f"❌ Error creating payment session: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


# ---------- WEBHOOK ----------
@app.post("/api/v1/payment/webhook")
async def stripe_webhook(request: Request):
    if not payment_service:
        raise HTTPException(status_code=503, detail="Payment service unavailable")
    import stripe
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, config.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.payment_status == "paid":
            payment_service.confirm_payment(session.id)
    elif event.type == "checkout.session.expired":
        session = event.data.object
        payment_service.payments_collection.update_one(
            {"session_id": session.id},
            {"$set": {"status": "expired", "expired_at": datetime.now(timezone.utc)}}
        )
    return {"success": True}

# ---------- PAYMENT ENDPOINTS ----------
@app.post("/api/v1/payment/create-session")
async def create_payment_session(request: CreatePaymentSessionRequest, current_user: dict = Depends(verify_token)):
    if not payment_service:
        raise HTTPException(status_code=503, detail="Payment service unavailable")
    
    # Ensure user_id matches token
    user_id = str(current_user['_id'])
    user_email = current_user['email']
    
    result = payment_service.create_checkout_session(
        order_id=request.order_id,
        amount=request.amount,
        user_email=user_email,
        user_id=user_id,
        metadata=request.metadata
    )
    
    if not result.get('success'):
        raise HTTPException(status_code=400, detail=result)
        
    return result

# ---------- DELIVERY ENDPOINTS ----------
@app.post("/api/v1/delivery/check-pincode")
async def check_pincode(request: CheckPincodeRequest):
    if not delivery_service:
        raise HTTPException(status_code=503, detail="Delivery service unavailable")
    
    return delivery_service.bluedart.check_pincode_serviceability(request.pincode)

@app.post("/api/v1/delivery/create-shipment")
async def create_shipment(request: CreateShipmentRequest, current_user: dict = Depends(verify_token)):
    if not delivery_service:
        raise HTTPException(status_code=503, detail="Delivery service unavailable")
        
    # Ideally verify order ownership here
    
    return delivery_service.create_shipment(request.order_id, request.customer_details)

@app.get("/api/v1/delivery/track/{awb_number}")
async def track_shipment(awb_number: str):
    if not delivery_service:
        raise HTTPException(status_code=503, detail="Delivery service unavailable")
        
    return delivery_service.get_shipment_status(awb_number)

    return delivery_service.get_shipment_status(awb_number)

# ---------- PRODUCT ENDPOINTS ----------
class Product(BaseModel):
    skuid: str
    name: str
    brand: Optional[str] = None
    style: Optional[str] = None
    size: Optional[str] = None
    price: float
    color_names: List[str] = []
    primary_category: Optional[str] = None
    secondary_category: Optional[str] = None
    material: Optional[str] = None
    gender: Optional[str] = None
    comfort: List[str] = []
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True

class ProductCreate(BaseModel):
    """Model for creating/updating products"""
    skuid: str
    name: str
    naming_system: Optional[str] = None
    brand: Optional[str] = None
    price: float
    list_price: Optional[float] = None
    description: Optional[str] = None
    image: Optional[str] = None
    images: Optional[List[str]] = []
    colors: Optional[List[str]] = []
    color_names: Optional[List[str]] = []
    framecolor: Optional[str] = None
    style: Optional[str] = None
    gender: Optional[str] = None
    size: Optional[str] = None
    material: Optional[str] = None
    shape: Optional[str] = None
    features: Optional[List[str]] = []
    variants: Optional[List[Dict[str, Any]]] = []
    sizes: Optional[List[str]] = []
    primary_category: Optional[str] = None
    secondary_category: Optional[str] = None
    comfort: Optional[List[str]] = []
    is_active: bool = True

@app.get("/api/v1/products")
async def get_products(
    page: int = 1, 
    limit: int = 20, 
    category: Optional[str] = None,
    brand: Optional[str] = None,
    gender: Optional[str] = None,
    search: Optional[str] = None,
    material: Optional[str] = None,  # NEW: Filter by material
    style: Optional[str] = None,  # NEW: Filter by style (Full Frame, Half Frame, Rimless)
    comfort: Optional[str] = None,  # NEW: Filter by comfort features
    size: Optional[str] = None,  # NEW: Filter by size
    min_price: Optional[float] = None,  # NEW: Minimum price
    max_price: Optional[float] = None,  # NEW: Maximum price
    frame_color: Optional[str] = None,  # NEW: Filter by frame color
    shape: Optional[str] = None,  # NEW: Filter by shape
):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")

    
    query = {"is_active": True}
    
    # Existing filters
    if category:
        query["primary_category"] = {"$regex": category, "$options": "i"}
    if brand:
        query["brand"] = {"$regex": brand, "$options": "i"}
    if gender:
        query["gender"] = {"$regex": gender, "$options": "i"}
    
    # NEW: Material filter
    if material:
        query["material"] = {"$regex": material, "$options": "i"}
    
    # NEW: Style filter
    if style:
        query["style"] = {"$regex": style, "$options": "i"}
    
    # NEW: Comfort filter (array field)
    if comfort:
        query["comfort"] = {"$in": [comfort]}
    
    # NEW: Size filter
    if size:
        query["size"] = {"$regex": size, "$options": "i"}
    
    # NEW: Price range filter
    if min_price is not None or max_price is not None:
        price_query = {}
        if min_price is not None:
            price_query["$gte"] = min_price
        if max_price is not None:
            price_query["$lte"] = max_price
        if price_query:
            query["price"] = price_query
    
    # NEW: Frame color filter
    if frame_color:
        query["frame_color"] = {"$regex": frame_color, "$options": "i"}
    
    # NEW: Shape filter (exact match for better accuracy)
    if shape:
        query["shape"] = shape
    
    # Search query
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"skuid": {"$regex": search, "$options": "i"}},
            {"brand": {"$regex": search, "$options": "i"}},
            {"naming_system": {"$regex": search, "$options": "i"}}
        ]
        
    products_collection = db['products']
    total = products_collection.count_documents(query)
    cursor = products_collection.find(query).skip((page - 1) * limit).limit(limit)
    
    products = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        products.append(doc)
        
    return {
        "success": True,
        "data": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }

@app.get("/api/v1/products/{product_id}")
async def get_product_by_id(product_id: str):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
        
    try:
        products_collection = db['products']
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        product["_id"] = str(product["_id"])
        return {"success": True, "data": product}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid product ID")

@app.get("/api/v1/products/sku/{sku}")
async def get_product_by_sku(sku: str):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
        
    products_collection = db['products']
    product = products_collection.find_one({"skuid": sku})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    product["_id"] = str(product["_id"])
    return {"success": True, "data": product}

@app.post("/api/v1/products/create")
async def create_product(product: ProductCreate, current_user: dict = Depends(verify_token)):
    """
    Create or update a product in the database.
    Uses upsert - will create new product or update existing one with same SKU.
    Requires authentication.
    """
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    try:
        products_collection = db['products']
        
        # Prepare product data
        product_data = {
            "skuid": product.skuid,
            "name": product.name,
            "naming_system": product.naming_system or product.skuid,
            "brand": product.brand or "",
            "price": float(product.price),
            "list_price": float(product.list_price) if product.list_price else None,
            "description": product.description or "",
            "image": product.image or "",
            "images": product.images or [],
            "colors": product.colors or [],
            "color_names": product.color_names or [],
            "framecolor": product.framecolor or "",
            "style": product.style or "",
            "gender": product.gender or "",
            "size": product.size or "",
            "material": product.material or "",
            "shape": product.shape or "",
            "features": product.features or [],
            "variants": product.variants or [],
            "sizes": product.sizes or [],
            "primary_category": product.primary_category or "",
            "secondary_category": product.secondary_category or "",
            "comfort": product.comfort or [],
            "is_active": product.is_active
        }
        
        # Remove None values
        product_data = {k: v for k, v in product_data.items() if v is not None}
        
        # Upsert product (create if doesn't exist, update if exists)
        result = products_collection.update_one(
            {"skuid": product.skuid},
            {"$set": product_data},
            upsert=True
        )
        
        # Get the created/updated product
        created_product = products_collection.find_one({"skuid": product.skuid})
        if created_product:
            created_product["_id"] = str(created_product["_id"])
        
        if result.upserted_id:
            logger.info(f"✅ Created new product: {product.skuid}")
            return {
                "success": True,
                "message": "Product created successfully",
                "data": created_product
            }
        else:
            logger.info(f"✅ Updated existing product: {product.skuid}")
            return {
                "success": True,
                "message": "Product updated successfully",
                "data": created_product
            }
            
    except Exception as e:
        logger.error(f"❌ Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")

@app.get("/api/v1/public/products")
async def get_public_products(
    page: int = 1,
    limit: int = 100,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    gender: Optional[str] = None,
    search: Optional[str] = None
):
    return await get_products(page, limit, category, brand, gender, search)

@app.get("/retailer/product-inventory")
async def get_product_inventory(
    page: int = 1, 
    limit: int = 20, 
    category: Optional[str] = None,
    brand: Optional[str] = None,
    gender: Optional[str] = None, # Added gender filter
    search: Optional[str] = None,
    material: Optional[str] = None,
    style: Optional[str] = None,
    comfort: Optional[str] = None,
    size: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    frame_color: Optional[str] = None,
    shape: Optional[str] = None,  # NEW: Shape filter
):
    # Enhanced to support all filter parameters
    return await get_products(
        page, limit, category, brand, gender, search,
        material, style, comfort, size, min_price, max_price, frame_color, shape
    )


# ---------- FILTER OPTIONS ENDPOINT ----------
@app.get("/api/v1/products/filters/options")
async def get_filter_options():
    """
    Get all available filter options from the database
    Returns unique values for each filterable field
    """
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    products_collection = db['products']
    
    # Get unique values for each filter field
    brands = products_collection.distinct("brand")
    genders = products_collection.distinct("gender")
    materials = products_collection.distinct("material")
    styles = products_collection.distinct("style")
    sizes = products_collection.distinct("size")
    frame_colors = products_collection.distinct("frame_color")
    
    # Get all unique comfort features (since it's an array field)
    comfort_pipeline = [
        {"": ""},
        {"": {"_id": ""}},
        {"": {"_id": 1}}
    ]
    comfort_results = list(products_collection.aggregate(comfort_pipeline))
    comfort_options = [r["_id"] for r in comfort_results if r["_id"]]
    
    # Get price range
    price_pipeline = [
        {"": {
            "_id": None,
            "min_price": {"": ""},
            "max_price": {"": ""}
        }}
    ]
    price_result = list(products_collection.aggregate(price_pipeline))
    price_range = price_result[0] if price_result else {"min_price": 0, "max_price": 500}
    
    return {
        "success": True,
        "data": {
            "brands": sorted([b for b in brands if b]),
            "genders": sorted([g for g in genders if g]),
            "materials": sorted([m for m in materials if m]),
            "styles": sorted([s for s in styles if s]),
            "sizes": sorted([sz for sz in sizes if sz]),
            "frame_colors": sorted([fc for fc in frame_colors if fc]),
            "comfort": sorted(comfort_options),
            "price_range": {
                "min": price_range.get("min_price", 0),
                "max": price_range.get("max_price", 500)
            }
        }
    }

# ---------- PIN AUTHENTICATION ----------
class RequestPinRequest(BaseModel):
    email: EmailStr

class LoginWithPinRequest(BaseModel):
    email: EmailStr
    pin: str

@app.post("/api/v1/auth/request-pin")
async def request_pin(request: RequestPinRequest):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    user = users_collection.find_one({"email": request.email})
    if not user:
        # For security, don't reveal if user exists, but for now we'll return success
        # In a real app, we might want to send a generic "If your email is registered..."
        return {"success": True, "msg": "If your email is registered, a PIN has been sent."}
    
    # Generate 6-digit PIN
    import random
    pin = str(random.randint(100000, 999999))
    print(f"DEBUG: Generated PIN for {request.email}: {pin}")
    
    # Store PIN with expiry (e.g., 15 minutes)
    expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"pin": pin, "pin_expiry": expiry}}
    )
    
    # Send PIN via MSG91
    if notification_service:
        user_name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() or None
        notification_service.send_login_pin(request.email, pin, user_name)
        print(f"DEBUG: Sent PIN via MSG91 to {request.email}")
    else:
        print(f"DEBUG: MSG91 not configured. Generated PIN for {request.email}: {pin}")
    
    return {"success": True, "msg": "PIN sent successfully"}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    pin: str
    new_password: str

@app.post("/api/v1/auth/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    # Normalize email
    email = request.email.lower().strip()
    
    user = users_collection.find_one({"email": email})
    if not user:
        # Return success to prevent email enumeration
        return {"success": True, "msg": "If your email is registered, a reset PIN has been sent."}
    
    # Generate 6-digit PIN
    import random
    pin = str(random.randint(100000, 999999))
    
    # Store PIN with expiry
    expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Update with verification
    result = users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "reset_pin": pin, 
            "reset_pin_expiry": expiry,
            "reset_pin_created_at": datetime.now(timezone.utc)
        }}
    )
    
    # Log the update result
    print(f"DEBUG: Update result for {email} - matched: {result.matched_count}, modified: {result.modified_count}")
    
    # Verify the PIN was stored
    updated_user = users_collection.find_one({"_id": user["_id"]})
    if updated_user.get("reset_pin"):
        print(f"DEBUG: Successfully stored reset_pin for {email}")
    else:
        print(f"ERROR: Failed to store reset_pin for {email}")
        raise HTTPException(status_code=500, detail="Failed to generate reset code")
    
    # Send PIN via MSG91 with error handling
    try:
        if notification_service:
            user_name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip() or None
            notification_service.send_password_reset_pin(email, pin, user_name)
            print(f"DEBUG: Sent Reset PIN via MSG91 to {email}")
        else:
            print(f"DEBUG: MSG91 not configured. Generated Reset PIN for {email}: {pin}")
    except Exception as e:
        print(f"ERROR: Failed to send notification to {email}: {e}")
        # Don't fail the request - PIN is still stored in DB
    
    return {"success": True, "msg": "Reset instructions sent successfully"}


@app.post("/api/v1/auth/reset-password")
async def reset_password(request: ResetPasswordRequest):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    # Normalize email
    email = request.email.lower().strip()
    
    user = users_collection.find_one({"email": email})
    if not user:
        print(f"DEBUG: User not found for email: {email}")
        raise HTTPException(status_code=400, detail={"success": False, "msg": "Invalid credentials"})
    
    stored_pin = user.get("reset_pin")
    pin_expiry = user.get("reset_pin_expiry")
    
    # Enhanced debugging
    print(f"DEBUG: Reset attempt for {email}")
    print(f"DEBUG: Has reset_pin: {bool(stored_pin)}")
    print(f"DEBUG: Has pin_expiry: {bool(pin_expiry)}")
    print(f"DEBUG: User ID: {user['_id']}")
    
    if not stored_pin or not pin_expiry:
        print(f"ERROR: Missing PIN data for {email}")
        print(f"DEBUG: All user fields: {list(user.keys())}")
        raise HTTPException(
            status_code=400, 
            detail={
                "success": False, 
                "msg": "No reset requested or PIN expired. Please request a new reset PIN."
            }
        )
    
    # Ensure pin_expiry is timezone-aware
    if pin_expiry.tzinfo is None:
        pin_expiry = pin_expiry.replace(tzinfo=timezone.utc)
    
    current_time = datetime.now(timezone.utc)
    print(f"DEBUG: Current time: {current_time}, PIN expiry: {pin_expiry}")
    
    if current_time > pin_expiry:
        print(f"ERROR: PIN expired for {email}")
        raise HTTPException(
            status_code=400, 
            detail={
                "success": False, 
                "msg": "PIN expired. Please request a new reset PIN."
            }
        )
    
    if stored_pin != request.pin:
        print(f"ERROR: Invalid PIN provided for {email}")
        raise HTTPException(
            status_code=400, 
            detail={
                "success": False, 
                "msg": "Invalid PIN"
            }
        )
    
    # Update password and clear PIN
    hashed_password = hash_password(request.new_password)
    users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "password": hashed_password, 
                "updateTime": datetime.now(timezone.utc)
            },
            "$unset": {
                "reset_pin": "", 
                "reset_pin_expiry": "",
                "reset_pin_created_at": ""
            }
        }
    )
    
    print(f"DEBUG: Password reset successful for {email}")
    
    return {"success": True, "msg": "Password reset successfully. Please login."}


# Optional: Add endpoint to check reset status (for debugging)
@app.get("/api/v1/auth/debug/reset-status/{email}")
async def debug_reset_status(email: str):
    """Debug endpoint - remove in production"""
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    email = email.lower().strip()
    user = users_collection.find_one({"email": email})
    
    if not user:
        return {"found": False}
    
    return {
        "found": True,
        "has_reset_pin": bool(user.get("reset_pin")),
        "has_reset_expiry": bool(user.get("reset_pin_expiry")),
        "pin_expired": datetime.now(timezone.utc) > user.get("reset_pin_expiry", datetime.min.replace(tzinfo=timezone.utc)) if user.get("reset_pin_expiry") else None,
        "fields": list(user.keys())
    }

    
@app.post("/api/v1/auth/login-with-pin")
async def login_with_pin(request: LoginWithPinRequest):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
        
    user = users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=400, detail={"success": False, "msg": "Invalid credentials"})
        
    stored_pin = user.get("pin")
    pin_expiry = user.get("pin_expiry")
    
    if not stored_pin or not pin_expiry:
        raise HTTPException(status_code=400, detail={"success": False, "msg": "No PIN requested or PIN expired"})
        
    # Ensure pin_expiry is timezone-aware
    if pin_expiry.tzinfo is None:
        pin_expiry = pin_expiry.replace(tzinfo=timezone.utc)
        
    if datetime.now(timezone.utc) > pin_expiry:
        raise HTTPException(status_code=400, detail={"success": False, "msg": "PIN expired"})
        
    if stored_pin != request.pin:
        raise HTTPException(status_code=400, detail={"success": False, "msg": "Invalid PIN"})
        
    # Clear PIN after successful login
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$unset": {"pin": "", "pin_expiry": ""}, "$set": {"updateTime": datetime.now(timezone.utc)}}
    )
    
    token = generate_jwt_token(str(user["_id"]), user["email"])
    return {
        "success": True,
        "status": 200,
        "msg": "Login successful",
        "data": {
            "first_name": user.get("firstName", ""),
            "last_name": user.get("lastName", ""),
            "email": user["email"],
            "mobile": str(user.get("primaryContact", "")),
            "mobile_international": user.get("international_mobile", ""),
            "is_verified": user.get("is_verified", False),
            "refer_code": user.get("my_code", ""),
            "id": str(user["_id"]),
            "token": token,
            "is_new_user": False
        }
    }

# ---------- HEALTH ----------
@app.get("/api/health")
@app.get("/health")
async def health_check():
    user_count = users_collection.count_documents({}) if db_connected else None
    return {
        "success": True,
        "message": "API is running",
        "mongodb": "connected" if db_connected else "disconnected",
        "total_users": user_count,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# ---------- RECENTLY VIEWED ----------
class RecentlyViewedRequest(BaseModel):
    product_id: str

@app.get("/api/v1/products/recently-viewed")
async def get_recently_viewed(token: str = Depends(security)):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    try:
        payload = jwt.decode(token.credentials, config.SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("sub")
        
        user = users_collection.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        recently_viewed_ids = user.get("recently_viewed", [])
        
        # Fetch product details (Mocking product fetch for now as product collection structure isn't fully defined in context)
        # In a real scenario, you would query the products collection
        # products = db.products.find({"skuid": {"$in": recently_viewed_ids}})
        
        return {
            "success": True, 
            "data": recently_viewed_ids # Returning IDs for now, frontend can fetch details or we can expand this
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Error fetching recently viewed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/products/recently-viewed")
async def add_recently_viewed(request: RecentlyViewedRequest, token: str = Depends(security)):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
        
    try:
        payload = jwt.decode(token.credentials, config.SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("sub")
        
        # Add to set to avoid duplicates, keep only last 10
        users_collection.update_one(
            {"email": user_email},
            {
                "$addToSet": {"recently_viewed": request.product_id}
            }
        )
        
        # Optional: Limit to last 10 (requires more complex query or pull)
        
        return {"success": True, "msg": "Added to recently viewed"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        print(f"Error adding recently viewed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ---------- PRESCRIPTIONS ----------
class PrescriptionData(BaseModel):
    type: str # 'manual', 'upload', 'photo'
    data: Dict[str, Any]
    name: Optional[str] = "My Prescription"

@app.get("/api/v1/user/prescriptions")
async def get_prescriptions(token: str = Depends(security)):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
        
    try:
        payload = jwt.decode(token.credentials, config.SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("sub")
        
        user = users_collection.find_one({"email": user_email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        prescriptions = user.get("saved_prescriptions", [])
        
        return {"success": True, "data": prescriptions}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        print(f"Error fetching prescriptions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/user/prescriptions")
async def save_prescription(request: PrescriptionData, token: str = Depends(security)):
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
        
    try:
        payload = jwt.decode(token.credentials, config.SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("sub")
        
        prescription_entry = {
            "id": str(ObjectId()),
            "type": request.type,
            "data": request.data,
            "name": request.name,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        users_collection.update_one(
            {"email": user_email},
            {"$push": {"saved_prescriptions": prescription_entry}}
        )
        
        return {"success": True, "msg": "Prescription saved", "id": prescription_entry["id"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        print(f"Error saving prescription: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 80)
    logger.info("🚀 STARTING FASTAPI SERVER")
    logger.info("=" * 80)
    
    # Print all registered routes
    logger.info("📋 Registered Routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            logger.info(f"   {route.path} [{','.join(route.methods)}]")
    
    if db_connected:
        user_count = users_collection.count_documents({})
        logger.info(f"📊 DB: {config.DATABASE_NAME} | Collection: {config.COLLECTION_NAME} | Users: {user_count}")
    
    logger.info("✅ Routes enabled: /simple-register/, /login/, /unified, /auth/")
    logger.info("✅ Cart Routes enabled: /api/v1/cart/*")
    logger.info("✅ Delivery Routes enabled: /api/v1/delivery/*")
    logger.info("=" * 80)
    logger.info(f"🌐 Server starting on http://{getattr(config, 'HOST', '0.0.0.0')}:{getattr(config, 'PORT', 5000)}")
    logger.info("=" * 80)
    
    uvicorn.run(
        app,
        host=getattr(config, "HOST", "0.0.0.0"),
        port=getattr(config, "PORT", 5000),
        log_level="info"
    )


# ---------- FILTER OPTIONS ENDPOINT ----------
@app.get("/api/v1/products/filters/options")
async def get_filter_options():
    """
    Get all available filter options from the database
    Returns unique values for each filterable field
    """
    if not db_connected:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    products_collection = db['products']
    
    # Get unique values for each filter field
    brands = products_collection.distinct("brand")
    genders = products_collection.distinct("gender")
    materials = products_collection.distinct("material")
    styles = products_collection.distinct("style")
    sizes = products_collection.distinct("size")
    frame_colors = products_collection.distinct("frame_color")
    
    # Get all unique comfort features (since it's an array field)
    comfort_pipeline = [
        {"$unwind": "$comfort"},
        {"$group": {"_id": "$comfort"}},
        {"$sort": {"_id": 1}}
    ]
    comfort_results = list(products_collection.aggregate(comfort_pipeline))
    comfort_options = [r["_id"] for r in comfort_results if r["_id"]]
    
    # Get price range
    price_pipeline = [
        {"$group": {
            "_id": None,
            "min_price": {"$min": "$price"},
            "max_price": {"$max": "$price"}
        }}
    ]
    price_result = list(products_collection.aggregate(price_pipeline))
    price_range = price_result[0] if price_result else {"min_price": 0, "max_price": 500}
    
    return {
        "success": True,
        "data": {
            "brands": sorted([b for b in brands if b]),
            "genders": sorted([g for g in genders if g]),
            "materials": sorted([m for m in materials if m]),
            "styles": sorted([s for s in styles if s]),
            "sizes": sorted([sz for sz in sizes if sz]),
            "frame_colors": sorted([fc for fc in frame_colors if fc]),
            "comfort": sorted(comfort_options),
            "price_range": {
                "min": price_range.get("min_price", 0),
                "max": price_range.get("max_price", 500)
            }
        }
    }

