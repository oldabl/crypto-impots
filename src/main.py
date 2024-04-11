import os
from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler

if __name__ == '__main__':

  print("Bienvenue dans Crypto Impots")
  print()
  statement = StatementHandler(os.path.join(os.getcwd(),'statements'))

  print()
  portfolio = PortfolioHandler(statement)

  print()
  portfolio.printSummaryPerYear()

  print()
  portfolio.printSummaryIfSoldRightNow()

  print("Cryptos Bought")
  print(portfolio.getCryptosBought())
