import psycopg2

class Connection:

    def __init__(self, host, port, database_name, user_name, user_pwd):
        """Инициализируем переменные класса"""
        self.host = host
        self.port = port
        self.database_name = database_name
        self.user_name = user_name
        self.user_pwd = user_pwd
        
    def execute(self, query):
        """Выполнение SQL запроса с возвращением результата"""
        with psycopg2.connect(f'postgresql://{self.user_name}:{self.user_pwd}@{self.host}:{self.port}/{self.database_name}') as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)  
                result = cursor.fetchall()
    

        return result