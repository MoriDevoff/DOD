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
    path('play/start/<str:mode>/', views.start_game, name='start_game'),
    path('locations/', views.locations_dashboard, name='location_dashboard'),
    path('locations/add/', views.location_create, name='location_create'),
    path('locations/<str:location_type>/<int:pk>/edit/', views.location_edit, name='location_edit'),
    path('locations/<str:location_type>/<int:pk>/delete/', views.location_delete, name='location_delete'),
    path('admin-panel/locations/', views.locations_dashboard, name='admin_locations_page'),
]

# Обслуживание медиа-файлов (фото из ImageField) только в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)