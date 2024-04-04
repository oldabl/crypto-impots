import ccxt,datetime,sys,currency_converter

exchange = ccxt.binance()
statementFile = open('statements/statementAllTime.csv', 'r')
lines = statementFile.readlines()
cryptosOwned = {}
taxableGainsPerYear = {}

def portfolioValue(date):
  timestamp = int(date.timestamp() * 1000)
  portfolioValue = 0
  for (cryptoName,amount) in cryptosOwned.items():
    value = 0
    try:
      response = exchange.fetch_ohlcv(cryptoName+'/USDT', '1m', timestamp, 1)
      value = (response[0][1] + response[0][4])/2
      c = currency_converter.CurrencyConverter()
      value = c.convert(value, 'USD', 'EUR', date=date)
    except Exception:
      #print("ERROR FOR "+ cryptoName)
      pass
    portfolioValue = portfolioValue + float(value)*amount
  return portfolioValue

def printableAmount(amount):
  return str(round(amount, 2))

amountInvested = 0

for line in reversed(lines):
  c = line.split(",")

  # Get all attributes
  try:
    date = datetime.datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S %Z")
  except Exception:
    continue
  opType,crypto,quantity,spotCurrency = c[1],c[2],float(c[3]),c[4]
  spotPrice,subTotal,totalWFees,fees,desc = float(c[5]),float(c[6]),float(c[7]),float(c[8]),c[9]

  # Compute all cryptos owned
  if opType == "Buy":
    if crypto not in cryptosOwned.keys():
      cryptosOwned[crypto] = 0
    cryptosOwned[crypto] = cryptosOwned[crypto] + quantity

  # Compute amount invested
  if opType == "Buy":
    amountInvested = amountInvested + subTotal

  # Compute information for taxes when selling
  if opType == "Sell":
    if crypto == spotCurrency:
      continue
    print("Vente de " + crypto + " en date du", date, ": ")
    valuePortfolio = portfolioValue(date)
    percentageSold = subTotal/valuePortfolio
    percentagePlusValue = valuePortfolio/amountInvested
    taxableGains = (valuePortfolio - amountInvested) * percentageSold
    print("Montant investi à cette date : " + printableAmount(amountInvested) + " EUR")
    print("Valeur du portefeuille à cette date : " + printableAmount(valuePortfolio) + " EUR")
    print("Valeur en euros vendue : " + printableAmount(subTotal) + " EUR")
    print("Plus value à déclarer : " + printableAmount(taxableGains) + " EUR")
    print()
    if date.year not in taxableGainsPerYear.keys():
      taxableGainsPerYear[date.year] = 0
    taxableGainsPerYear[date.year] = taxableGainsPerYear[date.year] + taxableGains


    # Compute information to withdraw sold amount part in invested amount
    toWithDrawFromAmountInvested = subTotal/percentagePlusValue
    amountInvested = amountInvested - toWithDrawFromAmountInvested
    
    # Remove crypto sold in owned crypto
    cryptosOwned[crypto] = cryptosOwned[crypto] - quantity

print("Résumé par année : ")
for year, taxableGain in taxableGainsPerYear.items():
  print("- " + str(year) + " : plus-value imposable " + printableAmount(taxableGain) + " EUR")
