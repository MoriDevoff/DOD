from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('authors/', views.authors, name='authors'),
    path('play/', views.play, name='play'),
    path('play/how-to-play/', views.how_to_play, name='how_to_play'),
    path('play/sfu/', views.sfu_mode, name='sfu_mode'),
    path('play/kras/', views.kras_mode, name='kras_mode'),
    path('play/records/', views.records, name='records'),
    path('play/reset/<str:mode>/', views.reset_game, name='reset_game'),
    path('admin-panel/locations/', views.admin_locations_page, name='admin_locations_page'),
    path('admin-panel/locations/data/', views.admin_locations_data, name='admin_locations_data'),
    path('admin-panel/locations/update/', views.admin_location_update, name='admin_location_update'),
    path('admin-panel/locations/create/', views.admin_location_create, name='admin_location_create'),
]

# Обслуживание медиа-файлов (фото из ImageField) только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)