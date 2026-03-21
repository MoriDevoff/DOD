from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('play/', views.play, name='play'),
    path('play/sfu/', views.sfu_mode, name='sfu_mode'),
    path('play/kras/', views.kras_mode, name='kras_mode'),
    path('play/records/', views.records, name='records'),
    path('play/reset/<str:mode>/', views.reset_game, name='reset_game'),
]

# Обслуживание медиа-файлов (фото из ImageField) только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)