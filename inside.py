from datetime import datetime


from flask import Flask, render_template, request, redirect, url_for, make_response, flash
import os
from connector import DBConnector

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
db = DBConnector()  # Инициализация подключения

tasks = []

@app.route('/', methods=['GET', 'POST'])
def start():
    error = None
    message = None
    show_login = False

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        action = request.form.get('action')

        if action == 'login':
            if db.check_user(username, password):
                response = make_response(redirect(url_for('task_manager')))
                response.set_cookie('username', username)
                return response
            else:
                error = "Неверный логин или пароль!"
                show_login = True

        elif action == 'create_account':
            if db.create_user(username, password):
                message = f"Аккаунт {username} успешно создан!"
                show_login = True
            else:
                error = "Это имя пользователя уже занято!"
                show_login = False

    elif request.args.get('action') == 'show_create':
        show_login = False

    theme = request.cookies.get('theme', 'day')
    return render_template(
        'helloWeb.html',
        show_login=show_login,
        error=error,
        message=message,
        theme=theme
    )

@app.route('/rol', methods=['GET', 'POST'])
def task_manager():
    global tasks
    night_mode = request.args.get('night_mode') == 'true' or request.cookies.get('night_mode') == 'true'

    # Инициализация tasks при первом обращении
    if 'tasks' not in globals():
        tasks = []

    if request.method == 'POST':
        task_text = request.form.get('text')
        deadline_str = request.form.get('deadline')
        description = request.form.get('description', '')

        if task_text and deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
                diff_days = (deadline - datetime.now()).days

                tasks.append({
                    'text': task_text,
                    'deadline': deadline_str,
                    'description': description,
                    'days_left': diff_days,
                    'completed': False,
                    'height': 180
                })
            except ValueError:
                pass

        resp = redirect(url_for('task_manager', night_mode=night_mode))
        resp.set_cookie('night_mode', str(night_mode))
        return resp

    # Обработка действий
    action = request.args.get('action')
    task_id = request.args.get('id', type=int)

    if action and task_id is not None and 0 <= task_id < len(tasks):
        if action == 'toggle':
            tasks[task_id]['completed'] = not tasks[task_id]['completed']
        elif action == 'resize':
            new_height = request.args.get('height', type=int)
            if new_height:
                tasks[task_id]['height'] = new_height
        elif action == 'edit':
            new_description = request.args.get('description')
            if new_description:
                tasks[task_id]['description'] = new_description
        elif action == 'delete':
            if request.args.get('confirm') == 'true':
                tasks.pop(task_id)

        resp = redirect(url_for('task_manager', night_mode=night_mode))
        resp.set_cookie('night_mode', str(night_mode))
        return resp

    # Пагинация
    current_page = request.args.get('page', 1, type=int)
    tasks_per_page = 3
    total_pages = max(1, (len(tasks) + tasks_per_page - 1) // tasks_per_page)
    current_page = max(1, min(current_page, total_pages))

    # Создаем response объект перед установкой куки
    response = make_response(render_template(
        'task_manager.html',
        tasks=tasks[(current_page - 1) * tasks_per_page: current_page * tasks_per_page],
        current_page=current_page,
        total_pages=total_pages,
        night_mode=night_mode
    ))
    response.set_cookie('night_mode', str(night_mode))
    return response


if __name__ == '__main__':
    app.run(debug=True)