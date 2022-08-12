import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import schedule
import os
from os import environ

CURRENCY = ['Ethereum','Fantom', 'Terra Luna','Mist', 'Bitcoin','Polkadot New', 'Oasis network' ,'Kadena', 'Cosmos','Thorchain','Osmosis','Bnb','Syscoin', 'Bloktopia', 'Moonriver', 'Fantohm','Demole', 'Strong' ]
AMOUNT = [0.6206,1474.86,15.11,15566.72 ,0.01313,22.08,1507.85 ,43.59 ,10.27 ,33.54, 18.32, 0.4367, 108, 3013.55,0.8682,4, 950, 1]




def bot_send_text(bot_message):


      bot_token = environ['bot_token']
      bot_chatID = environ['bot_chatID']
      send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
      response = requests.get(send_text)
      return response

def run():

    Actual_prices = []
    for i in CURRENCY:
        i = i.lower().strip().replace(' ','-')
        url = requests.get('https://coinmarketcap.com/currencies/'+i+'/')
        soup = BeautifulSoup(url.content, 'html.parser')
        price = soup.find('div',{'class': 'priceValue'}).text
        price = price.strip()
        price = price.replace('$','')
        price = price.replace(',','')
        Actual_prices.append(float(price))
    return Actual_prices

def dataframe():

    sleep= 0.01
    bot_send_text('------------------PORTAFOLIO -------------------------{}---------{}'.format(time.strftime("%d/%m/%y"),time.strftime("%H:%M")))
    df = pd.DataFrame({'Moneda':CURRENCY , 'Cantidad':AMOUNT})
    df['Precio Actual']= run()
    df['Inversion Actual USD'] = round(df['Precio Actual']*df['Cantidad'],1)
    final_inves = round(df['Inversion Actual USD'].sum(),2)

    for i in range(0,len(df['Moneda'])):

        bot_send_text('{} {} - Precio: {} USD - Total  {} USD. '.format(df['Cantidad'][i], df['Moneda'][i], df['Precio Actual'][i],df['Inversion Actual USD'][i]))
        time.sleep(sleep)
    
    
    result = (final_inves*3700) - 45345000
    result2 = round((result/45345000)*100,2)
    
    bot_send_text('Su inversion total es  de {} USD o {} COP'.format(final_inves, final_inves*3700))
    bot_send_text('Rentabilidad Actual $ {} COP o {} % '.format(result,result2))
    bot_send_text('***********************************************')

if __name__ == '__main__':

    schedule.every().day.at("12:30").do(dataframe)
    schedule.every().day.at("20:00").do(dataframe)
    schedule.every().day.at("02:50").do(dataframe)

    while True:
        schedule.run_pending()

