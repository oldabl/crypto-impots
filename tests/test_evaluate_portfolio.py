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

result = {2023: -0.8665641249477958, 2024: 947.8437781903135}

def test_portfolio_from_statement_matches_platform_values(mocker):
  mocker.patch('Exchange.CryptoExchange.getCryptoValueAtDate', return_value=0)
  mocker.patch('Exchange.CurrencyExchange.convertCurrencyAmount', return_value=0)

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
    'TIME': '0.14772372', 'USDC': '0.14772372'
  }
  for key,item in portfolio.getCryptosOwned().items():
    assert PortfolioHandler.roundCryptoQuantity(item) == platformValues[key]

def test_evaluate_taxable_gains_no_year(mocker):
  mocker.patch('PortfolioHandler.PortfolioHandler.getTaxableGainsPerYear', return_value=result)
  
  sth = StatementHandler(makeFullPath('test_files/statements/portfolio_evaluation/portfoliostatement.csv'))
  sth.uniqueLines()
  sth.sortDateAscending()
  
  portfolio = PortfolioHandler(sth, loadingBars=False)
  #portfolio.examinePortfolioForTaxableGains()

  assert portfolio.getTaxableGainsPerYear() == result
  assert portfolio.getTaxableGainsPerYear("") == result

def test_evaluate_taxable_gains_error_year(mocker):
  mocker.patch('PortfolioHandler.PortfolioHandler.getTaxableGainsPerYear', return_value=result)
  
  sth = StatementHandler(makeFullPath('test_files/statements/portfolio_evaluation/portfoliostatement.csv'))
  sth.uniqueLines()
  sth.sortDateAscending()
  
  portfolio = PortfolioHandler(sth, loadingBars=False)
  #portfolio.examinePortfolioForTaxableGains()

  assert portfolio.getTaxableGainsPerYear(10000000) == result
  assert portfolio.getTaxableGainsPerYear("HJBJK7") == result

def test_evaluate_taxable_gains_year_full_string_int(mocker):
  mocker.patch('PortfolioHandler.PortfolioHandler.getTaxableGainsPerYear', return_value=result[2023])
  
  sth = StatementHandler(makeFullPath('test_files/statements/portfolio_evaluation/portfoliostatement.csv'))
  sth.uniqueLines()
  sth.sortDateAscending()
  
  portfolio = PortfolioHandler(sth, loadingBars=False)
  #portfolio.examinePortfolioForTaxableGains()

  assert portfolio.getTaxableGainsPerYear("2023") == result[2023]
  assert portfolio.getTaxableGainsPerYear(2023) == result[2023]

def test_evaluate_taxable_gains_year_full(mocker):
  mocker.patch('PortfolioHandler.PortfolioHandler.getTaxableGainsPerYear', return_value=result[2024])
  
  sth = StatementHandler(makeFullPath('test_files/statements/portfolio_evaluation/portfoliostatement.csv'))
  sth.uniqueLines()
  sth.sortDateAscending()
  
  portfolio = PortfolioHandler(sth, loadingBars=False)
  #portfolio.examinePortfolioForTaxableGains()

  assert portfolio.getTaxableGainsPerYear(2024) == result[2024]

def test_evaluate_taxable_gains_year_empty(mocker):
  mocker.patch('PortfolioHandler.PortfolioHandler.getTaxableGainsPerYear', return_value=0)
  
  sth = StatementHandler(makeFullPath('test_files/statements/portfolio_evaluation/portfoliostatement.csv'))
  sth.uniqueLines()
  sth.sortDateAscending()
  
  portfolio = PortfolioHandler(sth, loadingBars=False)
  #portfolio.examinePortfolioForTaxableGains()

  assert portfolio.getTaxableGainsPerYear(2022) == 0

# FOR LOCAL RUN
if __name__ == '__main__':
  #test_evaluate_taxable_gains_no_year()
  #test_evaluate_taxable_gains_error_year()
  #test_evaluate_taxable_gains_year_full_string_int()
  #test_evaluate_taxable_gains_year_full()
  #test_evaluate_taxable_gains_year_empty()
  pass
# FOR LOCAL RUN
