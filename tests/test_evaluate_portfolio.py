# test_evaluate_portfolio.py

import sys, os
from unittest.mock import Mock, MagicMock
# FOR LOCAL RUN
if __name__ == '__main__':
  sys.path.append('src')
  sys.path.append('tests')
# FOR LOCAL RUN

def makeFullPath(path):
  return os.path.join(os.getcwd(), 'tests', path)

from StatementHandler import StatementHandler
from PortfolioHandler import PortfolioHandler
from Exchange import CryptoExchange, CurrencyExchange

def test_portfolio_from_statement_matches_platform_values():
  print("test_portfolio_from_statement_matches_platform_values()")
  sth = StatementHandler(makeFullPath('test_files/statements/real/'))

  portfolio = PortfolioHandler(sth, loadingBars=False)

  platformValues = {
    'BTC': '0.01525753', 'ETH': '0.11860456',
    'XLM': '29.8295733', 'FET': '4.01625122',
    'GRT': '25.24859345', 'AMP': '159.53212373',
    'LTC': '1.33607457', 'FIL': '0.98077875',
    'CRO': '50.31572195', 'SOL': '0.05721957',
    'SHIB': '314846.56679405', 'CLV': '67.80662592',
    'DOGE': '126.32311693', 'FIDA': '30.066464',
    'SAND': '3.1751083', 'GAL': '1.19601431',
    'NEAR': '0.69916509', 'XCN': '66.94582892',
    'TIME': '0.14772372', 'USDC': '0.175426'
  }
  for key,item in portfolio.getCryptosOwned().items():
    assert PortfolioHandler.roundCryptoQuantity(item) == platformValues[key]

def test_evaluate_taxable_gains():
  print("test_evaluate_taxable_gains_no_year()")
  sth = StatementHandler(makeFullPath('test_files/statements/portfolio_evaluation/portfoliostatement.csv'))
  sth.uniqueLines()
  sth.sortDateAscending()

  resultExpected = {2023: -0.8665641249477958, 2024: 891.8719901994936}
  
  portfolio = PortfolioHandler(sth, loadingBars=False)

  assert type(portfolio.getTaxableGainsPerYear()) is dict
  assert type(portfolio.getTaxableGainsPerYear("")) is dict
  assert portfolio.getTaxableGainsPerYear("2023") == portfolio.getTaxableGainsPerYear(2023)
  assert portfolio.getTaxableGainsPerYear("HJBJK7") == portfolio.getTaxableGainsPerYear(2024)
  assert portfolio.getTaxableGainsPerYear(2022) == 0
  assert portfolio.getTaxableGainsPerYear(2024) == resultExpected[2024]
  assert portfolio.getTaxableGainsPerYear() == resultExpected

# FOR LOCAL RUN
if __name__ == '__main__':
  test_evaluate_taxable_gains()
  test_portfolio_from_statement_matches_platform_values()
# FOR LOCAL RUN
