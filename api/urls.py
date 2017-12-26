from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^helloworld$', views.HelloWorld.as_view()),
    url(r'^home$', views.Home.as_view()),
    url(r'^goods/(?P<goods_id>\d+)/detail$', views.GoodsDetail.as_view()),
]
