#!/bin/bash

# 1. Ma'lumotlar bazasi jadvallarini yaratish
echo "Migrating database..."
python manage.py migrate --noinput

# 2. Celery Worker-ni fonda (background) ishga tushirish
echo "Starting Celery Worker..."
celery -A core worker -l info &

# 3. Celery Beat-ni ham fonda ishga tushirish
echo "Starting Celery Beat..."
celery -A core beat -l info &

# 4. Djangoni asosiy jarayon sifatida ishga tushirish
# Renderda port odatda 10000 bo'ladi, lekin biz 8001 ni ham ishlatsak bo'ladi
echo "Starting Django Server..."
python manage.py runserver 0.0.0.0:8001