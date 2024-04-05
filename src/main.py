import os
from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler

if __name__ == '__main__':

  statement = StatementHandler(os.path.join(os.getcwd(),'statements'))

  statement.uniqueLines()
  statement.sortDateAscending()
  
  portfolio = PortfolioHandler(statement)
  portfolio.examinePortfolioForTaxableGains()
  portfolio.summaryPerYear()
