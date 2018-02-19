from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^goods$', views.GoodsListView.as_view()),
]
