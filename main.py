import aiohttp
import asyncio
from bs4 import BeautifulSoup
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from models import SpimexTradingResult, AsyncSessionLocal


async def fetch_file_names(session, url):
    # res = ['https://spimex.com/files/55576/', 'https://spimex.com/files/55086/'...]
    try:
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            file_names = []
            for a_tag in soup.find_all('a', class_="accordeon-inner__item-title link xls"):
                href = a_tag.get('href')
                file_names.append(href)
            return file_names
    except Exception as e:
        print(f"Ошибка при парсинге списка файлов: {e}")
        return []


async def download_file(session, base_url, file_name, event):
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
    except asyncio.TimeoutError:
        print(f"Ошибка скачивания {file_name}")
    finally:
        event.set()


async def add_to_db(file_name, db_session, event):
    await event.wait()
    try:
        async with db_session:
            split_name_file = file_name.split('/')
            excel_data_df = pd.read_excel(split_name_file[1])
            for data in excel_data_df.values:
                        new_record = SpimexTradingResult(
                            year = data[0],
                            month_number = data[1],
                            category = data[2],
                            count_contracts = data[-2],
                            count_value_contracts = data[-1]
                        )
                        db_session.add(new_record)
        await db_session.commit()
    except SQLAlchemyError as e:
        print(f"Ошибка записи в БД для {file_name}: {e}")
        await db_session.rollback()


async def main(list_page_url, base_url):
    event = asyncio.Event()
    async with aiohttp.ClientSession() as session, AsyncSessionLocal() as db_session:
        file_names = await fetch_file_names(session, list_page_url)
        tasks_download_file = [download_file(session, base_url, file_name, event) for file_name in file_names]
        tasks_add_to_db = [add_to_db(file_name, db_session, event) for file_name in file_names]
        await asyncio.gather(*tasks_download_file, *tasks_add_to_db)


    
if __name__ == '__main__':
    list_page_url = 'https://spimex.com/markets/oil_products/trades/results/'
    base_url = 'https://spimex.com'
    asyncio.run(main(list_page_url, base_url))
