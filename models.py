from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, Float, String


Base = declarative_base()

class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Float) # Год
    month_number = Column(Float) # Номер месяца
    category = Column(String) # категория
    count_contracts = Column(Float) # 'Суммарное количество заключенных договоров во всех секциях, шт.'
    count_value_contracts = Column(Float) # 'Суммарный объем заключенных договоров во всех секциях, руб.'


DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
