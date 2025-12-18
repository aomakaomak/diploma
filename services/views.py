from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.views.generic.edit import FormMixin

from services.forms import ServiceForm, FeedbackForm, AppointmentForm
from services.models import MainPage, Service, Doctor, Appointment


class HomeView(FormMixin, ListView):
    model = Service
    template_name = "services/home.html"
    context_object_name = "services"

    form_class = FeedbackForm
    success_url = reverse_lazy("services:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_page"] = MainPage.objects.first()
        context["form"] = kwargs.get("form") or self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()

        if form.is_valid():
            name = form.cleaned_data["name"]
            phone = form.cleaned_data.get("phone", "")
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            subject = "Заявка с сайта: форма обратной связи (главная)"
            body = (
                f"Имя: {name}\n"
                f"Телефон: {phone}\n"
                f"Email: {email}\n\n"
                f"Сообщение:\n{message}\n"
            )

            try:
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f"Не удалось отправить письмо: {e}")
                context = self.get_context_data(form=form)
                return self.render_to_response(context)

            messages.success(request, "Спасибо! Сообщение отправлено. Мы свяжемся с вами в ближайшее время.")
            return redirect(f"{self.get_success_url()}#feedback")

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:home')

    def form_valid(self, form):
        if self.request.FILES:
            form.instance.image = self.request.FILES.get('image')
        return super().form_valid(form)


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'


class DoctorListView(ListView):
    model = Doctor
    template_name = "services/about.html"
    context_object_name = "doctors"


class ServicesListView(ListView):
    model = Service
    template_name = "services/services.html"
    context_object_name = "services"


class ContactsView(FormView):
    template_name = "services/contacts.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("services:contacts")

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        phone = form.cleaned_data.get("phone", "")
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]

        subject = "Заявка с сайта: форма обратной связи"
        body = (
            f"Имя: {name}\n"
            f"Телефон: {phone}\n"
            f"Email: {email}\n\n"
            f"Сообщение:\n{message}\n"
        )

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(self.request, f"Не удалось отправить письмо: {e}")
            return self.form_invalid(form)

        messages.success(self.request, "Спасибо! Сообщение отправлено. Мы свяжемся с вами в ближайшее время.")
        return super().form_valid(form)


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'services/appointment_form.html'
    success_url = reverse_lazy('services:home')


class AppointmentsListView(ListView):
    model = Appointment
    template_name = "services/appointments.html"
    context_object_name = "appointments"


