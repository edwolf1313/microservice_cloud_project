from django.urls import path, include
from rest_framework import routers
from django.conf.urls import url, include
from session_api.views import CreateAccessView,LoginAccessView,CheckSessionView,DeleteSessionView
#RefreshAccessView

router = routers.DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginAccessView.as_view()),
    path("register/", CreateAccessView.as_view()),
    path("auth/", CheckSessionView.as_view()),
    path("logout/",DeleteSessionView.as_view()),
    #path("refreshtoken/", RefreshAccessView.as_view())
]
