from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class OrderItem(BaseModel):
    flavor: str
    option: str  # "piece" or "box"
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    address: str
    items: List[OrderItem]
    total: float
    payment_method: str = "GCash"

class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    order_id: str
    customer_name: str
    phone: str
    address: str
    items: List[OrderItem]
    total: float
    payment_method: str
    status: str = "pending"
    created_at: str

class OrderUpdate(BaseModel):
    status: str

class InventoryStats(BaseModel):
    flavor: str
    pieces_sold: int
    boxes_sold: int
    total_quantity: int

class SalesSummary(BaseModel):
    total_orders: int
    total_revenue: float
    best_selling_flavor: str
    inventory: List[InventoryStats]

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminLoginResponse(BaseModel):
    success: bool
    message: str

# Routes
@api_router.get("/")
async def root():
    return {"message": "DivineCo API"}

@api_router.post("/orders", response_model=Order)
async def create_order(order: OrderCreate):
    import uuid
    order_dict = order.model_dump()
    order_dict['order_id'] = str(uuid.uuid4())[:8]
    order_dict['status'] = 'pending'
    order_dict['created_at'] = datetime.now(timezone.utc).isoformat()
    
    _ = await db.orders.insert_one(order_dict)
    return Order(**order_dict)

@api_router.get("/orders", response_model=List[Order])
async def get_orders():
    orders = await db.orders.find({}, {"_id": 0}).to_list(1000)
    return orders

@api_router.patch("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, update: OrderUpdate):
    result = await db.orders.find_one_and_update(
        {"order_id": order_id},
        {"$set": {"status": update.status}},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    result.pop('_id', None)
    return Order(**result)

@api_router.get("/inventory", response_model=SalesSummary)
async def get_inventory():
    orders = await db.orders.find({}, {"_id": 0}).to_list(1000)
    
    # Initialize inventory tracking
    flavors = [
        "Chocolate Chips",
        "White Matcha",
        "Deep Choco",
        "S'mores",
        "Monster Cookie",
        "Cheesy Velvet"
    ]
    
    inventory_data = {flavor: {"pieces": 0, "boxes": 0} for flavor in flavors}
    total_revenue = 0
    
    for order in orders:
        total_revenue += order['total']
        for item in order['items']:
            flavor = item['flavor']
            if flavor in inventory_data:
                if item['option'] == 'piece':
                    inventory_data[flavor]['pieces'] += item['quantity']
                else:
                    inventory_data[flavor]['boxes'] += item['quantity']
    
    # Build inventory stats
    inventory = []
    for flavor, data in inventory_data.items():
        total_qty = data['pieces'] + (data['boxes'] * 6)
        inventory.append(InventoryStats(
            flavor=flavor,
            pieces_sold=data['pieces'],
            boxes_sold=data['boxes'],
            total_quantity=total_qty
        ))
    
    # Find best selling
    best_selling = max(inventory, key=lambda x: x.total_quantity) if inventory else None
    
    return SalesSummary(
        total_orders=len(orders),
        total_revenue=total_revenue,
        best_selling_flavor=best_selling.flavor if best_selling else "N/A",
        inventory=inventory
    )

@api_router.post("/admin/login", response_model=AdminLoginResponse)
async def admin_login(credentials: AdminLogin):
    # Admin authentication
    if credentials.username == "Admin" and credentials.password == "vxnz.exe":
        return AdminLoginResponse(success=True, message="Login successful")
    return AdminLoginResponse(success=False, message="Invalid credentials")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
