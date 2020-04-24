"""NoteSpace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.urls import include, path

from notes import views

urlpatterns = [
    url(r'^$',views.homepage, name="home_page"),
    url(r'^about/', views.about, name='about'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/addreview/', views.add_review_api, name='add_review_api'),
    url(r'^api/login/', views.login_api, name='login_api'),
    url(r'^api/register/', views.register_api, name='register_api'),
    url(r'^api/upload/', views.upload_api, name='upload_api'),
    url(r'^notes/',include('notes.urls')),
    url(r'^register/', views.register_page, name="register_page"),
    url(r'^search/$', views.searchpage, name="search"),
    url(r'^upload/',views.uploadpage, name='upload_page'),
    
    path("help/", views.helppage, name='help'),
    path("help/<str:help_topic>", views.help_detail, name='help_detail'),
    path("tag/<str:tag>", views.tag_query, name="tagQuery"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
