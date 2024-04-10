
# Class responsible for extracting and
# holding the information of a line from
# an exchange platform CSV statement

# Possibilities for class members:
# - opType: Buy, Sell, Receive, Withdrawal, Send,
#            Convert, Staking Income, Learning Reward
# - crypto: crypto symbol (BTC, DOGE, etc...)
# spotCurrency: EUR or USD

class PlatformLine:

  # Attributes that class will attempt to extract
  date = opType = crypto = None
  quantity = spotCurrency = None
  spotPrice = subTotal = None
  fees = None

  # Will store the subclass type
  lineType = None

  # For debug purposes, will store raw data
  rawData = {}

  # Flag for determining if line is valid
  isLineFormatValid = False
  isLineInformationComplete = False

  # Constructor inputs:
  #  - textStatementLine: current line processed
  #  - previousStatementLine: previous StatementLine already analysed
  def __init__(self, textStatementLine, previousStatementLine=None):
    self.textStatementLine = textStatementLine.strip()
    self.previousStatementLine = previousStatementLine
    # Immediate call to extract information
    self.extractInformation()

  # Basic attribute getters
  def isFormatValid(self):
    return self.isLineFormatValid
  def isInformationComplete(self):
    return self.isLineInformationComplete
  def getDate(self):
    return self.date
  def getOpType(self):
    return self.opType
  def getCrypto(self):
    return self.crypto
  def getQuantity(self):
    return self.quantity
  def getSpotCurrency(self):
    return self.spotCurrency
  def getSpotPrice(self):
    return self.spotPrice
  def getSubTotal(self):
    return self.subTotal
  def getFees(self):
    return self.fees
  def getLineOptions(self):
    return self.lineOptions
  def getLineType(self):
    return self.lineType
  def getRawData(self):
    return self.rawData

  # Basic attribute setters
  def setFees(self, fees):
    self.fees = fees
  def setSubTotal(self, subTotal):
    self.subTotal = subTotal
  def setSpotCurrency(self, spotCurrency):
    self.spotCurrency = spotCurrency
  def setSpotPrice(self, spotPrice):
    self.spotPrice = spotPrice
  def setInformationComplete(self, isComplete):
    self.isLineInformationComplete = isComplete
  def setRawData(self, rawData):
    self.rawData = rawData

  # Role: sets validity flags to all good
  def setEverythingValid(self):
    self.isLineFormatValid = True
    self.isLineInformationComplete = True

  # Role: sets validity flags to all bad
  def setNothingValid(self):
    self.isLineFormatValid = False
    self.isLineInformationComplete = False

  # Returns:
  #  - true if line is an operation that buys crypto
  #  - false otherwise
  def isBuyLine(self):
    return self.getOpType() == "Buy"

  # Returns:
  #  - true if line is an operation that regards crypto entering the wallet
  #  - false otherwise
  def isInLine(self):
    return self.getOpType() in ["Buy", "Staking Income", "Learning Reward", "Receive"]

  # Returns:
  #  - true if line is an operation that sells crypto
  #  - false otherwise
  def isSellLine(self):
    return self.getOpType() == "Sell"

  # Returns:
  #  - true if line is an operation that regards crypto exiting the wallet
  #  - false otherwise
  def isOutLine(self):
    return self.getOpType() in ["Sell", "Withdraw", "Send"]

  # Role: perform basic checks for whether a line might be invalid
  def basicLineChecks(self):
    if(not self.textStatementLine or
      self.textStatementLine == ""
      or "," not in self.textStatementLine):
      self.setNothingValid()
      return False

  # Role: keeps the raw data from the line in an array
  def setRawData(self, splitData):
    if len(splitData) == len(self.listData):
      for i in range(0,len(splitData)):
        self.rawData[self.listData[i]] = splitData[i]
    else:
      raise IndexError("Data not extractable")

  # Human readable class functions
  def __str__(self):
    if self.isFormatValid():
      return str({
                  'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
                  'opType': self.opType,
                  'crypto': self.crypto,
                  'quantity': self.quantity,
                  'spotCurrency': self.spotCurrency,
                  'spotPrice': self.spotPrice,
                  'subTotal': self.subTotal,
                  'fees': self.fees,
                  'lineType': self.lineType
                })
    return "Invalid statement line"
  def __repr__(self):
    return "StatementLine("+self.textStatementLine+")"
