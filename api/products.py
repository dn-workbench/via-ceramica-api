from fastapi import FastAPI

app = FastAPI()

@app.get("/api/products")
def get_products():
    return {"message": "Hello from Vercel"}
