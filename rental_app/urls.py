from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('about', views.about),
    path('create', views.create),
    path('createproduct', views.createproduct),
    path('rental', views.rental),
    path('contact', views.contact),
    # path('upload_image', views.upload_image)
    path('createproduct', views.createproduct)
]
