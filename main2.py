import os
from StatementHandler import StatementHandler

if __name__ == '__main__':

  statement = StatementHandler(os.path.join(os.getcwd(),'statements'))
  print(statement.howManyLines())
  
  statement.uniqueLines()
  statement.sortDateAscending()
  
  print(statement.howManyLines())
