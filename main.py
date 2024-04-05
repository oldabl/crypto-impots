import os
from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler

if __name__ == '__main__':

  statement = StatementHandler(os.path.join(os.getcwd(),'statements'))
  print(statement.howManyLines())
  
  statement.uniqueLines()
  statement.sortDateAscending()
  
  print(statement.howManyLines())
  
  portfolio = PortfolioHandler(statement)
  portfolio.examinePortfolioForTaxableGains()
  portfolio.summaryPerYear()
