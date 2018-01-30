from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^cart$', views.Cart.as_view()),
    url(r'^settlement$', views.BuyNowSettlementView.as_view()),
    url(r'^order/buynow$', views.BuyNowOrderView.as_view()),
    url(r'^orders$', views.OrderListView.as_view()),
    url(r'^orders/(?P<order_id>\d+)$', views.OrderDetailView.as_view()),
    url(r'^goods/upload$', views.GoodsUpload.as_view()),
    url(r'^goods/(?P<goods_id>\d+)/detail$', views.GoodsDetail.as_view()),
    url(r'^goods/(?P<goods_id>\d+)/sku/upload$', views.GoodsSkuUpload.as_view()),
    url(r'^helloworld$', views.HelloWorld.as_view()),
    url(r'^home$', views.Home.as_view()),
    url(r'^home/banner/upload$', views.HomeBannerUpload.as_view()),
    url(r'^login$', views.Login.as_view()),
    url(r'^orders/(?P<order_id>\d+)/payment$', views.weixin_pay_cb)
]
