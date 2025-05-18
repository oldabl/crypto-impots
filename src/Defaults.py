import logging

# Class holding default information
# shared throughout the application
class Defaults:
  CURRENCY = "EUR"
  COMPATIBLE_PLATFORMS = ["Coinbase"]
  PRETEXT_LENGTH = 37

logging.basicConfig(filename="info.log",
                    filemode="w",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(module)s:%(funcName)s: %(message)s')
