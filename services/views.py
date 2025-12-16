
from django.views.generic import ListView, TemplateView

from services.models import MainPage, Service


# class MainPageView(TemplateView):
#     template_name = 'services/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["main_page"] = MainPage.objects.first()
#         return context


class HomeView(ListView):
    model = Service
    template_name = "services/home.html"
    context_object_name = "services"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_page"] = MainPage.objects.first()
        return context


