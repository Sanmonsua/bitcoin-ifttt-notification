import requests
import time

from datetime import datetime

BITCOIN_PRICE_EMERGENCY = 7000
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOK_URL = 'https://maker.ifttt.com/trigger/{}/with/key/jqHeTM_i_uy4PzVdOc3Nd-btWWNW3_vnsvKBUHza-jL'

def getLatestPrice():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])

def postWebhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOK_URL.format(event)
    requests.post(ifttt_event_url, json=data)

def formatPriceHistory(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y')
        price = bitcoin_price['price']
        row = '{}:<b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)

def main():
    bitcoin_history = []
    while True:
        price = round(getLatestPrice(), 4)
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        if len(bitcoin_history) == 7:
            postWebhook('bitcoin_price_weekly', formatPriceHistory(bitcoin_history))
            bitcoin_history = []
        elif price < BITCOIN_PRICE_THRESHOLD:
            postWebhook('bitcoin_price_emergency', price)
        else:
            postWebhook('bitcoin_price_daily', price)
        
        time.sleep(24*60*60)

if __name__ == "__main__":
    main()





