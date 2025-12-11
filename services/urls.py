from django.urls import path


from .views import ProductListView

app_name = 'services'

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
]

