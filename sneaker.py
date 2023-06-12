import requests
from datetime import datetime

class sneaker:
    
    def __init__(self,sku, image, name, taxamount: float,link = None):
        
        self.sku = sku
        self.image = image
        self.taxamount = taxamount
        self.link = link
        self.name = name
        self.sizedict = {
            "Sizes": {}
        }
        self.exchangerate = 1
        
    def addsize(self, size, store, buyprice, salesvolume=None,price=None, salesspeed = None, avgprice = None, profitraw = None):
        
        tempdict = {
            size: {
            "price": price,
            "avgprice": avgprice,
            "salesspeed": salesspeed,
            "salesvolume": salesvolume,
            "profitnotax": None,
            "profittax": None,
            }
        }
        
        self.sizedict["Sizes"].update(tempdict)
        self.addprofit(size, store, price, buyprice)
    
    def addprice(self, size, price):
        
        self.sizedict["Sizes"][size]["price"] = price
    
    def addsalesvolume(self, size, salesvolume):
        
        self.sizedict["Sizes"][size]["salesvolume"] = salesvolume
        
    def addprofit(self, size, store, saleprice, buyprice):
        
        if store == "alias":
            
            priceafterfeeUSD =  round(((((saleprice) * 0.905)-5)*0.971),2)
            priceinEUR = round(priceafterfeeUSD*self.exchangerate,2)
            self.sizedict["Sizes"][size]["profitnotax"] = round(priceinEUR - buyprice,2)
            self.sizedict["Sizes"][size]["profittax"] = round(priceinEUR - round((buyprice/self.taxamount),2),2)
            self.sizedict["Sizes"][size]["price"] = priceinEUR
                                 
    def getnewexchange(self):
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        self.exchangerate = response.json()["rates"]["EUR"]    
            
    def calculateDate(self, firstsold):
        
        firstSoldDateObj = datetime.strptime(firstsold[:10],"%Y-%m-%d").strftime("%d.%m.%Y")
        daysBetween = (datetime.now() - datetime.strptime(firstSoldDateObj, "%d.%m.%Y")).days
        return daysBetween
    
    def addsalesspeed(self, size, datespeed):
        
        self.sizedict["Sizes"][size]["salesspeed"] = datespeed
        
        
        
    