import datetime
from PlatformLine import PlatformLine
from Defaults import Defaults

class KrakenLine(PlatformLine):

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

      # If crypto was bought
      #  (previous and current line are linked)
      if (self.previousStatementLine and
          c[3] in ["receive", "spend"] and
          self.previousStatementLine.getcpre[3] in ["receive", "spend"] and
          c[1] == cpre[1]):
        print(cpre[3])
        print("WITH PREVIOUS LINE")
        self.opType = "Buy"
        self.crypto = c[6]
        if self.crypto[0] == 'X': self.crypto = c[6][1:]
        if self.crypto == "XBT" : self.crypto = "BTC"
        self.quantity = abs(float(c[7]))
        self.spotCurrency = cpre[6].split('.')[0]
        self.subTotal = abs(float(cpre[7]))
        self.spotPrice = self.subTotal/abs(float(c[7])) # Estimated
        self.fees = abs(float(c[8])) + abs(float(cpre[8]))
        self.totalWFees = self.subTotal + self.fees
        self.desc = c[1]
      # If deposit not into Kraken EUR hold, count it as Buy
      elif c[3] == "deposit" and not "HOLD" in c[6]:
        self.opType = "Buy"
        self.crypto = c[6]
        if self.crypto[0] == 'X': self.crypto = c[6][1:]
        if self.crypto == "XBT" : self.crypto = "BTC"
        self.quantity = abs(float(c[7]))
        self.spotCurrency = Defaults.currency
        self.subTotal = None
        self.spotPrice = None
        self.cryptoFees = abs(float(c[8]))
        self.totalWFees = None
        self.desc = c[1]
        self.setInformationComplete(False)
      # If withdrawal from crypto account
      elif c[3] == "withdrawal":
        self.opType = "Send"
        self.crypto = c[6]
        if self.crypto[0] == 'X': self.crypto = c[6][1:]
        if self.crypto == "XBT" : self.crypto = "BTC"
        self.quantity = abs(float(c[7]))
        self.spotCurrency = Defaults.currency
        self.subTotal = None
        self.spotPrice = None
        self.cryptoFees = abs(float(c[8]))
        self.totalWFees = None
        self.desc = c[1]
        self.setInformationComplete(False)
      else:
        return False
    except Exception:
      self.setNothingValid()
      return False # If failed to parse properly line

    # If no error occured
    self.setEverythingValid()
    return True
