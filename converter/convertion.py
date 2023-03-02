from converter.connect import Connect
from converter.currencies import Currency

class Convert:
    """
    Converts one currency to another
    """
    #constructor
    _base = 'USD'
    _rates = {}
    def __init__(self,base):
        self._base = base.name

    def get_rates(self):
        self._rates = Connect.get_rates(self._base)
        if self._rates:
            print(f'Retrieved {self._base} rates')
            print(self._rates)
        else:
             print('Cannot retrieve rates from API')
        

    def convert(self,amount,currency):
            return round(self._rates[currency.name]*amount, 4)
    
    def exchange(self,amount,currency,commision_percent):
         convert = self.convert(amount,currency)
         commision = commision_percent/100
         commisioned = convert*commision
         exchanged = convert - commisioned
         return {
              'converted':round(convert, 3),
              'commision':round(commisioned, 3),
              'received':round(exchanged, 3)
         }