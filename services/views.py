from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from services.forms import ServiceForm
from services.models import MainPage, Service


class HomeView(ListView):
    model = Service
    template_name = "services/home.html"
    context_object_name = "services"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_page"] = MainPage.objects.first()
        return context


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



# class MainPageView(TemplateView):
#     template_name = 'services/home.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["main_page"] = MainPage.objects.first()
#         return context

