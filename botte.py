import requests

TOKEN = "8654287727:AAEWxgi9VCLe6esdpg2Xej1WHZF3h74Gy"

base_url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

parameters = {
    "offset" : "8654287727"
}

resp = requests.get(base_url, data = parameters)
print(resp.text)