import datetime, logging
from Defaults import Defaults
from StatementLine import StatementLine

class CoinbaseLine(StatementLine):

  listData = ['Timestamp',
              'Transaction Type',
              'Asset',
              'Quantity Transacted',
              'Price Currency',
              'Price at Transaction',
              'Subtotal',
              'Total (inclusive of fees and/or spread)',
              'Fees and/or Spread',
              'Notes']

  # To set the line type before calling parent
  def __init__(self, textStatementLine, previousStatementLine=None):
    self.lineType = "Coinbase"
    super().__init__(textStatementLine, previousStatementLine)

  # Role: try to extract if line matches Coinbase statement
  # 0: Timestamp  1: Transaction Type  2: Asset
  # 3: Quantity Transacted  4: Price Currency
  # 5: Price at Transaction  6: Subtotal
  # 7: Total (inclusive of fees and/or spread)
  # 8: Fees and/or Spread  9: Notes
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
      self.date = datetime.datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S %Z")
      self.opType, self.crypto = str(c[1]), str(c[2])
      self.quantity, self.spotCurrency = abs(float(c[3])), str(c[4])
      self.spotPrice, self.subTotal = abs(float(c[5])), abs(float(c[6]))
      self.totalWFees, self.fees = abs(float(c[7])), abs(float(c[8]))
    except Exception:
      self.setNothingValid()
      logging.debug("Couldn't extract information")
      return False # If failed to parse properly line

    # If no error occurred
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
                  'totalWFees': self.totalWFees,
                  'lineType': self.lineType
                })
    return "Invalid statement line"
