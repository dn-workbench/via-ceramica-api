from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from parser import parse_xml

app = FastAPI()

# Разрешённые источники (фронтенд домен)
origins = [
    "https://via-ceramica-frontend.vercel.app",
    # если хочешь, можешь добавить http://localhost:3000 для локальной разработки
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Можно указать ["*"] для всех, но это менее безопасно
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products")
def get_products():
    if not os.path.exists("data.json"):
        try:
            parse_xml()
        except Exception as e:
            return {"error": f"Parsing failed: {str(e)}"}

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
