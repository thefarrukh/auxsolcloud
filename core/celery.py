import os
from celery import Celery

# ✅ BUGFIX: Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# ✅ BUGFIX: Celery app yaratish
app = Celery('core')

# ✅ BUGFIX: Django settings'dagi CELERY_ bilan boshlanadigan barcha konfiguratsiyalarni o'qish
app.config_from_object('django.conf:settings', namespace='CELERY')

# ✅ BUGFIX: Barcha app'lardagi tasks.py fayllarini avtomatik qidirish
app.autodiscover_tasks()

# ✅ BUGFIX: Debug task
@app.task(bind=True)
def debug_task(self):
    """Debug task - Celery ishlayotganini tekshirish uchun"""
    print(f'Request: {self.request!r}')
    return 'Celery is working!'