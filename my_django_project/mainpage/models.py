from django.db import models

# Для SFU
class SfuLocation(models.Model):
    photo = models.ImageField(upload_to='sfu/photos/')  # фото места
    latitude = models.FloatField()  # широта
    longitude = models.FloatField()  # долгота

    def __str__(self):
        return f"Sfu Location at ({self.latitude}, {self.longitude})"

class SfuRecord(models.Model):
    name = models.CharField(max_length=50, unique=True)  # имя уникальное
    score = models.IntegerField()  # сумма очков

    class Meta:
        ordering = ['-score']  # сортировка по убыванию очков

    def __str__(self):
        return f"{self.name}: {self.score}"

# Для Kras
class KrasLocation(models.Model):
    photo = models.ImageField(upload_to='kras/photos/')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Kras Location at ({self.latitude}, {self.longitude})"

class KrasRecord(models.Model):
    name = models.CharField(max_length=50, unique=True)
    score = models.IntegerField()

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.name}: {self.score}"