from discord_webhook import DiscordEmbed, DiscordWebhook
import requests, json, time, datetime


def timer():
    now = datetime.datetime.now()
    now = now.strftime("[%b %d @ %H:%M:%S.%f")[:-3]+("]")
    return now

def getProducts():
    response = requests.get(requestUrl).json()
    return response

def sendWebhook(productJson):
    title = productJson["title"]
    handle = productJson["handle"]
    productUrl = f"{siteUrl}/products/{handle}"
    price = productJson["variants"][0]["price"]
    image = productJson["images"][0]["src"]

    webhook = DiscordWebhook(url=webhookUrl, username="Shopify Monitor")
    embed = DiscordEmbed(title=title, url=productUrl)
    embed.add_embed_field(name="Price", value=price)
    embed.set_thumbnail(url=image)
    webhook.add_embed(embed)
    webhook.execute()



with open("config.json", "r") as f:
    configData = json.load(f)

    siteUrl = configData["site-url"]
    webhookUrl = configData["webhook-url"]
    delay = configData["delay"]

requestUrl = f"{siteUrl}/products.json"
productList = requests.get(requestUrl).json()

while True:
    print(f"{timer()} Scraping products from the website")
    products = getProducts()

    for product in products:
        if product not in productList:
            sendWebhook(product)
    
    productList = products
    print(f"{timer()} Sleeping {delay}s...")
    time.sleep(delay)