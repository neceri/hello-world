from urllib import request
from datetime import datetime
import itertools
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='(%(asctime)s [%(levelname)s] -%(threadName)-10s-) '
                    + '%(message)s')
markets = ['bitfinex', 'bitstamp', 'btce', 'itbit', 'anxhk', 'hitbtc',
           'kraken', 'bitkonan', 'bitbay', 'rock', 'cbx', 'cotr', 'vcx']
currencies = ['KRW', 'NMC', 'IDR', 'RON', 'ARS', 'AUD', 'BGN', 'BRL', 'BTC',
              'CAD', 'CHF', 'CLP', 'CNY', 'CZK', 'DKK', 'EUR', 'GAU', 'GBP',
              'HKD', 'HUF', 'ILS', 'INR', 'JPY', 'LTC', 'MXN', 'NOK', 'NZD',
              'PEN', 'PLN', 'RUB', 'SAR', 'SEK', 'SGD', 'SLL', 'THB', 'UAH',
              'USD', 'XRP', 'ZAR']
url = []


def generate_api_list(var1, var2):
    """
    Takes both a list of markets and a list of currencies as input
    Outputs combined values in a format needed for the bitcoincharts API
    """
    logging.debug('Ingested %s Markets and %s different Currencies.' %
                  (len(var1), len(var2)))
    for i in itertools.product(var1, var2):
        url.append(i[0] + i[1])
    logging.debug('Merged Markets and Currencies into %s permutations.' %
                  (len(url)))


def return_values(input_value):
    """
    Takes combination of market and currency as input.
    Returns tab-delimited transactions if available, otherwise returns error.
    """
    try:
        req = request.Request(
            'http://api.bitcoincharts.com/v1/trades.csv?symbol=' + n)
        resp = request.urlopen(req).read().decode('utf-8').split('\n')
        for x in resp:
            if len(x) == 0:
                logging.warn('No Data for %s!' % n)
            elif x:
                di = dict([(n, [int(x.split(',')[0]), float(x.split(',')[1]),
                                float(x.split(',')[2])])])
                logging.info(
                    'For %s: The value of the transaction at %s was %.2f' %
                    (n, di[n][0], di[n][1]))
    except Exception as e:
        logging.error('Symbol %s resulted in "%s"' % (n, str(e)))


if __name__ == '__main__':
    generate_api_list(markets, currencies)
    for n in url:
        return_values(n)
    logging.info('All done!')
