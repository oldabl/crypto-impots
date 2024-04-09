import os
from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler

if __name__ == '__main__':

  print("Bienvenue dans Crypto Impots")
  print()
  statement = StatementHandler(os.path.join(os.getcwd(),'statements'))

  statement.uniqueLines()
  statement.sortDateAscending()

  print()
  portfolio = PortfolioHandler(statement)
  portfolio.examinePortfolioForTaxableGains()
  portfolio.printSummaryPerYear()

  print()
  portfolio.printSummaryIfSoldRightNow()

  print(portfolio.getCryptosOwned())
  print(portfolio.getCryptosBought())
