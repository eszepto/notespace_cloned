from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("<int:note_index>/", views.detial,name="detail")
]