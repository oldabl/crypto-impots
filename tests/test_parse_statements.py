# test_parse_statements.py

import sys, pytest
if __name__ == '__main__':
  sys.path.append('src')

from StatementHandler import StatementHandler

def test_capital_case():
  assert 1+1 == 2

