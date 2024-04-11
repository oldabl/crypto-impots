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
  cryptoFees = None

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
  def getFee(self):
    return self.fee

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
      self.fee = abs(float(c[8]))
      self.lineFormatValid = True
      self.lineWorthSomething = False

      # If crypto was bought
      #  (previous and current line are linked)
      if (self.previousStatementLine and
          self.type in ["receive", "spend"] and
          self.previousStatementLine.getTransactionId() == self.transactionId and
          self.previousStatementLine.getType() in ["spend", "receive"]):

        if self.type == "receive" and self.previousStatementLine.getType() == "spend":
          self.opType = "Buy"
          self.crypto = KrakenLine.formatCrypto(c[6])
          self.quantity = abs(float(c[7]))
          self.spotCurrency = self.previousStatementLine.getAsset().split('.')[0]
          self.subTotal = abs(float(self.previousStatementLine.getAmount()))
          self.spotPrice = self.subTotal/self.amount # Estimated
          self.fees = abs(float(self.previousStatementLine.getRawData()['fee']))
          self.lineInformationComplete = True
          self.discardPreviousLine = True
          self.lineWorthSomething = True

        elif self.type == "spend" and self.previousStatementLine.getType() == "receive":
          self.opType = "Buy"
          self.crypto = KrakenLine.formatCrypto(self.previousStatementLine.getAsset())
          self.quantity = abs(float(self.previousStatementLine.getAmount()))
          self.spotCurrency = c[6].split('.')[0]
          self.subTotal = abs(float(c[7]))
          self.spotPrice = self.subTotal/self.previousStatementLine.getAmount() # Estimated
          self.fees = self.previousStatementLine.getFee()
          self.lineInformationComplete = True
          self.discardPreviousLine = True
          self.lineWorthSomething = True

      # If deposit not into Kraken EUR hold, count it as Buy
      if c[3] == "deposit" and not "HOLD" in c[6]:
        self.opType = "Buy"
        self.crypto = KrakenLine.formatCrypto(c[6])
        self.quantity = abs(float(c[7]))
        self.spotCurrency = Defaults.CURRENCY
        self.subTotal = None
        self.spotPrice = None
        self.cryptoFees = abs(float(c[8]))
        self.lineWorthSomething = True

      # If withdrawal from crypto account
      if c[3] == "withdrawal":
        self.opType = "Send"
        self.crypto = KrakenLine.formatCrypto(c[6])
        self.quantity = abs(float(c[7]))
        self.spotCurrency = Defaults.CURRENCY
        self.subTotal = None
        self.spotPrice = None
        self.cryptoFees = abs(float(c[8]))
        self.totalWFees = None
        self.lineWorthSomething = True

    except Exception as e:
      self.setNothingValid()
      logging.debug("Couldn't extract information")
      return False # If failed to parse properly line

  # Role: format crypto coming from Kraken statement line
  # Examples: FIDA -> FIDA
  #           XXBT -> BTC
  #           XLTC -> LTC
  @staticmethod
  def formatCrypto(crypto):
    if crypto[0] == 'X': crypto = crypto[1:]
    if crypto == "XBT" : crypto = "BTC"
    return crypto

  # Human readable class functions
  def __str__(self):
    if self.isLineFormatValid():
      return str({
                  'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
                  'opType': self.opType,
                  'crypto': self.crypto,
                  'quantity': self.quantity,
                  'spotCurrency': self.spotCurrency,
                  'spotPrice': self.spotPrice,
                  'subTotal': self.subTotal,
                  'fees': self.fees,
                  'cryptoFees': self.cryptoFees if self.cryptoFees != None else 0.0,
                  'lineType': self.lineType
                })
    return "Invalid statement line"
