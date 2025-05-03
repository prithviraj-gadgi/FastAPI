from fastapi import FastAPI, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

from model.customer import CustomerIn, CustomerOut, UpdateCustomer

app = FastAPI()

# MongoDB setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['customer_db']
customer_collection = db['customers']

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Save Customer
@app.post("/customer/save", response_model=CustomerOut)
async def save_customer(customer: CustomerIn):
    exists_with_customer_id = await customer_collection.find_one({"customerId": customer.customerId})
    if exists_with_customer_id:
        raise HTTPException(status_code=400, detail=f"Customer already exists with customerId: {customer.customerId}")
    exists_with_email = await customer_collection.find_one({"email": customer.email})
    if exists_with_email:
        raise HTTPException(status_code=400, detail=f"Customer already exists with email: {customer.email}")
    exists_with_phone_no = await customer_collection.find_one({"phoneNo": customer.phoneNo})
    if exists_with_phone_no:
        raise HTTPException(status_code=400, detail=f"Customer already exists with phoneNo: {customer.phoneNo}")
    cust_dict = customer.model_dump()
    cust_dict['password'] = hash_password(cust_dict['password'])
    await customer_collection.insert_one(cust_dict)
    return cust_dict

# Get Customer
@app.get("/customer/getById/{customer_id}", response_model=CustomerOut)
async def get_customer(customer_id: str = Path(...)):
    customer = await customer_collection.find_one({"customerId": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with customerId: {customer_id}")
    return customer

# Update Customer
@app.patch("/customer/update/{customer_id}", response_model=CustomerOut)
async def update_customer(updates: UpdateCustomer, customer_id: str = Path(...)):
    customer = await customer_collection.find_one({"customerId": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with customerId: {customer_id}")
    update_data = updates.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['password'] = hash_password(update_data['password'])
    await customer_collection.update_one({"customerId": customer_id}, {"$set": update_data})
    updated = await customer_collection.find_one({"customerId": customer_id})
    return updated

# Delete Customer
@app.delete("/customer/delete/{customer_id}")
async def delete_customer(customer_id: str = Path(...)):
    customer = await customer_collection.find_one({"customerId": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with customerId: {customer_id}")
    await customer_collection.delete_one({"customerId": customer_id})
    return f"Customer deleted with customerId: {customer_id}"

