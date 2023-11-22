from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about', views.about),
    path('create', views.create),
    path('listing', views.listing),
    path('createproduct', views.createproduct),

]
