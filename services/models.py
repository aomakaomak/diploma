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