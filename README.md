# Blogicum

Blogicum - это учебный проект на Django, предназначенный для работы со статическими страницами и публикациями пользователей.

## О проекте

Проект включает два приложения:
1. **pages** - для работы со статическими страницами (О проекте, Правила).
2. **blog** - для работы с публикациями пользователей.

## Установка и настройка

### 1. Клонирование репозитория
git clone https://github.com/yourusername/blogicum.git
cd blogicum
## 2. Создание и активация виртуального окружения
python -m venv venv

source venv/Scripts/activate
## 3. Установка зависимостей
pip install -r requirements.txt
## 4. Применение миграций
python manage.py migrate
## Запуск сервера разработки
python manage.py runserver

### Автор
Автор проекта: [Maksim]
