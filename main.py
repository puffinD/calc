from flask import Flask, request
import psycopg2

app = Flask(__name__)

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host="LocalHost",
    database="postgres",
    user="postgres",
    password="admin"
)
cursor = conn.cursor()

# Создание таблицы для логирования операций
cursor.execute("CREATE TABLE IF NOT EXISTS calculations (id SERIAL PRIMARY KEY, operation TEXT)")

@app.route('/')
def calculator():
    operation = request.args.get('operation', '')
    if operation:
        try:
            result = eval(operation)
            cursor.execute("INSERT INTO calculations (operation) VALUES (%s)", (operation,))
            conn.commit()
            return f"Результат: {result}"
        except Exception as e:
            return f"Ошибка: {str(e)}"
    else:
        return "Пожалуйста, введите операцию в формате 'число1 оператор число2'"

if __name__ == '__main__':
    app.run()