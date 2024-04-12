import os, sys
from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler

if __name__ == '__main__':

  print("Bienvenue dans Crypto Impots")
  print()
  statement = StatementHandler(os.path.join(os.getcwd(),'statements'))

  print()
  portfolio = PortfolioHandler(statement, loadingBars = sys.stdout.isatty())

  print()
  portfolio.printSummaryPerYear()

  print()
  portfolio.printSummaryIfSoldRightNow()
