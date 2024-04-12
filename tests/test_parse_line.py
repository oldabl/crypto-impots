# test_parse_line.py

import sys, datetime

# FOR LOCAL RUN
if __name__ == '__main__':
  sys.path.append('src')
# FOR LOCAL RUN


from CoinbaseLine import CoinbaseLine

def test_parse_coinbase_line():
  timestamp = "2024-03-26 23:12:03 UTC"
  trans_type = "Sell"
  asset = "FIDA"
  quantity_trans = "46.165532"
  spot_price_curr = "EUR"
  spot_price_at_trans = "0.48"
  subtotal = "22.38"
  total_with_fees = "20.89"
  fees = "-1.49"
  notes = "Sold 46.165532 FIDA for 20.89 EUR"
  coinbase_line = ",".join([timestamp, trans_type, asset, quantity_trans, spot_price_curr, spot_price_at_trans, subtotal, total_with_fees, fees, notes])

  stl = CoinbaseLine(coinbase_line)

  assert stl.getDate() == datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S %Z")
  assert stl.getOpType() == trans_type
  assert stl.getCrypto() == asset
  assert stl.getQuantity() == abs(float(quantity_trans))
  assert stl.getSpotCurrency() == spot_price_curr
  assert stl.getSpotPrice() == abs(float(spot_price_at_trans))
  assert stl.getSubTotal() == abs(float(subtotal))
  assert stl.getFees() == abs(float(fees))
  assert stl.getCryptoFees() == 0.0


# FOR LOCAL RUN
if __name__ == '__main__':
  test_parse_coinbase_line()
# FOR LOCAL RUN
