import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import schedule
import os
from os import environ

CURRENCY = ['Binance Coin','Litecoin', 'Uniswap', 'Solana', 'Cardano', 'VeChain', 'PancakeSwap', 'Polygon', 'Chainlink','Fantom', 'Swipe', 'Polygon', 'Dogecoin' ]
SYMBOLS = ['BNB','LTC','UNI', 'SOL', 'ADA', 'VET','CAKE', 'MATIC' ,'LINK','FTM', 'SXP', 'MATIC', 'DOGE']
PRICES = [583.94,303.19,40.183,45.10,1.25,0.246,27.65,0.8021,43.132,0.79701, 4.888, 0.71761, 0.54208]
AMOUNT = [2.226,1.98,7.465,6.69,160.4,407,5.424,187,5.80,126,20.471,141.40, 184.40]


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
        price = soup.find('div',{'class': 'priceValue___11gHJ'}).text
        price = price.strip()
        price = price.replace('$','')
        price = price.replace(',','')
        Actual_prices.append(float(price))
    return Actual_prices

def dataframe():

    sleep= 0.5
    bot_send_text('PORTAFOLIO DE INVERSION CRYPTOMONEDAS ---------------------{}---------{} UTC-----------------'.format(time.strftime("%d/%m/%y"),time.strftime("%H:%M")))
    df = pd.DataFrame({'Moneda':CURRENCY,'Precio Compra':PRICES, 'Cantidad: ': AMOUNT })
    df['Total inversion USD'] = round(df['Precio Compra']*df['Cantidad: '],1)
    df['Precio Actual']= run()
    df['Inversion Actual USD'] = df['Precio Actual']*df['Cantidad: ']
    df['%Rendimiento'] = round((df['Inversion Actual USD']-df['Total inversion USD'])/df['Total inversion USD']*100,2)
    df['% USD'] = round(df['Inversion Actual USD']-df['Total inversion USD'],1)
    initial_inves = round(df['Total inversion USD'].sum(),2)
    final_inves = round(df['Inversion Actual USD'].sum(),2)
    rendi_final = round(((final_inves-initial_inves)/initial_inves)*100,2)
    for i in range(0,len(df['Moneda'])):
        bot_send_text('La inversion inicial de {} fue de {} USD teniendo un rendimiento de {}% equilavente a {} USD.'.format(df['Moneda'][i],df['Total inversion USD'][i],df['%Rendimiento'][i],df['% USD'][i]))
        time.sleep(sleep)
    bot_send_text('Su inversion inicial fue de {} USD.'.format(initial_inves))
    time.sleep(sleep)
    bot_send_text('Su inversion actual es de {} USD.'.format(final_inves))
    time.sleep(sleep)
    bot_send_text('Obteniendo un rendimiento del {}% equivalente al {} USD.'.format(rendi_final,round(final_inves-initial_inves,2) ))
    bot_send_text('--------------------------------GRACIAS------------------------------')


if __name__ == '__main__':

    dataframe()

    # schedule.every().day.at("12:30").do(dataframe)
    # schedule.every().day.at("20:00").do(dataframe)
    # schedule.every().day.at("02:35").do(dataframe)

    # while True:
    #     schedule.run_pending()
