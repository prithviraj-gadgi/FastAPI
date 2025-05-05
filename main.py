from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorClient

from model.customer import CustomerIn, CustomerOut, UpdateCustomer
from utility.jwt_util import JWTUtil

app = FastAPI()
jwt_util = JWTUtil()

# MongoDB setup
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client['customer_db']
customer_collection = db['customers']

# Save Customer
@app.post("/customer/save", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
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
    cust_dict['password'] = jwt_util.hash_password(cust_dict['password'])
    await customer_collection.insert_one(cust_dict)
    return cust_dict

# Get Customer
@app.get("/customer/getById/{customer_id}", response_model=CustomerOut, status_code=status.HTTP_200_OK)
async def get_customer(current_user: Annotated[str, Depends(jwt_util.get_current_user)], customer_id: str = Path(...)):
    customer = await customer_collection.find_one({"customerId": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with customerId: {customer_id}")
    return customer

# Update Customer
@app.patch("/customer/update/{customer_id}", response_model=CustomerOut, status_code=status.HTTP_200_OK)
async def update_customer(current_user: Annotated[str, Depends(jwt_util.get_current_user)], updates: UpdateCustomer, customer_id: str = Path(...)):
    customer = await customer_collection.find_one({"customerId": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with customerId: {customer_id}")
    update_data = updates.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['password'] = jwt_util.hash_password(update_data['password'])
    await customer_collection.update_one({"customerId": customer_id}, {"$set": update_data})
    updated = await customer_collection.find_one({"customerId": customer_id})
    return updated

# Delete Customer
@app.delete("/customer/delete/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(current_user: Annotated[str, Depends(jwt_util.get_current_user)], customer_id: str = Path(...)):
    customer = await customer_collection.find_one({"customerId": customer_id})
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with customerId: {customer_id}")
    await customer_collection.delete_one({"customerId": customer_id})
    return f"Customer deleted with customerId: {customer_id}"

# Login Customer
@app.post("/login", status_code=status.HTTP_200_OK)
async def login_customer(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    customer = await customer_collection.find_one({"customerId": form_data.username})
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found with customerId: {form_data.username}")
    if not jwt_util.verify_password(form_data.password, customer["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt_util.encode_jwt(customer["customerId"])
    return {"access_token": token, "token_type": "Bearer"}
