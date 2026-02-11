#!/bin/bash

# Ma'lumotlar bazasini tayyorlash
python manage.py migrate --noinput

# Celery Beat-ni fonda ishga tushirish (yengil rejimda)
celery -A core beat -l info --detach

# Celery Worker-ni xotirani tejash rejimida ishga tushirish
# --concurrency=1 bu faqat bitta jarayon ochadi (xotira tejaydi)
celery -A core worker -l info --concurrency=1 --detach

# Gunicorn (Web server) ni ishga tushirish
# --workers 2 xotira uchun yetarli
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2