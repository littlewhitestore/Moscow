from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^home$', views.Home.as_view()),
]
