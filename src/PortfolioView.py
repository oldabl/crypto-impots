import time, datetime, logging
from PortfolioHelpers import PortfolioHelpers
from Defaults import Defaults

# Class responsible for handling all
# outputs with data from a Portfolio
# of type PortfolioHandler
class PortfolioView:
  
  portfolio = None

  # Constructor
  #  with PortfolioHandler parameter
  def __init__(self, portfolio):
    self.portfolio = portfolio

  # Role: print current portfolio composition
  def printCurrentPortfolioComposition(self):
    print("")
    print("Votre portefeuille de crypto :")

    # Will print over two columns
    sameLine = 0
    column = dict()
    for key, item in self.portfolio.getCryptosOwned().items():
      column[sameLine] = "- " + key.ljust(4) + ": " + PortfolioHelpers.roundCryptoQuantity(item)
      if sameLine == 1:
        PortfolioView.ptc(column[0], column[1], 30)
        time.sleep(0.05)
      sameLine = (sameLine + 1) % 2

  # Role: Print summary if the portfolio
  #  was sold immediately
  def printSummaryIfSoldRightNow(self):
    now = datetime.datetime.now() - datetime.timedelta(hours=8)

    print("Informations actuelles du portefeuille :")

    PortfolioView.ptc("- Montant investi : ", PortfolioHelpers.roundCurrency(self.portfolio.getAmountInvested(), Defaults.CURRENCY), 20)

    valuePortfolioOwned = PortfolioHelpers.portfolioValue(self.portfolio, now, False)
    PortfolioView.ptc("- Valorisation : ", PortfolioHelpers.roundCurrency(valuePortfolioOwned, Defaults.CURRENCY), 20)

    valuePortfolioBought = PortfolioHelpers.portfolioValue(self.portfolio, now, True)
    # print("- Valeur actuelle du portefeuille ramené aux achats :\n   " + PortfolioHelpers.roundCurrency(valuePortfolioBought))

    percentageGains = valuePortfolioOwned/self.portfolio.getAmountInvested()
    gains = valuePortfolioOwned - self.portfolio.getAmountInvested()
    
    PortfolioView.ptc("- Plus-value : ", PortfolioHelpers.roundCurrency(gains, Defaults.CURRENCY), 20)

    ptd = ("+",(percentageGains*100-100)) if percentageGains >= 1 else ("-",(100 - percentageGains*100))
    PortfolioView.ptc("- Plus-value % : ", ptd[0]+PortfolioHelpers.roundCurrency(ptd[1]) + "%", 20)

  # Role: prints a summary of taxable gains per year
  def printSummaryPerYear(self):
    print("Plus-value imposable par année : ")
    for year, taxableGain in self.portfolio.getTaxableGainsPerYear().items():
      time.sleep(0.05)
      print("- " + str(year) + " : " + PortfolioHelpers.roundCurrency(taxableGain, Defaults.CURRENCY))

  # Role: print in two columns
  @staticmethod
  def ptc(column1, column2, widthFirstColumn):
    formatStyle = "{0:"+str(widthFirstColumn)+"}  {1}"
    print(formatStyle.format(column1, column2))
