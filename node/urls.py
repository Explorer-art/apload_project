from django.urls import path
from . import views

urlpatterns = [
	path("upload", views.upload),
	path("search", views.search),
	path("status", views.status),
]