import os
from StatementHandler import StatementHandler

class StatementsHandler:
  def __init__(self, folderPath):
    self.folderPath = folderPath
    self.checkFolderPath()
    self.uniteAndOrganiseAllStatements()
      
  def checkFolderPath(self):
    if not os.path.exists(self.folderPath) or not os.path.isdir(self.folderPath):
      print("Folder path given is incorrect")
      raise Exception(self.folderPath)

  def uniteAndOrganiseAllStatements(self):
    allStatements = new StatementHandler()
    for filename in os.listdir(self.folderPath):
      newStatement = new StatementHandler(os.path.join(self.folderPath, filename))
      allStatements = allStatements + newStatement
    allStatements.sortByOperationDate()

      with open(os.path.join(self.folderPath, filename), 'r') as f:
        lines = f.readlines()
        for line