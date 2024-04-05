import os
from StatementLine import StatementLine

class StatementHandler:
  def __init__(self, path):
    self.path = path
    self.isDir = False
    self.statementLines = []
    self.checkPath()
    if self.isDir:
      print("Parse directory " + self.path)
      self.checkForStatementsInDir()
    else: # if it's a file
      print(" - Look in file "+ self.path)
      self.gatherInformationFromStatement()

  def __str__(self):
    printString = "["
    firstLoop = True
    for stl in self.statementLines:
      if firstLoop:
        printString = printString + str(stl)
        firstLoop = False
      else:
        printString = printString + "," + os.linesep + str(stl)
    printString = printString + "]"
    return printString

  def __repr__(self):
    return "StatementHandler("+self.path+")"

  def howManyLines(self):
    return len(self.statementLines)

  def getBuyAndSellLines(self):
    buyAndSellLines = []
    for line in self.statementLines:
      if line.isBuyLine() or line.isSellLine():
        buyAndSellLines.append(line)
    return buyAndSellLines

  def getAllStatementLines(self):
    return self.statementLines

  def checkPath(self):
    if not os.path.exists(self.path):
      self.errorPathIncorrect()
    elif os.path.isdir(self.path):
      self.isDir = True
    elif os.path.isfile(self.path):
      self.isDir = False
    else:
      self.errorPathIncorrect()

  def errorPathIncorrect(self):
    raise Exception("Folder path given is incorrect: " + self.path)

  def checkForStatementsInDir(self):
    for filename in os.listdir(self.path):
      newStatement = StatementHandler(os.path.join(self.path, filename))
      self.statementLines = self.statementLines + newStatement.getAllStatementLines()

  def gatherInformationFromStatement(self):
    with open(self.path, 'r') as f:
      lines = f.readlines()
      for line in lines:
        statementLine = StatementLine(line)
        if statementLine.isStatementLineValid():
          self.statementLines.append(statementLine)

  def sortDateAscending(self):
    self.statementLines.sort(key=lambda stl: stl.getDate())

  def uniqueLines(self):
    uniqueLines = []
    uniqueStatementLines = []
    for stl in self.statementLines:
      if str(stl) not in uniqueLines:
        uniqueStatementLines.append(stl)
        uniqueLines.append(str(stl))
    self.statementLines = uniqueStatementLines
