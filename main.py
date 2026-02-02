
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from models import SpimexTradingResult

async def fetch_file_names(session, url):
    # res = ['https://spimex.com/files/55576/', 'https://spimex.com/files/55086/'...]
    try:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            file_names = []
            for a_tag in soup.find_all('a', class_="accordeon-inner__item-title link xls"):
                href = a_tag.get('href')
                file_names.append(f"https://spimex.com{href}")
                file_names.append(f"{href}")
            return file_names
    except Exception as e:
        print(f"Ошибка при парсинге списка файлов: {e}")
        return []


async def download_file(session, base_url, file_name, db_session):
    # на вход base_url = https://spimex.com
    # file_name = '/files/55576/'
    try:
        async with session.get(base_url + file_name) as response:
            response.raise_for_status()
            content = await response.read()
            split_name_file = file_name.split('/')
            with open(f"{split_name_file[2]}.xml", 'wb') as f:
                f.write(content)
            print(f"Скачан {file_name}")
            excel_data_df = pd.read_excel(f"{split_name_file[2]}.xml")
            for data in excel_data_df.values:
                index = 0
                while index < len(data):
                    if data[index] == '-' or pd.isna(data[index]):
                        data[index] = 0
                    index += 1
                new_record = SpimexTradingResult(
                    year = data[0],
                    мonth_number = data[1],
                    Category = data[2],
                    count_contract_petroleum_products = data[3],
                    value_contract_petroleum_products = data[4],
                    count_contract_energy_carriers = data[5],
                    value_contract_energy_carriers = data[6],
                    count_contract_agricultural = data[7],
                    value_contract_agricultural = data[8],
                    count_contract_mineral_raw = data[9],
                    value_contract_mineral_raw = data[10],
                    count_contract_oil = data[11],
                    value_contract_oil = data[12],
                    count_contract_gas = data[13],
                    value_contract_gas = data[14],
                    count_contract_forest = data[15],
                    value_contract_forest = data[16],
                    count_contract_metals = data[17],
                    value_contract_metals = data[18],
                    count_contract_carbon = data[19],
                    value_contract_carbon = data[20],
                    count_contracts = data[21],
                    count_value_contracts = data[22]
                )
                db_session.add(new_record)
                await db_session.commit()
    except SQLAlchemyError as e:
        print(f"Ошибка записи в БД для {file_name}: {e}")
        await db_session.rollback()
    except:
        print(f"Ошибка скачивания {file_name}, статус {response.status}")

async def main(list_page_url, base_url):
    async with aiohttp.ClientSession() as session:
        file_names = await fetch_file_names(session, list_page_url)
        tasks = [download_file(session, base_url, file_name) for file_name in file_names]
        await asyncio.gather(*tasks)
