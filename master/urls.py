from django.urls import path
from . import views

urlpatterns = [
	path("", views.home),
	path("images/<str:filename>", views.images),
	path("load_balancer", views.load_balancer),
]