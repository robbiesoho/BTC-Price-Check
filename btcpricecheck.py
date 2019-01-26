
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd

my_url = 'https://coinmarketcap.com/'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

containers = page_soup.find("div", {"class": "container main-section"})
tabes = containers.find("table", {"id": "currencies"})
table_names= tabes.find("tbody")

btc = table_names.find_all("tr")

#Get the names and prices of the first 16 crypto coins
prices = []
names = []

for i in range(16):
    x = btc[i]

    #find the price
    x.find("a", {"class": "price"}).text
    current_price = x.find("a", {"class": "price"}).text.strip()
    prices.append(current_price)
    
    #find the name of the crypto
    name = x.find("td", {"class": "no-wrap currency-name"})
    q = name.text.strip()
    coin_name = " ".join(q.split("\n"))
    names.append(coin_name)

#Make a dataframe with the information we have gathered
df = pd.DataFrame({'Name': names,
                   'Price': prices,
                   })

#Use regular expressions to create a column with just the symbol
import re

symbols = []

for i in df['Name']:
    symbols.append(re.search(r"[A-Z]{3,5}\s\s", i).group().split()[0])
    
df['Symbol'] = symbols

#GUI
from tkinter import *

root = Tk()
root.title('BTC Price Check')
root.geometry('{}x{}'.format(950, 550))

frame = Frame(root,relief= GROOVE)
frame.pack(side = BOTTOM)

class CheckBox(Checkbutton):
    boxes = []  # Storage for all buttons
    def __init__(self, master=None, **options):
        Checkbutton.__init__(self, frame, options)
        self.boxes.append(self)
        self.var = IntVar() 
        self.configure(variable=self.var)
        
header = Label(height=1, width=100, text = "Welcome to BTC Price Check")
header.config(font=("Courier", 20))
header.pack(side = TOP, pady = 0)

text = Text(frame)
text.pack(padx = 20, pady = 0, side = RIGHT)

#fucntions for our buttons
def display_price():
    for c, box in enumerate(CheckBox.boxes):
        if box.var.get():
            text.insert(INSERT, "The price of " + names[c] + " is: " + prices[c])
            text.insert(INSERT, "\n")
    text.config(state=DISABLED)
                
def clearBox():
    text.config(state=NORMAL)
    text.delete("1.0", "end")

#Use the class we created to iterate through the 16 cryptos and create a checkbox for each             
a=0
while a<len(df['Name']):
   bouton=CheckBox(text = names[a],bg = 'yellow')
   a=a+1
   bouton.pack(fill = Y, pady = 2, side = TOP)

#Buttons
pricefind = Button(frame, text = 'Search',width= 20, command = display_price)
pricefind.pack()
clearprice = Button(frame, text = 'Clear', width= 20, command = clearBox)
clearprice.pack()

mainloop()



