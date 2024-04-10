import logging

# Class holding default information
# shared throughout the application
class Defaults:
  CURRENCY = "EUR"
  COMPATIBLE_PLATFORMS = ["Coinbase", "Kraken"]

logging.basicConfig(filename="debug.log",
                    filemode="w",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(module)s:%(funcName)s: %(message)s')
