# Music_plog (Musical)
Музыкальная платформа Musical: Cервис для прослушивания и загрузки музыки с возможностью создания плейлистов.
Также присутсвует возможность выставления оценок с отзывами на песни других исполнителей и комментирование отзывов

# Стек
```
Python 3.9 as programming language
```
```
Django 3.2 as web framework
```
```
Django REST framework 3.12 as toolkit for building Web APIs
```
```
SQLite3 as database
```
```
GitHub as repo and workflows manager
```
# Установка проекта

## Склонировать репозиторий и перейти в него в командной строке
```
 git clone https://github.com/N0len-sasha/Music_plog.git
```
```
 cd Music_plog
```
## Создать и активировать виртуальное окружение
```
python -m venv venv
```
```
source venv/Scripts/activate
```
## Установить зависимости
```
pip install -r requirements.txt
```
## Перейти в папку проекта и создать БД
```
cd music_blog_api
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
## Запустить проект
```
python manage.py runserver
```
