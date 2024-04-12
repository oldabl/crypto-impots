import os, sys
from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler
from PortfolioView import PortfolioView

if __name__ == '__main__':

  print("Bienvenue dans Crypto Impots\n")

  statement = StatementHandler(os.path.join(os.getcwd(),'statements'))

  print()
  portfolio = PortfolioHandler(statement, loadingBars = sys.stdout.isatty())

  portfolioView = PortfolioView(portfolio)

  print()
  portfolioView.printCurrentPortfolioComposition()

  print()
  portfolioView.printSummaryPerYear()

  print()
  portfolioView.printSummaryIfSoldRightNow()
