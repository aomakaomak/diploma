from django.db import models

class MainPage(models.Model):
    header_1 = models.CharField(max_length=300, verbose_name="Заголовок на главной")
    header_2 = models.CharField(max_length=300, verbose_name="Подзаголовок на главной")
    button_text_1 = models.CharField(max_length=30, verbose_name="Текст на кнопке 1")
    button_text_2 = models.CharField(max_length=30, verbose_name="Текст на кнопке 2")
    benefits = models.TextField(verbose_name="Почему выбирают нас")
    about_company = models.TextField(verbose_name="О компании")
    short_about_us_header = models.CharField(max_length=30, verbose_name="Кратко о нас")
    short_about_us_1 = models.TextField(verbose_name="О нас блок 1")
    short_about_us_2 = models.TextField(verbose_name="О нас блок 2")
    short_about_us_3 = models.TextField(verbose_name="О нас блок 3")
    short_about_us_4 = models.TextField(verbose_name="О нас блок 4")

    def __str__(self):
        return "Главная страница"

    class Meta:
        verbose_name = 'главная'
        verbose_name_plural = 'главные'
        ordering = ['header_1']


class Service(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название услуги")
    short_description = models.CharField(max_length=1000, verbose_name="Краткое описание")
    example = models.CharField(max_length=1000, verbose_name="Пример услуги")
    full_description = models.TextField(verbose_name="Полное описание")
    price = models.IntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'
        ordering = ['title']


class Doctor(models.Model):
    name = models.CharField(max_length=150, verbose_name="ФИО")
    specialization = models.CharField(max_length=150, verbose_name="Специализация")
    photo = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.name} -- {self.specialization}"

    class Meta:
        verbose_name = 'врач'
        verbose_name_plural = 'врачи'
        ordering = ['name']


from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Appointment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Пользователь",
    )

    service = models.ForeignKey(
        "services.Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Услуга",
    )

    doctor = models.ForeignKey(
        "services.Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Врач",
    )

    result = models.TextField(verbose_name="Результат", blank=True, null=True)

    def clean(self):
        super().clean()
        if (self.service is None and self.doctor is None) or (self.service is not None and self.doctor is not None):
            raise ValidationError("Запись должна быть либо на услугу, либо к врачу (только один вариант).")

    def __str__(self):
        if self.service_id:
            return f"{self.user} — {self.service}"
        if self.doctor_id:
            return f"{self.user} — {self.doctor}"
        return f"{self.user} — (не выбрано)"

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"

