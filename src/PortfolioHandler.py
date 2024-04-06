import ccxt,datetime,sys,currency_converter
from StatementHandler import StatementHandler
from StatementLine import StatementLine

class PortfolioHandler:
  
  def __init__(self, statement):
    self.statement = statement
    self.cryptosOwned = {}
    self.amountInvested = 0
    self.taxableGainsPerYear = {}
    self.exchange = ccxt.binance()
    self.currencyConverter = currency_converter.CurrencyConverter()

  def getTaxableGainsPerYear(self, year=None):
    if not year:
      return self.taxableGainsPerYear
    yearInt = year
    try:
      yearInt = int(year)
      date = datetime.datetime(yearInt, 1, 1)
    except (Exception, ValueError):
      print("'", year, "' is not a year, will return whole summary")
      return self.taxableGainsPerYear
    else:
      if yearInt in self.taxableGainsPerYear.keys():
        return self.taxableGainsPerYear[yearInt]
      else:
        return 0

  def portfolioValue(self, date):
    timestamp = int(date.timestamp() * 1000)
    portfolioValue = 0
    for (cryptoName,amount) in self.cryptosOwned.items():
      value = 0
      try:
        response = self.exchange.fetch_ohlcv(cryptoName+'/USDT', '1m', timestamp, 1)
        value = (response[0][1] + response[0][4])/2
        value = self.currencyConverter.convert(value, 'USD', 'EUR', date=date)
      except Exception:
        #print("ERROR FOR "+ cryptoName)
        pass
      portfolioValue = portfolioValue + float(value)*amount
    return portfolioValue

  def examinePortfolioForTaxableGains(self):
    print('Examen des relevés', end='', flush=True)
    for line in self.statement.getAllStatementLines():

      if line.isBuyLine():
        crypto = line.getCrypto()
        if crypto not in self.cryptosOwned.keys():
          self.cryptosOwned[crypto] = 0
        self.cryptosOwned[crypto] = self.cryptosOwned[crypto] + line.getQuantity()
        
        self.amountInvested = self.amountInvested + line.getSubTotal()
      
      if line.isSellLine():
        print('.', end='', flush=True)
        crypto = line.getCrypto()
        if crypto == line.getSpotCurrency():
          continue
        date = line.getDate()
        #print("Vente de " + crypto + " en date du", date, ": ")
        valuePortfolio = self.portfolioValue(date)
        percentageSold = line.getSubTotal()/valuePortfolio
        percentagePlusValue = valuePortfolio/self.amountInvested
        taxableGains = (valuePortfolio - self.amountInvested) * percentageSold
        #print("Montant investi à cette date : " + PortfolioHandler.printableAmount(self.amountInvested) + " EUR")
        #print("Valeur du portefeuille à cette date : " + PortfolioHandler.printableAmount(valuePortfolio) + " EUR")
        #print("Valeur en euros vendue : " + PortfolioHandler.printableAmount(line.getSubTotal()) + " EUR")
        #print("Plus value à déclarer : " + PortfolioHandler.printableAmount(taxableGains) + " EUR")
        #print()
        if date.year not in self.taxableGainsPerYear.keys():
          self.taxableGainsPerYear[date.year] = 0
        self.taxableGainsPerYear[date.year] = self.taxableGainsPerYear[date.year] + taxableGains
    
    
        # Compute information to withdraw sold amount part in invested amount
        toWithDrawFromAmountInvested = line.getSubTotal()/percentagePlusValue
        self.amountInvested = self.amountInvested - toWithDrawFromAmountInvested
        
        # Remove crypto sold in owned crypto
        self.cryptosOwned[crypto] = self.cryptosOwned[crypto] - line.getQuantity()
    print()

  def printSummaryPerYear(self):
    print("Résumé par année : ")
    for year, taxableGain in self.taxableGainsPerYear.items():
      print("- " + str(year) + " : plus-value imposable " + PortfolioHandler.printableAmount(taxableGain) + " EUR")

  @staticmethod
  def printableAmount(amount):
    return str(round(amount, 2))