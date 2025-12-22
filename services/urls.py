from django.urls import path

from .views import (AppointmentCreateView, AppointmentsListView, ContactsView,
                    DoctorListView, HomeView, ServiceCreateView,
                    ServiceDetailView, ServicesListView)

app_name = "services"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("new/", ServiceCreateView.as_view(), name="service_create"),
    path(
        "service_detail/<int:pk>/", ServiceDetailView.as_view(), name="service_detail"
    ),
    path("about/", DoctorListView.as_view(), name="about"),
    path("services/", ServicesListView.as_view(), name="services_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path(
        "new-appointment/", AppointmentCreateView.as_view(), name="appointment_create"
    ),
    path("appointments/", AppointmentsListView.as_view(), name="appointments_list"),
]
