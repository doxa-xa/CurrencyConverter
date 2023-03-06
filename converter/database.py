from converter.currencies import Currency
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, Enum, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

engine = create_engine("sqlite:///currency_converter.db", echo=True)

Base = declarative_base()

class Rates(Base):
     __tablename__ = 'rates'

     currency = Column(Enum(Currency),primary_key=True)
     rate = Column(Float)
     base = Column(Enum(Currency))
     
     def __repr__(self):
        return f'<Rates(base={self.base},rate={self.rate})>'

class Transaction(Base):
     __tablename__ = 'transactions'

     transaction_id = Column(Integer, autoincrement=True, primary_key=True)
     from_curr = Column(Enum(Currency))
     amount = Column(Float(4))
     to_curr = Column(Enum(Currency))
     exchanged = Column(Float(4))
     commission = Column(Integer)
     total = Column(Float(4))
     transact_date = Column(DateTime(timezone=False))
    
     def __repr__(self):
        return f'''id:{self.transaction_id},from_curr:{self.from_curr.name},amount:{self.amount},to_curr:{self.to_curr.name},exchanged:{round(self.exchanged, 3)},commission:{round(self.commission, 3)},total:{round(self.total, 3)},transact_date:{date.today()}'''



Base.metadata.create_all(engine)
session = sessionmaker(engine)