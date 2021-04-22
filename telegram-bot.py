import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import schedule

CURRENCY = ['Binance Coin','Litecoin', 'Bitcoin', 'Ethereum Classic', 'Cardano', 'VeChain', 'PancakeSwap', 'Uniswap', 'Chainlink']
PRICES = [583.94,259.56,55336,34.20,1.25,0.246,27.65,31.82,37.92]
AMOUNT = [2.226,3.46,0.009035,8.77,160.4,407,5.424,4.710,4.12]


def bot_send_text(bot_message):

      bot_token = '1708867172:AAE6Y2blw4Nnp-Tqs60AgkWEZpPq_XY5r3s'
      bot_chatID = '1139403272'
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
    bot_send_text('PORTAFOLIO DE INVERSION CRYPTOMONEDAS ---------------------{}---------{}---------------------'.format(time.strftime("%d/%m/%y"),time.strftime("%H:%M")))
    df = pd.DataFrame({'Moneda':CURRENCY,'Precio Compra':PRICES, 'Cantidad: ': AMOUNT })
    df['Total inversion USD'] = df['Precio Compra']*df['Cantidad: ']
    df['Precio Actual']= run()
    df['Inversion Actual USD'] = df['Precio Actual']*df['Cantidad: ']
    df['% Rendimiento'] = round((df['Inversion Actual USD']-df['Total inversion USD'])/df['Total inversion USD']*100,2)
    df['% USD'] = round(df['Inversion Actual USD']-df['Total inversion USD'],1)
    initial_inves = round(df['Total inversion USD'].sum(),2)
    final_inves = round(df['Inversion Actual USD'].sum(),2)
    rendi_final = round(((final_inves-initial_inves)/initial_inves)*100,2)
    for i in range(0,len(df['Moneda'])):
        bot_send_text('El rendimiento de {} fue de {}% equilavente a {} USD.'.format(df['Moneda'][i],df['% Rendimiento'][i],df['% USD'][i]))
        time.sleep(sleep)
    bot_send_text('Su inversion inicial fue de {} USD.'.format(initial_inves))
    time.sleep(sleep)
    bot_send_text('Su inversion actual es de {} USD.'.format(final_inves))
    time.sleep(sleep)
    bot_send_text('Obteniendo un rendimiento del {}% equivalente al {} USD.'.format(rendi_final,round(final_inves-initial_inves,2) ))
    bot_send_text('--------------------------------GRACIAS------------------------------')


if __name__ == '__main__':
    dataframe()
    # schedule.every().day.at("08:00").do(dataframe)
    # schedule.every().day.at("15:00").do(dataframe)
    # schedule.every().day.at("21:00").do(dataframe)

    # while True:
    #     schedule.run_pending()
