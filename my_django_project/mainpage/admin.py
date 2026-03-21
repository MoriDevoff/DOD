from django.contrib import admin
from .models import SfuLocation, SfuRecord, KrasLocation, KrasRecord

# Регистрация моделей для SFU
@admin.register(SfuLocation)
class SfuLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'photo')  # что показывать в списке
    list_filter = ('latitude', 'longitude')
    search_fields = ('latitude', 'longitude')

@admin.register(SfuRecord)
class SfuRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')
    search_fields = ('name',)
    ordering = ('-score',)

# Регистрация моделей для Kras
@admin.register(KrasLocation)
class KrasLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'photo')
    list_filter = ('latitude', 'longitude')
    search_fields = ('latitude', 'longitude')

@admin.register(KrasRecord)
class KrasRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')
    search_fields = ('name',)
    ordering = ('-score',)