from converter.currencies import Currency
from converter.convertion import Convert

usd = Convert(Currency.USD)

usd.get_rates()

print(usd.convert(3000,Currency.BGN))
print(usd.exchange(3000,Currency.BGN,1))








