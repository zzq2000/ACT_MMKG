from django.urls import path
from . import views

urlpatterns = [
    path('search', views.search),
    path('detection', views.detect),
    path('graph', views.graph)
]
