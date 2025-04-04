Проверка состояния службы PostgreSQL

Чтобы проверить работу службы PostgreSQL, выполните команду:

sudo systemctl status postgresql

ВАЖНО! Эта команда покажет текущее состояние службы: работает ли она, есть ли ошибки, и другую полезную информацию.
Запуск службы PostgreSQL

Если служба не запущена, выполните:

sudo systemctl start postgresql

Установка PostgreSQL

Для установки PostgreSQL и дополнительных компонентов выполните:

sudo dnf install postgresql-server postgresql-contrib

Инициализация базы данных

После установки необходимо инициализировать базу данных:

sudo postgresql-setup --initdb

Эта команда создаст необходимые структуры данных для работы PostgreSQL.
