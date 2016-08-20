from django.conf.urls import url, include
from hropapi.views import *


# Routers provide an easy way of automatically determining the URL conf.
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hrops', HropViewSet)

urlpatterns = [
    url(r'^users/register', RegistrationsView.as_view()),
    url(r'^', include(router.urls)),
    # url(r'^profiles/(?P<user_id>[0-9]+)$', ),

]