from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from services.models import MainPage, Service, Doctor, Appointment

from django.urls import reverse


class ModelCreationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username="u1", password="pass12345")

        cls.service = Service.objects.create(
            title="УЗИ",
            short_description="Короткое описание",
            example="Пример услуги",
            full_description="Полное описание услуги",
            price=1500,
        )

        cls.doctor = Doctor.objects.create(
            name="Иванов Иван Иванович",
            specialization="Терапевт",
        )

    def test_main_page_can_be_created(self):
        obj = MainPage.objects.create(
            header_1="Заголовок 1",
            header_2="Заголовок 2",
            button_text_1="Кнопка 1",
            button_text_2="Кнопка 2",
            benefits="Преимущества",
            about_company="О компании",
            short_about_us_header="Кратко",
            short_about_us_1="Блок 1",
            short_about_us_2="Блок 2",
            short_about_us_3="Блок 3",
            short_about_us_4="Блок 4",
        )
        self.assertIsNotNone(obj.pk)
        self.assertEqual(str(obj), "Главная страница")

    def test_service_can_be_created(self):
        s = Service.objects.create(
            title="Анализы",
            short_description="Сдадим анализы быстро",
            example="Общий анализ крови",
            full_description="Подробное описание",
            price=999,
        )
        self.assertIsNotNone(s.pk)
        self.assertEqual(str(s), "Анализы")

    def test_doctor_can_be_created(self):
        d = Doctor.objects.create(
            name="Петров Пётр Петрович",
            specialization="Хирург",
        )
        self.assertIsNotNone(d.pk)
        self.assertIn("Петров", str(d))
        self.assertIn("Хирург", str(d))

    def test_appointment_can_be_created_with_service_only(self):
        a = Appointment(
            user=self.user,
            owner=self.user,
            service=self.service,
            doctor=None,
            result=None,
        )
        a.full_clean()  # запускает clean() + валидации полей
        a.save()
        self.assertIsNotNone(a.pk)
        self.assertIn("—", str(a))

    def test_appointment_can_be_created_with_doctor_only(self):
        a = Appointment(
            user=self.user,
            owner=self.user,
            service=None,
            doctor=self.doctor,
            result=None,
        )
        a.full_clean()
        a.save()
        self.assertIsNotNone(a.pk)
        self.assertIn("—", str(a))

    def test_appointment_rejects_both_service_and_doctor(self):
        a = Appointment(
            user=self.user,
            owner=self.user,
            service=self.service,
            doctor=self.doctor,
        )
        with self.assertRaises(ValidationError):
            a.full_clean()

    def test_appointment_rejects_neither_service_nor_doctor(self):
        a = Appointment(
            user=self.user,
            owner=self.user,
            service=None,
            doctor=None,
        )
        with self.assertRaises(ValidationError):
            a.full_clean()






class PagesReturn200Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username="u2", password="pass12345")

        # Чтобы шаблоны главной/списков не падали на пустых данных
        cls.main_page = MainPage.objects.create(
            header_1="Заголовок 1",
            header_2="Заголовок 2",
            button_text_1="Кнопка 1",
            button_text_2="Кнопка 2",
            benefits="Преимущества",
            about_company="О компании",
            short_about_us_header="Кратко",
            short_about_us_1="Блок 1",
            short_about_us_2="Блок 2",
            short_about_us_3="Блок 3",
            short_about_us_4="Блок 4",
        )

        cls.service = Service.objects.create(
            title="Консультация",
            short_description="Коротко",
            example="Пример",
            full_description="Полное описание",
            price=1000,
        )

        cls.doctor = Doctor.objects.create(
            name="Сидоров Сидор Сидорович",
            specialization="Кардиолог",
        )

    def test_public_pages_return_200(self):
        urls = [
            reverse("services:home"),
            reverse("services:service_create"),
            reverse("services:service_detail", kwargs={"pk": self.service.pk}),
            reverse("services:about"),
            reverse("services:services_list"),
            reverse("services:contacts"),
        ]

        for url in urls:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 200)

    def test_login_required_pages_return_200_for_authenticated_user(self):
        self.client.force_login(self.user)

        urls = [
            reverse("services:appointment_create"),
            reverse("services:appointments_list"),
        ]

        for url in urls:
            with self.subTest(url=url):
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, 200)

