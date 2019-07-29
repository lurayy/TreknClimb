from django.urls import path
from . import views

urlpatterns = [
    path('<str:package_name>',views.index, name = "Whole Package"),
    path('',views.index, name = "things")
]
