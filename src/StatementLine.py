import datetime

class StatementLine:
  def __init__(self, statementLine):
    self.statementLine = statementLine
    self.date = None
    self.opType = None
    self.crypto = None
    self.quantity = None
    self.spotCurrency = None
    self.spotPrice = None
    self.subTotal = None
    self.totalWFees = None
    self.fees = None
    self.desc = None
    self.isStatementLineInvalid = False
    self.gatherAllInformation()

  def isStatementLineValid(self):
    return not self.isStatementLineInvalid

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

  def getTotalWFees(self):
    return self.totalWFees

  def getFees(self):
    return self.fees

  def getDesc(self):
    return self.desc

  def isBuyLine(self):
    return self.getOpType() == "Buy"

  def isSellLine(self):
    return self.getOpType() == "Sell"

  def gatherAllInformation(self):
    if not isinstance(self.statementLine, str) or not self.statementLine or self.statementLine == "":
      self.isStatementLineInvalid = True
      return
      
    c = self.statementLine.split(",")
    # Get all attributes
    try:
      self.date = datetime.datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S %Z")
    except Exception:
      self.isStatementLineInvalid = True
      return
    self.opType, self.crypto = c[1], c[2]
    self.quantity, self.spotCurrency = float(c[3]), c[4]
    self.spotPrice, self.subTotal = float(c[5]), float(c[6])
    self.totalWFees, self.fees = float(c[7]), float(c[8])
    self.desc = c[9].rstrip()
    
  def __str__(self):
    if self.isStatementLineValid():
      return str({
                  'date': self.date.strftime("%Y-%m-%d %H:%M:%S"),
                  'opType': self.opType,
                  'crypto': self.crypto,
                  'quantity': self.quantity,
                  'spotCurrency': self.spotCurrency,
                  'spotPrice': self.spotPrice,
                  'subTotal': self.subTotal,
                  'totalWFees': self.totalWFees,
                  'fees': self.fees,
                  'desc': self.desc
                })
    return "Invalid statement line"

  def __repr__(self):
    return "StatementLine("+self.statementLine+")"
