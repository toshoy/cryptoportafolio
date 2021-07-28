import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import schedule
import os
from os import environ

CURRENCY = ['Sushi Swap', 'Uniswap', 'Solana', 'Polygon', 'PancakeSwap', 'Chainlink', 'Ethereum','Cardano' ,'Bitcoin', 'Theta', 'Mist', 'Dogecoin']
SYMBOL = ['SUSHI', 'UNI', 'SOL', 'MATIC', 'CAKE', 'LINK', 'ETH','ADA' ,'BTC', 'THETA', 'MIST', 'DOGE']
AMOUNT = [20.54,7.465,6.447,319.20,5.424,6.81,0.000001,189.430,0.000001,55.18,1824.91,292.5]




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

    sleep= 0.4
    bot_send_text('PORTAFOLIO DE INVERSION CRYPTOMONEDAS ---------------------{}---------{}--------------------'.format(time.strftime("%d/%m/%y"),time.strftime("%H:%M")))
    df = pd.DataFrame({'Moneda':CURRENCY, 'Cantidad': AMOUNT, 'SYMBOL':SYMBOL})
    df['Precio Actual']= run()
    df['Inversion Actual USD'] = round(df['Precio Actual']*df['Cantidad'],2)
    final_inves = round(df['Inversion Actual USD'].sum(),2)
    for i in range(0,len(df['Moneda'])):
        bot_send_text('{} - Amount: {} - Price: {} USD - TOTAL: {} USD '.format(df['SYMBOL'][i],df['Cantidad'][i],df['Precio Actual'][i],df['Inversion Actual USD'][i]))
        time.sleep(sleep)
    bot_send_text('Su inversion actual es de {} USD.'.format(final_inves))
    time.sleep(sleep)
    bot_send_text('--------------------------------GRACIAS------------------------------')


if __name__ == '__main__':

    schedule.every().day.at("12:30").do(dataframe)
    schedule.every().day.at("20:00").do(dataframe)
    schedule.every().day.at("02:30").do(dataframe)

    while True:
        schedule.run_pending()
