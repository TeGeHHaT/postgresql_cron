import os  
import dotenv
from connection import Connection
import time
from croniter import croniter
from concurrent.futures import ProcessPoolExecutor
import asyncio
  
# Переменные  
dotenv.load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB = os.getenv('DB')
USER_NAME = os.getenv('USER_NAME')
USER_PASSWORD = os.getenv('USER_PASSWORD')
  
# Создаём экземпляр класса Connection
connection = Connection(host=HOST, port=PORT, database_name=DB, user_name=USER_NAME, user_pwd=USER_PASSWORD)
  
def get_cron():  
    """Получаем информацию о кроне"""  
    return connection.execute(os.getenv('SELECT_CRON'))
  
def execute_cron(func_name):
    """Выполнение отдельного задания по расписанию"""

    # Создание команды cron для выполнения функции PostgreSQL
    command = f"psql -h '{HOST}' -p '{PORT}' -d '{DB}' -U '{USER_NAME}' -w -c 'SELECT {func_name}()'"
    os.system(command)

async def run_cron_async(cron_str, func_name):
    """Асинхронное выполнение задания по расписанию"""
    cron = croniter(cron_str, time.time())  # Создание объекта для работы с расписанием cron и текущего времени

    while True:
        # Запускаем задание в отдельном процессе
        with ProcessPoolExecutor() as executor:
            executor.submit(execute_cron, func_name)

        # Вычисляем время следующего запуска задания после его запуска
        next_run_timestamp = cron.get_next(float)

        # Вычисляем время ожидания до следующего запуска
        time_to_wait = next_run_timestamp - time.time()

        # Если время ожидания отрицательное, это значит, что следующий запуск уже прошел, пропускаем его и ловим следующий
        if time_to_wait <= 0:
            continue

        # Ждем до следующего запуска
        await asyncio.sleep(time_to_wait)

def run_cron(crons):
    """Запуск заданий по расписанию (cron) в асинхронном режиме"""

    loop = asyncio.get_event_loop()
    tasks = [run_cron_async(cron_str, func_name) for cron_str, func_name in crons]
    loop.run_until_complete(asyncio.gather(*tasks))
  
if __name__ == '__main__':  
    run_cron(get_cron())