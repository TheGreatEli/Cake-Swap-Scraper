from bs4 import BeautifulSoup
import requests
import re
from datetime import timezone
import datetime
import json
import os
import schedule
import time

url = "https://coinmarketcap.com/currencies/pancakeswap/"

def run_scraper():
  print('running')
  data = []

  #load prices
  if os.path.exists('PancakeSwap_prices.json'):
    with open('PancakeSwap_prices.json') as f:
      data = json.load(f)

  
  
  content = requests.get(url).text
  soup = BeautifulSoup(content, 'lxml')

  #print(soup)

  #find class id 
  regex = re.compile('.*priceValue*.')

  #find the current price
  current_percent = soup.find('div', {'class': regex}).text

  print(current_percent)

  #get our current time
  dt = datetime.datetime.now(timezone.utc)

  utc_time = dt.replace(tzinfo=timezone.utc)
  utc_timestamp = utc_time.timestamp()
  

  #prepare Json obj
  export_obj = {
    'time': utc_timestamp,
    'price': current_percent
  }

  data.append(export_obj)

  print(export_obj)

  #save to json file
  with open('PancakeSwap_prices.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
  
#run scrapper

schedule.every(6).minutes.do(run_scraper)

while True:
  schedule.run_pending()
  time.sleep(1)

