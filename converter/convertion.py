from converter.connect import Connect
from converter.currencies import Currency
from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker
from converter.database import Rates, Transaction
from datetime import date
# from config import db_user,db_pass,db_server

# db connection 
# engine = create_engine(f'mysql+mysql://{db_user}:{db_pass}@{db_server}/currency_converter')

engine = create_engine("sqlite:///currency_converter.db", echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

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
            with Session.begin() as session:
                 for k,v in self._rates.items():
                      session.add(Rates(currency=k,rate=v,base=self._base))
                 
                
        else:
            print('Cannot retrieve rates from API')
            return None
        

    def convert(self,amount,currency):
            curr = session.query(Rates).filter_by(currency=currency.name).first()
            return round(curr.rate*amount, 4)
    
    def exchange(self,amount,currency,commission_percent):
         convert = self.convert(amount,currency)
         commission = commission_percent/100
         commisioned = convert*commission
         exchanged = convert - commisioned

         with Session.begin() as session:
              session.add(
                   Transaction(
                    from_curr=self._base,
                    amount=amount,
                    to_curr=currency.name,
                    exchanged=convert,
                    commission=commission_percent,
                    total=exchanged,
                    transact_date=date.today())
                    )
            
         return {
              'converted':round(convert, 3),
              'commision':round(commisioned, 3),
              'received':round(exchanged, 3)
         }
    def get_db_rates(self):
        with Session.begin() as session:
            rates = session.query(Rates.currency,Rates.rate,).all()
            print(rates)

    def get_transactions(self):
         query = session.query(Transaction).all()
         return session.execute(query)
    
    def delete_transaction_table(self):
         session.delete(Transaction)

    def delete_rates_table(self):
         session.delete(Rates)