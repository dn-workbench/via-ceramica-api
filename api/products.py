from fastapi import FastAPI
import requests
import xmltodict

app = FastAPI()

@app.get("/api/products")
def get_products():
    url = "https://viaceramica.online/index.php?route=extension/module/viaceramica_api&secret_key=hmlx4WPh"
    
    try:
        response = requests.get(url)
        data = xmltodict.parse(response.content)
        offers = data.get("yml_catalog", {}).get("shop", {}).get("offers", {}).get("offer", [])
        
        result = []

        for offer in offers:
            pictures_raw = offer.get("picture", [])
            if isinstance(pictures_raw, str):
                pictures = [pictures_raw]
            elif isinstance(pictures_raw, list):
                pictures = pictures_raw
            else:
                pictures = []

            item = {
                "id": offer.get("@id"),
                "url": offer.get("url"),
                "price": offer.get("price"),
                "quantity": offer.get("quantity"),
                "currencyId": offer.get("currencyId"),
                "categoryId": offer.get("categoryId"),
                "pictures": pictures,
                "delivery": offer.get("delivery") == "true",
                "name": offer.get("name"),
                "vendor": offer.get("vendor"),
                "vendorCode": offer.get("vendorCode"),
                "model": offer.get("model"),
                "description": offer.get("description"),
                "barcode": offer.get("barcode"),
                "params": {
                    p["@name"]: p["#text"]
                    for p in offer.get("param", []) if isinstance(p, dict)
                }
            }

            result.append(item)

        return result

    except Exception as e:
        return {"error": str(e)}
