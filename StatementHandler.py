import os, datetime

class StatementHandler:
  def __init__(self, statementFilePath):
    self.statementFilePath = statementFilePath
    self.checkStatementFilePath()
    self.gatherAllInformation()
      
  def checkFolderPath(self):
    if not os.path.exists(self.statementFilePath) or not os.path.isfile(self.statementFilePath):
      print("File path given is incorrect")
      raise Exception(self.statementFilePath)

  def gatherAllInformation(self):
    with open(os.path.join(self.folderPath, filename), 'r') as f:
      lines = f.readlines()
      for line in lines:
        

