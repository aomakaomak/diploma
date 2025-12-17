from django.urls import path


from .views import HomeView, ServiceCreateView, ServiceDetailView, DoctorListView

app_name = 'services'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('new/', ServiceCreateView.as_view(), name='service_create'),
    path('service_detail/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('about/', DoctorListView.as_view(), name='about'),

]

