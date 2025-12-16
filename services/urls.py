from django.urls import path


from .views import HomeView

app_name = 'services'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]

