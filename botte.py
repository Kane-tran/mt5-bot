import requests

TOKEN = "8654287727:AAEWxgi9VCLe6esdpg2Xej1WHZF3h74GyAk"
CHAT_ID ="7542202988"

for i in range(5):
    message = "helllo world" + str(i)

    base_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    resp = requests.get(base_url)
