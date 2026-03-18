# Проект: LLM-Proxy API
Сервис на FastAPI для защищенного взаимодействия с LLM (OpenRouter) с использованием JWT-авторизации, SQLite и архитектурного разделения слоев.

## Установка и запуск через uv
Установка зависимостей
`uv pip install -r <(uv pip compile pyproject.toml)`

Запуск приложения
`uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
Доступ к Swagger по ссылке: `http://127.0.0.1:8000/docs`

## Демонстрация работы
### Общий вид
![alt text](images/image.png)
### 1. Регистрация пользователя
Критерий: Email в формате student_surname@email.com, хеширование пароля.
Тест: Регистрируем пользователя с паролем  «password».
![alt text](images/image-1.png)
![alt text](images/image-2.png)

### 2. Логин и получение JWT
Критерий: Аутентификация по email/паролю, выдача JWT.
Тест: Вводим данные зарегистрированного пользователя и получаем токен.
![alt text](images/image-3.png)
![alt text](images/image-4.png)
### 3. Авторизация в Swagger
Критерий: Корректное использование кнопки Authorize.
Тест: Вставляем полученный токен в поле Bearer token и нажимаем “Authorize”, затем “Close”.
![alt text](images/image-5.png)
![alt text](images/image-6.png)
![alt text](images/image-7.png)

### 4. Запрос к LLM (POST /chat)
Критерий: Обработка запроса, вызов OpenRouter, сохранение в БД.
Тест: Отправляем запрос, используя токен.
![alt text](images/image-8.png)
![alt text](images/image-9.png)
![alt text](images/image-10.png)

### 5. Просмотр истории (GET /chat/history)
Критерий: Возврат истории, привязанной к текущему пользователю.
Тест: Проверяем, что запрос и ответ LLM сохранились.
![alt text](images/image-11.png)
![alt text](images/image-12.png)
![alt text](images/image-13.png)

### 6. Очистка истории (DELETE /chat/history)
Критерий: Корректное удаление записей из БД.
Тест: Очищаем историю.
![alt text](images/image-14.png)
![alt text](images/image-15.png)