# 📝 Flask Task Manager

Это веб-приложение на Flask с поддержкой регистрации, входа в систему и управления задачами. Все данные сохраняются в PostgreSQL.

---

## 🚀 Быстрый старт

### 📦 Установка зависимостей (для всех ОС)

Установи Python-библиотеки:

```bash
pip install flask psycopg2-binary
```

### 🪟 Установка и настройка PostgreSQL на Windows

1. **📥 Скачивание и установка PostgreSQL**

   Перейди на сайт: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)

   Скачай и установи PostgreSQL, запомни пароль от пользователя `postgres`, он понадобится позже.

2. **▶️ Запуск pgAdmin**

   После установки найди pgAdmin в меню Пуск и запусти.

3. **🛠 Создание базы данных**

   - Открой pgAdmin.
   - Подключись к серверу (используй пароль, указанный при установке).
   - Кликни правой кнопкой по `Databases` > `Create` > `Database`.
   - Назови базу данных `workdb`.

4. **⚙️ Проверка подключения в коде**

   В `connector.py` должны быть такие параметры:

   ```python
   self.conn = psycopg2.connect(
       dbname="workdb",
       user="postgres",
       password="ТВОЙ_ПАРОЛЬ",
       host="127.0.0.1",
       port="5432"
   )
   ```

### 🐧 Установка и настройка PostgreSQL на Linux

1. **🔍 Проверка состояния службы PostgreSQL**

   ```bash
   sudo systemctl status postgresql
   ```

   Показывает, работает ли PostgreSQL.

2. **▶️ Запуск службы PostgreSQL**

   ```bash
   sudo systemctl start postgresql
   ```

3. **📥 Установка PostgreSQL**

   ```bash
   sudo dnf install postgresql-server postgresql-contrib
   ```

4. **🛠 Инициализация базы данных**

   ```bash
   sudo postgresql-setup --initdb
   ```

5. **📂 Создание базы данных**

   ```bash
   psql -U postgres
   CREATE DATABASE workdb;
   \q
   ```

6. **⚙️ Подключение к БД**

   Приложение подключается автоматически при запуске Flask — таблицы создаются автоматически, вручную ничего писать не нужно.

### ▶️ Запуск приложения

```bash
python inside.py
```

Приложение откроется по адресу: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 💡 Возможности

- 🔐 Регистрация и вход
- 📋 Добавление задач с дедлайнами и описанием
- ⏱ Подсчёт дней до дедлайна
- ✅ Выполненные задачи
- 🌙 Ночной режим