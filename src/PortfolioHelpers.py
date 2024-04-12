from Exchange import CryptoExchange

# Class giving helper functions
# for handling a PortfolioHandler
class PortfolioHelpers:

  # Returns: the whole portfolio value owned
  @staticmethod
  def portfolioValue(portfolio, date, onlyBought=True):
    cryptoRegistry = portfolio.getCryptosOwned()
    if onlyBought:
      cryptoRegistry = portfolio.getCryptosBought()

    portfolioValue = 0
    for (cryptoName,amount) in cryptoRegistry.items():
      value = CryptoExchange.getCryptoValueAtDate(cryptoName, date)
      portfolioValue += float(value)*amount
    return portfolioValue

  # Round currency for printing (two decimals)
  @staticmethod
  def roundCurrency(amount, currency = None):
    if currency:
      currency = " " + currency
    else:
      currency = ""
    return str(round(amount, 2)) + currency

  # Round currency for printing (8 decimals)
  @staticmethod
  def roundCryptoQuantity(amount):
    return str(round(amount, 8))
