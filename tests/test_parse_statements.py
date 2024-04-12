# test_parse_statements.py

import sys, pytest, os
# FOR LOCAL RUN
if __name__ == '__main__':
  sys.path.append('src')
  sys.path.append('tests')
# FOR LOCAL RUN

def makeFullPath(path):
  return os.path.join(os.getcwd(), 'tests', path)

from StatementHandler import StatementHandler

def test_wrong_path():
  print("test_wrong_path()")
  with pytest.raises(Exception, match="Folder path given is incorrect: fake/path"):
    StatementHandler('fake/path')
    
def test_parse_single_statement_in_folder():
  print("test_parse_single_statement_in_folder()")
  sth = StatementHandler(makeFullPath('test_files/statements/single'))
  assert sth.howManyLines() == 20

def test_parse_single_statement_file():
  print("test_parse_single_statement_file()")
  sth = StatementHandler(makeFullPath('test_files/statements/single/statement.csv'))
  assert sth.howManyLines() == 20

def test_parse_several_statements_one_folder_no_duplicates():
  print("test_parse_several_statements_one_folder_no_duplicates()")
  sth = StatementHandler(makeFullPath('test_files/statements/several/no_duplicates'))
  assert sth.howManyLines() == 95

def test_parse_several_statements_one_folder_with_duplicates():
  print("test_parse_several_statements_one_folder_with_duplicates()")
  sth = StatementHandler(makeFullPath('test_files/statements/several/duplicates'))
  assert sth.howManyLines() == 10
  sth.uniqueLines()
  assert sth.howManyLines() == 6

def test_parse_several_statements_one_file_only_invalid():
  print("test_parse_several_statements_one_file_only_invalid()")
  sth = StatementHandler(makeFullPath('test_files/statements/only_invalid.csv'))
  assert sth.howManyLines() == 0

def test_parse_several_statements_sort_by_date():
  print("test_parse_several_statements_sort_by_date()")
  sth = StatementHandler(makeFullPath('test_files/statements/several/no_duplicates'))
  # Test wrong before sorting
  foundUnsortedDates = False
  old_date = None
  for line in sth.getStatementLines():
    if old_date:
      if not line.getDate() >= old_date:
        foundUnsortedDates = True
        break
    old_date = line.getDate()
  assert foundUnsortedDates == False

# FOR LOCAL RUN
if __name__ == '__main__':
  test_wrong_path()
  test_parse_single_statement_in_folder()
  test_parse_single_statement_file()
  test_parse_several_statements_one_folder_no_duplicates()
  test_parse_several_statements_one_folder_with_duplicates()
  test_parse_several_statements_one_file_only_invalid()
  test_parse_several_statements_sort_by_date()
# FOR LOCAL RUN
