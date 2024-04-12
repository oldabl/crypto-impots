import datetime, logging, multiprocessing
from Exchange import CryptoExchange, CurrencyExchange
from Defaults import Defaults
from ProgressBar import ProgressBar

# Class responsible for parsing and
# extracting the information from
# an exchange platform CSV statement
class PortfolioHandler:

  cryptosBought = cryptosOwned = {}
  taxableGainsPerYear = {}

  # Constructor input:
  # - statement: StatementHandler object
  # - loadingBars: show progress bars
  def __init__(self, statement, loadingBars=True):
    self.loadingBars = loadingBars
    self.statement = statement

    # Dictionaries to count cryptos
    self.cryptosBought = {}
    self.cryptosOwned = {}

    # Track amount invested and gains per year
    self.amountInvested = 0
    self.taxableGainsPerYear = {}

    self.populateMissingInformation()
    self.examinePortfolioForTaxableGains()

  # Basic attribute getters
  def getCryptosBought(self):
    return self.cryptosBought
  def getCryptosOwned(self):
    return self.cryptosOwned
  def getAmountInvested(self):
    return self.amountInvested

  # Returns: the gain taxable for the year specified
  # If the year is invalid, return current tax year
  def getTaxableGainsPerYear(self, year=None):
    if not year:
      return self.taxableGainsPerYear
    currentYear = datetime.date.today().year
    try:
      year = int(year)
      date = datetime.datetime(year, 1, 1)
    except (Exception, ValueError):
      print("'" + str(year) + "' is not a year, will return current tax year", currentYear)
      year = currentYear
      logging.warning("Year not valid: %s", year)
    if year in self.taxableGainsPerYear.keys():
      return self.taxableGainsPerYear[year]
    else:
      return 0

  # Role: populate information that might be missing like
  # - price at which the crypto was acquired in the default currency
  # - fees in the default currency
  def populateMissingInformation(self):
    pretext = "Vérification des données des relevés "
    if self.loadingBars:
      progressbar = ProgressBar.ProgressBar(pretext=pretext, rightjustified=False)
      number = multiprocessing.Value("i", 0)
      pr = multiprocessing.Process(target=progressbar.inThread, args=(number,len(self.statement.getStatementLines())-1))
      pr.start()
    else:
      print(pretext.strip()+"...")

    # Will track the line we look at
    i = -1

    logging.debug("Here to populate missing information from some lines")

    for line in self.statement.getStatementLines():

      # Track
      i += 1

      # Update progress bar
      if self.loadingBars:
        number.value += 1

      # Flag to know if the statement needs updated
      change = False
      oldLine = line

      # Check if line is worth looking into
      if not line.isLineWorthSomething():
        logging.info("Will ignore line %d", i)
        logging.debug(line)
        continue

      # If missing information in line
      if not line.isLineInformationComplete():
        logging.debug("Line %d information incomplete, will update", i)
        logging.debug(line)

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
        logging.info("Replaced line %d", i)
        logging.debug("Old line %s", str(oldLine))
        logging.debug("New line %s", str(line))
        self.statement.replaceLine(i, line)

    # Stop progress bar
    if self.loadingBars:
      pr.join()

  # Returns: the whole portfolio value owned
  def portfolioValue(self, date, onlyBought=True):
    cryptoRegistry = self.cryptosOwned
    if onlyBought:
      cryptoRegistry = self.cryptosBought

    portfolioValue = 0
    for (cryptoName,amount) in cryptoRegistry.items():
      value = CryptoExchange.getCryptoValueAtDate(cryptoName, date)
      portfolioValue += float(value)*amount
    return portfolioValue

  # Role: go through portfolio to evaluate taxable gains
  # - will print the portfolio composition if showPortfolio=True
  def examinePortfolioForTaxableGains(self, showPortfolio=True):
    pretext = "Examen des relevés" + " "*19
    if self.loadingBars:
      progressbar = ProgressBar.ProgressBar(pretext=pretext,rightjustified=False)
      number = multiprocessing.Value("i", 0)
      pr = multiprocessing.Process(target=progressbar.inThread, args=(number,len(self.statement.getStatementLines())-1))
      pr.start()
    else:
      print(pretext.strip()+"...")

    for line in self.statement.getStatementLines():

      # Update progress bar
      if self.loadingBars:
        number.value += 1

      # Only examine if line is worth something to us
      if not line.isLineWorthSomething():
        continue

      # Look at quantities of cryptos owned in total
      #
      # Add to cryptos owned
      if line.isInLine():
        crypto = line.getCrypto()
        if crypto not in self.cryptosOwned.keys():
          self.cryptosOwned[crypto] = 0
        self.cryptosOwned[crypto] += line.getQuantity()
      #
      # Substract from cryptos owned
      if line.isOutLine():
        crypto = line.getCrypto()
        if crypto not in self.cryptosOwned.keys():
          self.cryptosOwned[crypto] = 0
        self.cryptosOwned[crypto] -= line.getQuantity()
      #
      # Substract crypto fees from quantities owned
      if line.getCryptoFees() != None:
        crypto = line.getCrypto()
        if crypto not in self.cryptosOwned.keys():
          self.cryptosOwned[crypto] = 0
        self.cryptosOwned[crypto] -= line.getCryptoFees()
      #
      # # # # # # # # # # # # # # # # # # # # # # #


      # Look at quantities of cryptos bought with time
      #
      # Add to crypto bought and workout amount of money invested
      if line.isBuyLine():
        crypto = line.getCrypto()
        if crypto not in self.cryptosBought.keys():
          self.cryptosBought[crypto] = 0
        self.cryptosBought[crypto] += line.getQuantity()

        self.amountInvested += line.getSubTotal()
      #
      # If selling crypto, remove part from amount invested and work out how much gains was made from the sale
      if line.isSellLine():
        crypto = line.getCrypto()
        if crypto == line.getSpotCurrency():
          continue
        date = line.getDate()
        valuePortfolio = self.portfolioValue(date)
        percentageSold = line.getSubTotal()/valuePortfolio if valuePortfolio > 0 else 1
        percentageGains = valuePortfolio/self.amountInvested if self.amountInvested != 0 else valuePortfolio
        taxableGains = (valuePortfolio - self.amountInvested) * percentageSold

        if date.year not in self.taxableGainsPerYear.keys():
          self.taxableGainsPerYear[date.year] = 0
        self.taxableGainsPerYear[date.year] += taxableGains

        # Compute information to withdraw sold amount part in invested amount
        toWithDrawFromAmountInvested = line.getSubTotal()/percentageGains if percentageGains > 0 else line.getSubTotal()
        self.amountInvested -= toWithDrawFromAmountInvested

        # Remove crypto sold in owned crypto
        self.cryptosBought[crypto] -= line.getQuantity()

    # Stop progress bar
    if self.loadingBars:
      pr.join()

    # Clean portfolio of useless values (like actual currency or 0)
    self.cleanPortfolioOfUselessKeys()

    # Show portfolio if asked
    if showPortfolio:
      self.printCurrentPortfolioComposition()

  # Role: clean portfolio of default currency
  def cleanPortfolioOfUselessKeys(self):
    # Remove default currency
    del self.cryptosOwned[Defaults.CURRENCY]
    # Remove crypto whose quantity is 0
    keysToDelete = []
    for key, item in self.cryptosOwned.items():
      if item == 0:
        keysToDelete.append(key)
    for key in keysToDelete:
      del self.cryptosOwned[key]

  # Role: print current portfolio composition
  def printCurrentPortfolioComposition(self):
    print("")
    print("Votre portefeuille de crypto :")

    # Will print over two columns
    sameLine = 0
    column = dict()
    for key, item in self.cryptosOwned.items():
      column[sameLine] = "- " + key.ljust(4) + ": " + PortfolioHandler.roundCryptoQuantity(item)
      if sameLine == 1:
        print('{0:30}  {1}'.format(column[0], column[1]))
      sameLine = (sameLine + 1) % 2

  # Role: Print summary if the portfolio
  #  was sold immediately
  def printSummaryIfSoldRightNow(self):
    now = datetime.datetime.now() - datetime.timedelta(hours=8)
    print("Calcul de la plus-value si tout est vendu maintenant...")
    valuePortfolioOwned = self.portfolioValue(now, False)
    valuePortfolioBought = self.portfolioValue(now, True)

    percentageSold = 1 # 100%
    percentageGains = valuePortfolioBought/self.amountInvested
    taxableGains = (valuePortfolioBought - self.amountInvested) * percentageSold

    print("- Valeur actuelle du portefeuille :\n   " + PortfolioHandler.roundCurrency(valuePortfolioOwned))
    print("- Valeur actuelle du portefeuille ramené aux achats :\n   " + PortfolioHandler.roundCurrency(valuePortfolioBought))
    print("- Montant investi à date :\n   " + PortfolioHandler.roundCurrency(self.amountInvested))
    print("- Plus-value à déclarer pour l'année en cours :\n   " + PortfolioHandler.roundCurrency(taxableGains))

  # Role: prints a summary of taxable gains per year
  def printSummaryPerYear(self):
    print("Résumé par année : ")
    for year, taxableGain in self.taxableGainsPerYear.items():
      print("- " + str(year) + " : plus-value imposable " + PortfolioHandler.roundCurrency(taxableGain) + " EUR")

  # Round currency for printing (two decimals)
  @staticmethod
  def roundCurrency(amount):
    return str(round(amount, 2))

  # Round currency for printing (8 decimals)
  @staticmethod
  def roundCryptoQuantity(amount):
    return str(round(amount, 8))