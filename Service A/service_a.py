from fastapi import FastAPI

app = FastAPI()

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}"}

@app.post("/sum")
def sum_numbers(data: dict):
    return {"result": data["a"] + data["b"]}

# uvicorn service_a:app --port 8000