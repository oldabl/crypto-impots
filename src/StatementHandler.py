import os
from Defaults import Defaults
from KrakenLine import KrakenLine
from CoinbaseLine import CoinbaseLine

# Class responsible for parsing and
# extracting the information from
# an exchange platform CSV statement
class StatementHandler:

  # Flag for if path passed to class 
  #  is a directory
  isDir = False

  # Variable that will hold all statement lines
  statementLines = []

  # Constructor input:
  #  - path: path to statement file or folder
  def __init__(self, path):
    self.path = path
    # Will check if path is valid
    self.checkPath()

    if self.isDir: # Path is directory, we look inside
      print("Examen du dossier " + self.path)
      self.checkForStatementsInDir()
    else: # Path is a file, we examine the file
      print(" - Relevé disponible : "+ os.path.basename(self.path))
      self.gatherInformationFromStatement()

  # Basic attribute getters
  def getStatementLines(self):
    return self.statementLines
  def getPath(self):
    return self.path
  def isDir(self):
    return self.isDir
  def howManyLines(self):
    return len(self.statementLines)

  # Role: update line at index in list statementLines
  def replaceLine(self, index, newLine):
    self.statementLines[index] = newLine

  # Returns: all lines regarding buying or selling crypto
  def getBuyAndSellLines(self):
    buyAndSellLines = []
    for line in self.statementLines:
      if line.isBuyLine() or line.isSellLine():
        buyAndSellLines.append(line)
    return buyAndSellLines

  # Role: check if class member 'path'
  #  is valid and exists on disk
  def checkPath(self):
    if not self.path:
      self.errorPathIncorrect()
    elif not os.path.exists(self.path):
      self.errorPathIncorrect()
    elif os.path.isdir(self.path):
      self.isDir = True
    elif os.path.isfile(self.path):
      self.isDir = False
    else:
      self.errorPathIncorrect()

  # Role: raise error if path given is incorrect
  def errorPathIncorrect(self):
    raise Exception("Folder path given is incorrect: " + self.path)

  # Role: browse folder looking for files and folders
  #  in class member 'path'
  def checkForStatementsInDir(self):
    if not self.isDir:
      return
    # If member 'path' is a folder, look through it
    for filename in os.listdir(self.path):
      # Add new paths found to list of statement lines
      newStatement = StatementHandler(os.path.join(self.path, filename))
      self.statementLines = self.statementLines + newStatement.getStatementLines()

  # Role: gather all information from statement file
  def gatherInformationFromStatement(self):
    if self.isDir:
      return

    # Will read all lines from file
    #  in class member 'path'
    with open(self.path, 'r') as f:
      lines = f.readlines()
      previousLine = None
      

      # Go through all lines...
      for line in lines:
        # ... and send them for analysis
        for option in Defaults.platformsCompatible:
          statementLine = eval(option+"Line")(line, previousLine)

          # If line is valid, add it to list
          if statementLine.isFormatValid():
            self.statementLines.append(statementLine)

            # Save current line for next loop iteration
            previousLine = statementLine
            break

  # Role: sort the list of lines by ascending date
  def sortDateAscending(self):
    self.statementLines.sort(key=lambda stl: stl.getDate())

  # Role: make sure there are no line duplicates
  #  in the list of lines
  def uniqueLines(self):
    uniqueLines = []
    uniqueStatementLines = []

    # Parse all statement lines
    for stl in self.statementLines:

      # If not already saved in unique list...
      if str(stl) not in uniqueLines:
        # ... add it to unique list
        uniqueStatementLines.append(stl)
        uniqueLines.append(str(stl))

    # Make statement lines class member unique
    self.statementLines = uniqueStatementLines

  # Human readable class functions
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
