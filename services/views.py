from django.shortcuts import render
from django.views.generic import ListView


class ProductListView(ListView):
    template_name = 'services/base.html'
    context_object_name = 'home'
    queryset = []

