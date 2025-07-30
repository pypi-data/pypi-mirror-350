# Ссылка на каталог с файлами для загрузки
UPLOADS = 'uploads'

# Префикс идентификаторов записей сущностей специфический для продукта. Должен быть заполнен в продуктах в settings.py
# или в конфигурационном файле
RDM_EXPORT_ENTITY_ID_PREFIX = ''

# Количество записей моделей ЭШ обрабатываемых за одну итерацию сбора данных
RDM_COLLECT_CHUNK_SIZE = 500

# Количество записей моделей обрабатываемых за одну итерацию экспорта
RDM_EXPORT_CHUNK_SIZE = 500

# Количество не экспортированных записей моделей обрабатываемых за одну итерацию обновления поля modified
RDM_UPDATE_NON_EXPORTED_CHUNK_SIZE = 5_000

# Отображение пункта меню "Региональная витрина данных"
RDM_MENU_ITEM = True


# Загрузка данных в Региональную витрину данных (РВД)
# Адрес витрины (schema://host:port)
RDM_UPLOADER_CLIENT_URL = 'http://localhost:8090'

# Мнемоника Витрины
RDM_UPLOADER_CLIENT_DATAMART_NAME = 'test'

# Количество повторных попыток запроса
RDM_UPLOADER_CLIENT_REQUEST_RETRIES = 10

# Таймаут запроса, сек
RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT = 10

# Включить эмуляцию отправки запросов
RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION = True


# Настройка запуска периодической задачи выгрузки данных:
RDM_TRANSFER_TASK_MINUTE = '0'
RDM_TRANSFER_TASK_HOUR = '*/4'
RDM_TRANSFER_TASK_DAY_OF_WEEK = '*'
RDM_TRANSFER_TASK_LOCK_EXPIRE_SECONDS = 60 * 60 * 6

# Настройка запуска периодической задачи выгрузки данных - очередь быстрого уровня
RDM_FAST_TRANSFER_TASK_MINUTE = '*/5'
RDM_FAST_TRANSFER_TASK_HOUR = '*'
RDM_FAST_TRANSFER_TASK_DAY_OF_WEEK = '*'
RDM_FAST_TRANSFER_TASK_LOCK_EXPIRE_SECONDS = 60 * 30

# Настройка запуска периодической задачи выгрузки данных - очередь медленного уровня
RDM_LONG_TRANSFER_TASK_MINUTE = '0'
RDM_LONG_TRANSFER_TASK_HOUR = '*/6'
RDM_LONG_TRANSFER_TASK_DAY_OF_WEEK = '*'
RDM_LONG_TRANSFER_TASK_LOCK_EXPIRE_SECONDS = 60 * 60 * 6


# Настройка запуска периодической задачи статуса загрузки данных в витрину:
RDM_UPLOAD_STATUS_TASK_MINUTE = '*/30'
RDM_UPLOAD_STATUS_TASK_HOUR = '*'
RDM_UPLOAD_STATUS_TASK_DAY_OF_WEEK = '*'
RDM_UPLOAD_STATUS_TASK_LOCK_EXPIRE_SECONDS = 60 * 60 * 2

# Настройка очереди Redis для формирования файлов РВД
RDM_UPLOAD_QUEUE_MAX_SIZE = 500_000_000
# Таймаут для сохранения параметров в общем кеш
RDM_REDIS_CACHE_TIMEOUT_SECONDS = 60 * 60 * 2


# Настройка запуска периодической задачи отправки csv-файлов в витрину:
RDM_UPLOAD_DATA_TASK_MINUTE = '0'
RDM_UPLOAD_DATA_TASK_HOUR = '*/2'
RDM_UPLOAD_DATA_TASK_DAY_OF_WEEK = '*'
RDM_UPLOAD_DATA_TASK_LOCK_EXPIRE_SECONDS = 60 * 60 * 2
# Количество подэтапов для обработки в периодической задаче отправки данных
RDM_UPLOAD_DATA_TASK_EXPORT_STAGES = 500

RDM_RESPONSE_FILE_STATUS = 'success'
