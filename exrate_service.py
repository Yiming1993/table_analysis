import re
import json
import urllib.request

def exchange_rate(number, currency, target_currency):
    exchange_code = str(currency+target_currency).upper()
    url = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREX{}&column=Code,Price".format(exchange_code)
    req = urllib.request.Request(url)
    f = urllib.request.urlopen(req)
    html = f.read().decode("utf-8")

    s = re.findall("{.*}",str(html))[0]
    sjson = json.loads(s)

    rate = sjson["Data"][0][0][1]/10000
    rate = float('%.5f' % rate)

    fin_currency = number*rate
    return fin_currency

if __name__ == '__main__':
    currency = exchange_rate(50000, 'cny', 'usd')
    print(currency)