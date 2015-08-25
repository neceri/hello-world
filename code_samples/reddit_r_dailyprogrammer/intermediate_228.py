#  Author: neceri
#  Created for the following reddit dailyprogrammer challenge:
#    https://www.reddit.com/r/dailyprogrammer/comments/3hj4o2/20150819_challenge_228_intermediate_use_a_web/cuclldn
#    General idea is to iterate through each combination for a web API, parse
#    the CSV response, and display the data.  Also, check for errors in the
#    response.

import requests
import itertools


#  Creating initial data set and initializing the url list
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
    print('Ingested %s Markets and %s different Currencies.' %
                  (len(var1), len(var2)))
    for i in itertools.product(var1, var2):
        url.append(i[0] + i[1])
    print('Merged Markets and Currencies into %s permutations.' %
                  (len(url)))


def return_values(input_value):
    """
    Takes combination of market and currency as input.
    Returns tab-delimited transactions if available, otherwise returns error.
    """
    try:
        data = []
        #  Sends request for the current combination of market and currency
        req = requests.get(
            'http://api.bitcoincharts.com/v1/trades.csv?symbol=' + n)
        #  Checks for 404 errors and prints error response
        if req.status_code == 404:
            print('The request for %s resulted in an HTTP 404 error!' % n)
        #  Then, checks for empty responses and complains
        elif len(req.text) == 0:
            print('Symbol %s resulted in NO DATA' % (n))
        #  Otherwise, splits the reponse in nested lists and print them
        #    out one at a time.  %.2f prints a floating point in 0.00 form
        else:
            for h in req.text.replace(',', '\t').split('\n'):
                data.append(h.split('\t'))
        for row in data:
            print('The request at %s on %s resulted' % (row[0], n)
                  + 'in %.2f (%.5f BTC traded)' % (float(row[1]),
                                                   float(row[2])))
    #  Print out error in the event of a code exception
    except Exception as e:
        print('ERROR:   %s' % e)


#  See this for an exaplanation on what this section does:
#    http://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    generate_api_list(markets, currencies)
    for n in url:
        return_values(n)
    print('\n\nAll done!')
