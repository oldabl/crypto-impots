import ccxt, currency_converter, datetime, logging
from Defaults import Defaults

# Class responsible for handling all
# cryptocurrency market details
class CryptoExchange:

  exchange = ccxt.binance()

  # Returns: the value of the crypto at the date specified,
  #  in the default currency
  # If an error occurs, it will return 0
  @staticmethod
  def getCryptoValueAtDate(cryptoHandle, date):
    value = 0.00
    try:
      timestamp = int(date.timestamp() * 1000)
      response = CryptoExchange.exchange.fetch_ohlcv(cryptoHandle+'/USDT', '1m', timestamp, 1)
      value = (response[0][1] + response[0][4])/2
      value = CurrencyExchange.convertCurrencyAmount(value, 'USD', Defaults.CURRENCY, date=date)
    except Exception as e:
      logging.error("Exception: %s %s", cryptoHandle, e)
    return value

# Class responsible for handling all
# currency exchange details
class CurrencyExchange:

  currencyConverter = currency_converter.CurrencyConverter(currency_converter.ECB_URL)

  # Returns: the amount of fromCurrency converted
  #  into the toCurrency, with the rate available at specified date
  # If an error occurs, it will return 0
  @staticmethod
  def convertCurrencyAmount(amount, fromCurrency, toCurrency=Defaults.CURRENCY, date=datetime.datetime.now()):
    value = 0.00
    try:
      value = CurrencyExchange.currencyConverter.convert(amount, fromCurrency, toCurrency, date=date)
    except Exception as e:
      logging.error("Exception: %s %s", fromCurrency, e)
    return value
