import requests
import xmltodict
import json

URL = "https://viaceramica.online/index.php?route=extension/module/viaceramica_api&secret_key=hmlx4WPh"

def parse_xml():
    response = requests.get(URL)
    data = xmltodict.parse(response.content)
    
    items = []
    offers = data.get('yml_catalog', {}).get('shop', {}).get('offers', {}).get('offer', [])

    for offer in offers:
        item = {
            "id": offer.get("@id"),
            "url": offer.get("url"),
            "price": offer.get("price"),
            "quantity": offer.get("quantity"),
            "currencyId": offer.get("currencyId"),
            "categoryId": offer.get("categoryId"),
            "pictures": offer.get("picture", []),
            "delivery": offer.get("delivery") == "true",
            "name": offer.get("name"),
            "vendor": offer.get("vendor"),
            "vendorCode": offer.get("vendorCode"),
            "model": offer.get("model"),
            "description": offer.get("description"),
            "barcode": offer.get("barcode"),
            "params": {
                p['@name']: p['#text']
                for p in offer.get("param", []) if isinstance(p, dict)
            }
        }

        if isinstance(item["pictures"], str):
            item["pictures"] = [item["pictures"]]
        items.append(item)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    return items
