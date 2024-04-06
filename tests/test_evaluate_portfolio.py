# test_evaluate_portfolio.py

import sys, pytest, os
# FOR LOCAL RUN
if __name__ == '__main__':
  sys.path.append('src')
  sys.path.append('tests')
# FOR LOCAL RUN

def makeFullPath(path):
  return os.path.join(os.getcwd(), 'tests', path)

from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler

def test_evaluate_taxable_gains(mocker):
  result = {2023: -0.8665641249477958, 2024: 947.8437781903135}
  mocker.patch('PortfolioHandler.PortfolioHandler.getTaxableGainsPerYear', return_value=result)
  
  sth = StatementHandler(makeFullPath('test_files/statements/portfolio_evaluation/portfoliostatement.csv'))
  sth.uniqueLines()
  sth.sortDateAscending()
  
  portfolio = PortfolioHandler(sth)
  #portfolio.examinePortfolioForTaxableGains()

  assert portfolio.getTaxableGainsPerYear() == result
  assert portfolio.getTaxableGainsPerYear("") == result
  assert portfolio.getTaxableGainsPerYear("2023") == result[2023]
  assert portfolio.getTaxableGainsPerYear(2023) == result[2023]
  assert portfolio.getTaxableGainsPerYear(10000000) == result
  assert portfolio.getTaxableGainsPerYear(2024) == result[2024]
  assert portfolio.getTaxableGainsPerYear(2022) == 0
  assert portfolio.getTaxableGainsPerYear("HJBJK7") == result


# FOR LOCAL RUN
if __name__ == '__main__':
  #Only available on GitHub: test_evaluate_taxable_gains()
  pass
# FOR LOCAL RUN
