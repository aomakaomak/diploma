# Django Medical Center

Учебный проект на Django: сайт медицинского центра с услугами, врачами, формами обратной связи и личным кабинетом для записей на приём.

## Приложения проекта

- `services` — публичные страницы (главная, услуги, врачи, контакты) и записи на приём.
- `users` — регистрация/вход/выход и кастомная модель пользователя.

## Основной функционал

### Публичная часть (без авторизации)

- **Главная** `/home/` — выводит контент из модели `MainPage` и список услуг (`Service`). Также содержит форму обратной связи (письмо отправляется на email через SMTP).
- **Услуги**:
  - список `/services/`
  - детальная страница услуги `/service_detail/<pk>/`
  - создание услуги `/new/` (в текущей версии доступ не ограничен; обычно это делают только через админку)
- **О компании / Врачи** `/about/` — список врачей (`Doctor`).
- **Контакты** `/contacts/` — форма обратной связи (письмо отправляется на email через SMTP).
- **Пользователи**:
  - регистрация `/users/register/`
  - вход `/users/login/`
  - выход `/users/logout/`

### Личный кабинет (требуется вход)

- **Создать запись** `/new-appointment/` — запись либо на конкретную услугу, либо к конкретному врачу.
- **Мои записи** `/appointments/` — список записей текущего пользователя.

### Админка

- `/admin/` — управление пользователями, контентом главной страницы, услугами, врачами и записями.

## Модели

### `users.CustomUser`
Кастомная модель пользователя на базе `AbstractUser` (дополнительных полей нет). Используется как `AUTH_USER_MODEL`.

### `services.MainPage`
Контент главной страницы:
- `header_1`, `header_2` — заголовки
- `button_text_1`, `button_text_2` — подписи кнопок
- `benefits`, `about_company` — текстовые блоки
- `short_about_us_header`, `short_about_us_1..4` — блок «Кратко о нас»

> На главной берётся первый объект: `MainPage.objects.first()` — обычно в базе должна быть одна запись.

### `services.Service`
Услуга:
- `title` — название
- `short_description` — краткое описание
- `example` — пример услуги
- `full_description` — полное описание
- `price` — цена (целое число)
- `image` — изображение (опционально)

### `services.Doctor`
Врач:
- `name` — ФИО
- `specialization` — специализация
- `photo` — фотография (опционально)

### `services.Appointment`
Запись на приём:
- `user` — пользователь (кто создал запись)
- `owner` — пациент (в текущей реализации равен `request.user`)
- `service` — ссылка на услугу (опционально)
- `doctor` — ссылка на врача (опционально)
- `result` — результат/заключение (опционально)

**Валидация (важно):** запись должна быть **либо** на услугу, **либо** к врачу — строго один вариант.
- нельзя оставить одновременно пустыми `service` и `doctor`
- нельзя заполнить одновременно и `service`, и `doctor`

Эта логика реализована в `Appointment.clean()`.

## Что может делать пользователь

### Гость (не авторизован)
- Просматривать страницы: главная, услуги, врачи, контакты
- Смотреть детальную страницу услуги
- Регистрироваться и входить в аккаунт
- Отправлять сообщения через формы обратной связи (если настроен SMTP)

### Авторизованный пользователь
- Всё, что гость
- Создавать запись на приём
- Смотреть список **только своих** записей
- Выходить из аккаунта

### Администратор
- Управлять всеми моделями через админку
- Добавлять/редактировать услуги, врачей, контент главной страницы
- Просматривать/редактировать записи пользователей
- Управлять пользователями

## Переменные окружения (.env)

Проект читает переменные из окружения через `python-dotenv` (файл `.env` в корне проекта).

Обязательные для запуска с Postgres:

```env
SECRET_KEY=
DEBUG=True

NAME=medical
USER=postgres
PASSWORD=postgres
HOST=db
PORT=5432
```

Переменные для отправки писем (нужны для форм обратной связи и приветственного письма при регистрации):

```env
EMAIL_HOST_USER=example@yandex.ru
EMAIL_HOST_PASSWORD=your_smtp_password
DEFAULT_FROM_EMAIL=example@yandex.ru
```

Если SMTP-переменные не заданы или неверные, отправка письма завершится ошибкой (на страницах будет показано сообщение об ошибке).

## Запуск через Docker Compose

### 1) Убедись, что в `docker-compose.yml` проброшен порт

Для доступа из браузера нужен `ports`:

```yaml
ports:
  - "8000:8000"
```

### 2) Поднять проект

```bash
docker compose up --build -d
```

Открыть в браузере:
- `http://localhost:8000/home/`

Логи веб-контейнера:
```bash
docker compose logs -f web
```

Остановить:
```bash
docker compose down
```

## Статика в Docker (важно)

Ты запускаешь проект через **gunicorn**, а он сам статику не раздаёт. Для раздачи статики в контейнере используется **WhiteNoise** (он уже добавлен в `requirements.txt`).

Нужно включить middleware в `config/settings.py` — строка уже есть, но может быть закомментирована:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

После включения пересобери контейнеры:
```bash
docker compose down
docker compose up --build -d
```

Проверка, что статика отдаётся:
- `http://localhost:8000/static/admin/css/base.css`

## Запуск без Docker (локально)

Создай и активируй виртуальное окружение, установи зависимости:

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Применить миграции и запустить сервер:

```bash
python manage.py migrate
python manage.py runserver
```

## Тесты

Запуск тестов приложения `services`:

```bash
python manage.py test services
```

## Форматирование и линтинг

```bash
python -m isort services users config
python -m black services users config
python -m flake8
```
