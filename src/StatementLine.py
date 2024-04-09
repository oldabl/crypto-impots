from Defaults import Defaults
from KrakenLine import KrakenLine
from CoinbaseLine import CoinbaseLine

class StatementLine:

  # Options as to where the line could come from
  lineOptions = Defaults.platformsCompatible

  # Constructor inputs:
  #  - statementLine: current line processed
  #  - previousStatementLine: line preceding the current line if exists
  def __init__(self, statementLine, previousStatementLine=None):
    self.statementLine = statementLine.rstrip()
    self.previousStatementLine = previousStatementLine
    # Immediate call to extract information
    self.gatherAllInformation()

  # Role: extract all information about operation from line
  #   and attempt to find which exchange platform the line comes from
  def gatherAllInformation(self):

    # Look at all attributes and determine which
    #   exchange platform it comes from
    optionSuccess = False
    for option in self.lineOptions:
      # Call option-associated function (Coinbase -> self.tryCoinbase())
      optionSuccess = eval(option+"Line("++")")
      # Stop looking if we have managed to extract info
      if optionSuccess:
        self.lineType = option
        break
    
    # Update flags
    if not optionSuccess:
      self.isStatementLineInvalid = True
      self.lineOptions = []
