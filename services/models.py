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


class Service(models.Model):
    pass