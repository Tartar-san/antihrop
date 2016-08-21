"""antihrop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render
from django.conf.urls.static import static

urlpatterns = [
  url(r'^$',
      view=lambda request: render(request, 'pages/home.html') if not isinstance(request.user,
                                                                                AnonymousUser) else render(
          request, 'pages/login.html')),
  url(r'^login/$',
      view=lambda request: render(request, 'pages/login.html') if not isinstance(request.user,
                                                                                 AnonymousUser) else render(
          request, 'pages/login.html')),
  url(r'^hrops_length/$',
      view=lambda request: render(request, 'pages/hrops_length.html') if not isinstance(request.user,
                                                                                        AnonymousUser) else render(
          request, 'pages/login.html')),
  url(r'^max_intensity/$',
      view=lambda request: render(request, 'pages/max_intensity.html') if not isinstance(request.user,
                                                                                         AnonymousUser) else render(
          request, 'pages/login.html')),
  url(r'^avg_intensity/$',
      view=lambda request: render(request, 'pages/avg_intensity.html') if not isinstance(request.user,
                                                                                         AnonymousUser) else render(
          request, 'pages/login.html')),
  url(r'^counts/$', view=lambda request: render(request, 'pages/counts.html')),
  url(r'^admin/', admin.site.urls),
  url(r'^api/', include('hropapi.urls')),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
