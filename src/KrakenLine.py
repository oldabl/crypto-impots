import datetime, logging
from Defaults import Defaults
from StatementLine import StatementLine

class KrakenLine(StatementLine):

  listData = ['txid',
              'refid',
              'time',
              'type',
              'subtype',
              'aclass',
              'asset',
              'amount',
              'fee',
              'balance']

  transactionId = None
  asset = None
  type = None
  amount = None
  cryptoFees = 0.0

  # To set the line type before calling parent
  def __init__(self, textStatementLine, previousStatementLine=None):
    self.lineType = "Kraken"
    super().__init__(textStatementLine, previousStatementLine)

  # Basic attribute getters
  def getTransactionId(self):
    return self.transactionId
  def getType(self):
    return self.type
  def getAmount(self):
    return self.amount
  def getAsset(self):
    return self.asset
  def getCryptoFees(self):
    return self.cryptoFees

  # Role: try to extract if line matches Kraken statement
  # 0: txid  1: refid  2: time
  # 3: type  4: subtype
  # 5: aclass  6: asset
  # 7: amount
  # 8: fee  9: balance
  def extractInformation(self):
    super().basicLineChecks()

    # Split attributes of the CSV file
    c = self.textStatementLine.split(",")
    if len(c) != len(self.listData):
      self.setNothingValid()
      return False
    
    # Set raw data
    try:
      super().setRawData(c)
    except IndexError:
      self.setNothingValid()
      return False

    # Look for information in line
    try:
      # Remove all trailing double quotes
      c = [x.strip('"').strip() for x in c]

      # If first ID is null we ignore it
      if c[0] == "": return False

      self.date = datetime.datetime.strptime(c[2], "%Y-%m-%d %H:%M:%S")
      self.transactionId = c[1]
      self.type = str(c[3])
      self.asset = str(c[6])
      self.amount = abs(float(c[7]))
      self.isLineFormatValid = True

      # If crypto was bought
      #  (previous and current line are linked)
      if (self.previousStatementLine and
          self.type in ["receive", "spend"] and
          self.previousStatementLine.getTransactionId() == self.transactionId and
          self.previousStatementLine.getType() in ["spend", "receive"]):
        self.opType = "Buy"
        self.crypto = c[6]
        if self.crypto[0] == 'X': self.crypto = c[6][1:]
        if self.crypto == "XBT" : self.crypto = "BTC"
        self.quantity = abs(float(c[7]))
        self.spotCurrency = self.previousStatementLine.getAsset().split('.')[0]
        self.subTotal = abs(float(self.previousStatementLine.getAmount()))
        self.spotPrice = self.subTotal/self.amount # Estimated
        self.fees = abs(float(self.previousStatementLine.getRawData()['fee']))
        self.isLineInformationComplete = True
      # If deposit not into Kraken EUR hold, count it as Buy
      elif c[3] == "deposit" and not "HOLD" in c[6]:
        self.opType = "Buy"
        self.crypto = c[6]
        if self.crypto[0] == 'X': self.crypto = c[6][1:]
        if self.crypto == "XBT" : self.crypto = "BTC"
        self.quantity = abs(float(c[7]))
        self.spotCurrency = Defaults.CURRENCY
        self.subTotal = None
        self.spotPrice = None
        self.cryptoFees = abs(float(c[8]))
      # If withdrawal from crypto account
      elif c[3] == "withdrawal":
        self.opType = "Send"
        self.crypto = c[6]
        if self.crypto[0] == 'X': self.crypto = c[6][1:]
        if self.crypto == "XBT" : self.crypto = "BTC"
        self.quantity = abs(float(c[7]))
        self.spotCurrency = Defaults.CURRENCY
        self.subTotal = None
        self.spotPrice = None
        self.cryptoFees = abs(float(c[8]))
        self.totalWFees = None
        self.desc = c[1]
    except Exception as e:
      self.setNothingValid()
      logging.debug("Couldn't extract information")
      return False # If failed to parse properly line

    # If no error occured
    self.setEverythingValid()
    return True

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
                  'cryptoFees': self.cryptoFees,
                  'lineType': self.lineType
                })
    return "Invalid statement line"
