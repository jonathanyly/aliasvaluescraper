import sys
import random
import cloudscraper
from termcolor import colored
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from sneakerclass.sneaker import sneaker
from termcolor import colored

def loadproxies():
    proxyList = []
    with open("proxies.txt", "r") as f:
        for line in f:
            line = line.replace("\n", "")
            tmp = line.split(":")
            proxies = {
                "http": "http://" + tmp[2] +":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
                "https": "http://" + tmp[2] +":" + tmp[3] + "@" + tmp[0] + ":" + tmp[1] + "/",
    
            }
            proxyList.append(proxies)
    return proxyList


scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
    }
)

proxies = loadproxies()

class aliaschecker:
    
    def __init__(self, webhook:str, taxamount: float):

        self.webhook = webhook
        self.taxamount = taxamount
    
    def check(self, inputs:list):

        webhook = DiscordWebhook(url=self.webhook)
        priceinput = float(inputs[-1].replace(",", "."))
        sku = str(' '.join(inputs[:-1])).replace(" ", "-")
    
        header = {
            'Host': '2fwotdvm2o-dsn.algolia.net',
            'Content-Type': 'application/json; charset=UTF-8',
            'x-emb-st': '1650552513964',
            'Accept': '*/*',
            'X-Algolia-API-Key': '838ecd564b6aedc176ff73b67087ff43',
            'User-Agent': 'alias/1.15.3 (com.goat.OneSell.ios; build:513; iOS 15.4.1) Alamofire/1.15.3',
            'Accept-Language': 'de-DE;q=1.0',
            'X-Algolia-Application-Id': '2FWOTDVM2O',
            'x-emb-id': 'E5813537190243EA9241A0B289420ADD',
        }
            
        searchparams = {
            'analyticsTags': '["platform:ios","channel:alias"]',
            'distinct': '1',
            'facetingAfterDistinct': '1',
            'facets': '["product_category"]',
            'filters': '(product_category:shoes)',
            'page': '0',
            'query': sku,
        } 
        while True:
            try:
                response = scraper.get('https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2', headers=header, params=searchparams, proxies = random.choice(proxies), timeout= 2)
                if response.status_code == 200:
                    sneakerid = response.json()
                    break
                else:
                    print(colored("["+str(datetime.now())+ "]", 'white'), colored(f"[Alias | {response.status_code}] Bad status code while searching for SKU, retrying...", 'red'))
            except Exception as e:
                print(colored("["+str(datetime.now())+ "]", 'white'), colored(f"Exception occured, {e}", 'red'))
        
        sneakerid = response.json()["hits"][0]["slug"]
        if len(sneakerid["hits"]) == 0:
            print(colored("["+str(datetime.now())+ "]", 'white'), colored("Could not find product on Alias...", 'red'))
            embed_alias_error = DiscordEmbed(title='Could not find product on Alias',color='ff0000')
            embed_alias_error.set_thumbnail(url="https://play-lh.googleusercontent.com/hGPivPBekRKMAZsCfVfhARsYbVDqQHpwyix0ntC8frNDmBld1HXx2_ZhgFkidbD-MFc=s180-rw")
            embed_alias_error.set_footer(text='Alias Price Check')
            embed_alias_error.set_timestamp()
            webhook.add_embed(embed_alias_error)
            webhook.execute()
            return
        
        sneakerobj = sneaker(str(response.json()["hits"][0]["sku"].replace(" ", "-")), response.json()["hits"][0]["grid_glow_picture_url"], response.json()["hits"][0]["name"],self.taxamount)
        if str(inputs[0]).replace(" ", "-").upper() not in str(sneakerobj.sku).upper():
            print(colored("["+str(datetime.now())+ "]", 'white'), colored("Could not find product on Alias...", 'red'))
            embed_alias_error = DiscordEmbed(title='Could not find product on Alias',color='ff0000')
            embed_alias_error.set_thumbnail(url="https://play-lh.googleusercontent.com/hGPivPBekRKMAZsCfVfhARsYbVDqQHpwyix0ntC8frNDmBld1HXx2_ZhgFkidbD-MFc=s180-rw")
            embed_alias_error.set_footer(text='Jonathan Price Checker')
            embed_alias_error.set_timestamp()
            webhook.add_embed(embed_alias_error)
            webhook.execute()
            return

        
        data = '{{"variant":{{"id":"{}","packagingCondition":1,"consigned":false,"regionId":"2"}}}}'.format(sneakerid)
        while True:
            try:
                response = scraper.post('https://sell-api.goat.com/api/v1/analytics/list-variant-availabilities',data = data, proxies = random.choice(proxies), timeout = 2)
                if response.status_code == 200:
                    break
            except:
                print(colored("["+str(datetime.now())+ "]", 'white'), colored("[Alias] Error while searching for Info, retrying...", 'red'))
        data = response.json()
        sneakerobj.getnewexchange()
        for info in data["availability"]:
            try:
                sneakerobj.addsize(size = info["variant"]["size"], store = "alias", buyprice = priceinput, price = int(info['high_demand_price_cents'])/100)
            except KeyError:
                continue
        

        for size in sneakerobj.sizedict["Sizes"]:
            
            data = '{{"count":"10","variant":{{"id":"{}","size":{},"productCondition":1,"packagingCondition":1,"consigned":false}}}}'.format(str(sneakerid), size)
            
            
            while True:
                try:
                    response = scraper.post('https://sell-api.goat.com/api/v1/analytics/orders/recent', data=data, timeout = 3)
                    if response.status_code == 200:
                       break
                except:
                    print(colored("["+str(datetime.now())+ "]", 'white'), colored("[Alias] Error while searching for Info, retrying...", 'red'))
            try:
               volumeDict = response.json()["recent_sales"]
               try:
                   sneakerobj.addsalesvolume(size, len(volumeDict))
               except:
                   continue  
            except KeyError:
                continue
            sneakerobj.addsalesspeed(size, sneakerobj.calculateDate(volumeDict[-1]["purchased_at"]))
        
        embed_alias = DiscordEmbed(title='ID: {}'.format(sneakerobj.sku) + " | " + "Name: " + str(sneakerobj.name), color='793194', description="US Size [Amount of Sales | No. of days it took]")
        embed_alias.set_thumbnail(url=str(sneakerobj.image))
        embed_alias.set_footer(text='Jonathans Alias Price Check')
        embed_alias.set_timestamp()
        
        print(colored("["+str(datetime.now())+ "]", 'white'), colored("Fetched Info on Alias for "+str(sneakerobj.name), 'green'))
        for sizeinfo in sneakerobj.sizedict["Sizes"]:
            if sneakerobj.sizedict["Sizes"][sizeinfo]["profitnotax"] != None and sneakerobj.sizedict["Sizes"][sizeinfo]["salesvolume"] != None and sneakerobj.sizedict["Sizes"][sizeinfo]["salesspeed"] <= 30:
                embed_alias.add_embed_field(name=f'{sizeinfo} [{sneakerobj.sizedict["Sizes"][sizeinfo]["salesvolume"]} | {sneakerobj.sizedict["Sizes"][sizeinfo]["salesspeed"]}]', value=f'{sneakerobj.sizedict["Sizes"][sizeinfo]["price"]} | **{sneakerobj.sizedict["Sizes"][sizeinfo]["profittax"]}**')
            else:
                continue
        webhook.add_embed(embed_alias)
        webhook.execute()
        
        

        

