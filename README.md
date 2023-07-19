Создать файл .env в котором указать:

```env
CONNECT_DB = 'postgresql://login:password@host:port/db_name'
HOST = ''
PORT = ''
DB = ''
USER_DB = ''
SELECT_CRON = 'select c.id as cron_id, c.cron, c.func_name from table c'
```