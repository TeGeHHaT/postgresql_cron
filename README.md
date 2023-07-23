Создать файл .env в котором указать:

```env
CONNECT_DB = 'postgresql://login:password@host:port/db_name'
HOST = ''
PORT = ''
DB = ''
USER_NAME = ''
USER_PASSWORD = ''
SELECT_CRON = 'select c.cron, c.func_name from table c'
```