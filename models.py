from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, Float, String


Base = declarative_base()

class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Float) # Год
    мonth_number = Column(Float) # Номер месяца
    Category = Column(String)
    count_contract_petroleum_products = Column(Float) # Количество заключенных договоров в Секции "Нефтепродукты", шт.
    value_contract_petroleum_products = Column(Float) # Объем заключенных договоров в Секции "Нефтепродукты", руб.
    count_contract_energy_carriers = Column(Float)  # Количество заключенных договоров в Секции "Энергоносители", шт.
    value_contract_energy_carriers = Column(Float)  # Объем заключенных договоров в Секции "Энергоносители", руб.
    count_contract_agricultural = Column(Float)  # Количество заключенных договоров в Секции "Сельскохозяйственная продукция и биоресурсы", шт.
    value_contract_agricultural = Column(Float)  # Объем заключенных договоров в Секции "Сельскохозяйственная продукция и биоресурсы", руб.
    count_contract_mineral_raw = Column(Float)  # Количество заключенных договоров в Секции "Минеральное сырье и химическая продукция", шт.
    value_contract_mineral_raw = Column(Float) # Объем заключенных договоров в Секции "Минеральное сырье и химическая продукция", руб.
    count_contract_oil = Column(Float) # Количество заключенных договоров в Секции "Нефть", шт.
    value_contract_oil = Column(Float)  # Объем заключенных договоров в Секции "Нефть", руб.
    count_contract_gas = Column(Float) # Количество заключенных договоров в Секции "Газ природный", шт.
    value_contract_gas = Column(Float) # Объем заключенных договоров в Секции "Газ природный", руб.
    count_contract_forest = Column(Float) # Количество заключенных договоров в Секции "Лес и стройматериалы", шт.
    value_contract_forest = Column(Float) # Объем заключенных договоров в Секции "Лес и стройматериалы", руб.
    count_contract_metals = Column(Float) # Количество заключенных договоров в Секции "Металлы и сплавы", шт.
    value_contract_metals = Column(Float) # Объем заключенных договоров в Секции "Металлы и сплавы", руб.
    count_contract_carbon = Column(Float)  # Количество заключенных договоров в Секции "Углеродный рынок", шт.
    value_contract_carbon = Column(Float)  # Объем заключенных договоров в Секции "Углеродный рынок", руб.
    count_contracts = Column(Float) # 'Суммарное количество заключенных договоров во всех секциях, шт.'
    count_value_contracts = Column(Float) # 'Суммарный объем заключенных договоров во всех секциях, руб.'



DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
