import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import schedule
import os
from os import environ

CURRENCY = ['Ethereum','Bitcoin', 'Verasity', 'Mist', 'PancakeSwap', 'Cardano', 'Polkadot New', 'Terra Luna', 'Polygon', 'Binance Coin', 'Terrausd']
AMOUNT = [0.6407,0.02346,25372.82,8170,99.85,208.93,15.53,15.58,313.8,0.4751,806]




def bot_send_text(bot_message):

      bot_token = environ['bot_token']
      bot_chatID = environ['bot_chatID']
      send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
      response = requests.get(send_text)
      return response

def run():

    Actual_prices = []
    for i in CURRENCY:
        i = i.lower()
        i = i.strip()
        i = i.replace(' ','-')
        i = '/currencies/'+i+'/'
        url = requests.get('https://coinmarketcap.com/'+ i)
        soup = BeautifulSoup(url.content, 'html.parser')
        price = soup.find('div',{'class': 'priceValue'}).text
        price = price.strip()
        price = price.replace('$','')
        price = price.replace(',','')
        Actual_prices.append(float(price))
    return Actual_prices

def dataframe():

    sleep= 0.4
    bot_send_text('               PORTAFOLIO DE HODL CRYPTOMONEDAS ---------------------{}---------{}--------------------'.format(time.strftime("%d/%m/%y"),time.strftime("%H:%M")))
    df = pd.DataFrame({'Moneda':CURRENCY , 'Cantidad: ': AMOUNT})
    df['Precio Actual']= run()
    df['Inversion Actual USD'] = round(df['Precio Actual']*df['Cantidad: '],1)
    final_inves = round(df['Inversion Actual USD'].sum(),2)

    for i in range(0,len(df['Moneda'])):

        bot_send_text('La precio actual  de {} es de {} USD y su inversion es de {} USD. '.format(df['Moneda'][i], df['Precio Actual'][i],df['Inversion Actual USD'][i]))
        time.sleep(sleep)
    
    bot_send_text('Su inversion total es  de {} USD o {} COP'.format(final_inves, final_inves*3700))



#if __name__ == '__main__':

#    schedule.every().day.at("12:30").do(dataframe)
#    schedule.every().day.at("20:00").do(dataframe)
#    schedule.every().day.at("02:50").do(dataframe)

#    while True:
#        schedule.run_pending()
