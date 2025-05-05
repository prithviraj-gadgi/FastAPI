from fastapi import FastAPI
import httpx

app = FastAPI()

SERVICE_A_URL = "http://localhost:8000"

@app.get("/call-greet/{name}")
async def call_greet(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVICE_A_URL}/greet/{name}")
    return response.json()

@app.post("/call-sum")
async def call_sum():
    payload = {"a": 10, "b": 20}
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICE_A_URL}/sum", json=payload)
    return response.json()

# uvicorn service_b:app --port 8001