import datetime, logging
from Exchange import CryptoExchange, CurrencyExchange
from Defaults import Defaults

# Class responsible for parsing and
# extracting the information from
# an exchange platform CSV statement
class PortfolioHandler:

  # Dictionaries to count cryptos
  cryptosBought = {}
  cryptosOwned = {}

  # Track amount invested and gains per year
  amountInvested = 0
  taxableGainsPerYear = {}

  # Constructor input:
  #  - statement: StatementHandler object
  def __init__(self, statement):
    logging.debug
    self.statement = statement
    self.populateMissingInformation()

  # Basic attribute getters
  def getCryptosBought(self):
    return self.cryptosBought
  def getCryptosOwned(self):
    return self.cryptosOwned
  def getAmountInvested(self):
    return self.amountInvested
  def getTaxableGainsPerYear(self):
    return self.taxableGainsPerYear

  # Returns: the gain taxable for the year specified
  # If the year is invalid, return current tax year
  def getTaxableGainsPerYear(self, year):
    yearInt = datetime.date.today().year
    try:
      yearInt = int(year)
      date = datetime.datetime(yearInt, 1, 1)
    except (Exception, ValueError):
      print("'", year, "' is not a year, will return current tax year", yearInt)

    if yearInt in self.taxableGainsPerYear.keys():
      return self.taxableGainsPerYear[yearInt]
    else:
      return 0

  # Role: populate information that might be missing like
  # - price at which the crypto was acquired in the default currency
  # - fees in the default currency
  def populateMissingInformation(self):
    # Will track the line we look at
    i = 0

    for line in self.statement.getStatementLines():

      # Flag to know if the statement needs updated
      change = False

      if not line.isInformationComplete():

        change = True
        cvad = CryptoExchange.getCryptoValueAtDate(line.getCrypto(), line.getDate())

        # If missing default currency fees
        if line.getFees() == None and line.getCryptoFees() != None:
          line.setFees(line.getCryptoFees()*cvad)

        # If missing spot price
        if line.getSpotPrice() == None:
          line.setSpotPrice(cvad)
        
        # If missing different totals
        if line.getSubTotal() == None:
          line.setSubTotal(line.getQuantity()*cvad)
      
      # If information is complete but currency is wrong
      if line.getSpotCurrency() != Defaults.CURRENCY:
        change = True
        newSubTotal = CurrencyExchange.convertCurrencyAmount(line.getSubTotal(), line.getSpotCurrency(), Defaults.CURRENCY, line.getDate())
        line.setSubTotal(newSubTotal)
        newFees = CurrencyExchange.convertCurrencyAmount(line.getFees(), line.getSpotCurrency(), Defaults.CURRENCY, line.getDate())
        line.setFees(newFees)
        line.setSpotCurrency(Defaults.CURRENCY)

      # Update the statement if needed
      if change:
        self.statement.replaceLine(i, line)
      i = i + 1

  # Returns the whole portfolio value owned
  def portfolioValue(self, date, onlyBought=True):
    cryptoRegistry = self.cryptosOwned
    if onlyBought:
      cryptoRegistry = self.cryptosBought

    portfolioValue = 0
    for (cryptoName,amount) in cryptoRegistry.items():
      value = CryptoExchange.getCryptoValueAtDate(cryptoName, date)
      portfolioValue = portfolioValue + float(value)*amount
    return portfolioValue

  def examinePortfolioForTaxableGains(self):
    print('Examen des relevés', end='', flush=True)
    sumBitcoin = 0
    for line in self.statement.getStatementLines():

      if line.getCrypto() == "BTC":
        if line.isOutLine(): sumBitcoin = sumBitcoin - line.getQuantity()
        if line.isInLine(): sumBitcoin = sumBitcoin + line.getQuantity()
        if line.getLineType() == "Kraken": sumBitcoin = sumBitcoin - line.getCryptoFees() 

      if line.getLineType() == "Kraken" and line.getCryptoFees() != None:
        crypto = line.getCrypto()
        if crypto not in self.cryptosOwned.keys():
          self.cryptosOwned[crypto] = 0.00
        self.cryptosOwned[crypto] = self.cryptosOwned[crypto] - line.getCryptoFees()

      if line.isBuyLine():
        crypto = line.getCrypto()
        if crypto not in self.cryptosBought.keys():
          self.cryptosBought[crypto] = 0.00
        self.cryptosBought[crypto] = self.cryptosBought[crypto] + line.getQuantity()
        
        self.amountInvested = self.amountInvested + line.getSubTotal()

      if line.isInLine():
        crypto = line.getCrypto()
        if crypto not in self.cryptosOwned.keys():
          self.cryptosOwned[crypto] = 0.00
        self.cryptosOwned[crypto] = self.cryptosOwned[crypto] + line.getQuantity()

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
          self.taxableGainsPerYear[date.year] = 0.00
        self.taxableGainsPerYear[date.year] = self.taxableGainsPerYear[date.year] + taxableGains


        # Compute information to withdraw sold amount part in invested amount
        toWithDrawFromAmountInvested = line.getSubTotal()/percentagePlusValue
        self.amountInvested = self.amountInvested - toWithDrawFromAmountInvested

        # Remove crypto sold in owned crypto
        self.cryptosBought[crypto] = self.cryptosBought[crypto] - line.getQuantity()
        self.cryptosOwned[crypto] = self.cryptosOwned[crypto] - line.getQuantity()
    print()
    print("sumBitcoin",sumBitcoin)

  def printSummaryIfSoldRightNow(self):
    now = datetime.datetime.now() - datetime.timedelta(hours=8)
    print("Calcul de la plus-value si tout est vendu maintenant...")
    valuePortfolioOwned = self.portfolioValue(now, False)
    valuePortfolioBought = self.portfolioValue(now, True)

    percentageSold = 1 # 100%
    percentagePlusValue = valuePortfolioBought/self.amountInvested
    taxableGains = (valuePortfolioBought - self.amountInvested) * percentageSold

    print("- Valeur portefeuille de cryptos possédées : " + PortfolioHandler.printableAmount(valuePortfolioOwned))
    print("- Valeur portefeuille de cryptos achetées : " + PortfolioHandler.printableAmount(valuePortfolioBought))
    print("- Montant investi à date : " + PortfolioHandler.printableAmount(self.amountInvested))
    print("- Plus-value à déclarer pour l'année en cours : " + PortfolioHandler.printableAmount(taxableGains))

  def printSummaryPerYear(self):
    print(self.cryptosOwned)
    print("Résumé par année : ")
    for year, taxableGain in self.taxableGainsPerYear.items():
      print("- " + str(year) + " : plus-value imposable " + PortfolioHandler.printableAmount(taxableGain) + " EUR")

  @staticmethod
  def printableAmount(amount):
    return str(round(amount, 2))