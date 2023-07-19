import psycopg2  
import os  
import dotenv  
from crontab import CronTab  
  
# Переменные  
dotenv.load_dotenv()
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DB = os.getenv('DB')
USER_DB = os.getenv('USER_DB')
  
# Открываем соединение с БД  
connection = psycopg2.connect(os.getenv('CONNECT_DB'))  
cursor = connection.cursor()  
  
def GetCron():  
    """Получаем информацию о кроне"""  
    cursor.execute(os.getenv('SELECT_CRON'))  
    return cursor.fetchall()  
  
def CreateCron(crons):  
    """Создаём cron задания на сервере"""  
    # Создание объекта cron  
    cron = CronTab(user=True)
  
    # Добавление новых задач на основе списка кронов из базы данных  
    for cron_id, cron_str, func_name in crons:
        # Создание команды cron для выполнения функции PostgreSQL  
        command = f"psql -h '{HOST}' -p '{PORT}' -d '{DB}' -U '{USER_DB}' -c 'SELECT {func_name}()'"
        cron_comment = f'database_cron_{cron_id}' 
 
        '''
        # Обновление задачи 
        for job in cron: 
            if job.comment == cron_comment: 
                job.setall(cron_str) 
                job.set_command(command)
        
         
        # Если крон не найден, то добавляем его  
        if not any(job.comment == cron_comment for job in cron):
        '''
        # Создание новой задачи cron с указанным расписанием и командой  
        job = cron.new(command=command, comment=cron_comment)  
        job.setall(cron_str)

        # Включение задачи  
        job.enable() 
  
    # Сохранение изменений в cron  
    cron.write()  
  
if __name__ == '__main__':  
    CreateCron(GetCron())  
  
    # Закрываем соединение с БД  
    cursor.close()  
    connection.close()