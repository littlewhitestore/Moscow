from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^goods/(?P<goods_id>\d+)/detail$', views.GoodsDetail.as_view()),
    url(r'^helloworld$', views.HelloWorld.as_view()),
    url(r'^home$', views.Home.as_view()),
    url(r'^home/banner/upload$', views.HomeBannerUpload.as_view()),
    url(r'^login$', views.Login.as_view()),
    url(r'^cart$', views.Cart.as_view()),
    url(r'^settlement/buynow$', views.SettlementBuyNowView.as_view()),
    url(r'^order/all$', views.OrderListView.as_view()),
    url(r'^order/create/buynow$', views.BuyNowOrderView.as_view()),
    url(r'^order/(?P<order_id>\d+)$', views.OrderDetailView.as_view()),
    url(r'^order/(?P<order_id>\d+)/pay/success$', views.WeixinPayCallbackView.as_view()),
    url(r'^order/(?P<order_sn>\d+)/logistics$', views.delivery),
    url(r'^wechat/user/info/upload$', views.WXUserInfoUpload.as_view()),
]
