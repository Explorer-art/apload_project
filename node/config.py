MASTER_SERVER = "127.0.0.1"
STATUS_PASSWORD = "rw0ZscjhLwhN661"

LINK_LENGTH = 7 # Длина ссылки
MAX_FILE_SIZE = 1073741824 # Максимальный размер файла
EXPIRE_CLEAR = 3600 # Период очистки
MAX_DISK_SPACE = 10737418240 # Лимит загрузки файлов
MAX_UPLOADS = 100 # Лимит количества загруженных файлов
ADDED_FREE_BYTES = 10485760

AVAILABLES_FILE_EXPIRE = [3600, 86400, 604800, 2419200, 31536000]

FILE_EXPIRE = [
	{
		"title": "1 час",
		"expire": 3600
	},
	{
		"title": "1 день",
		"expire": 86400
	},
	{
		"title": "1 неделя",
		"expire": 604800
	},
	{
		"title": "1 месяц",
		"expire": 2419200
	},
	{
		"title": "1 год",
		"expire": 31536000
	}
]