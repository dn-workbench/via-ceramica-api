from fastapi import FastAPI
import json
import os
from parser import parse_xml

app = FastAPI()

@app.get("/products")
def get_products():
    if not os.path.exists("data.json"):
        # Первый запуск — сразу парсим и создаём файл
        try:
            parse_xml()
        except Exception as e:
            return {"error": f"Parsing failed: {str(e)}"}

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
