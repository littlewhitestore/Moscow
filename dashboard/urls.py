from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^goods$', views.GoodsListView.as_view(), name="dashboard.goods.list"),
    url(r'^goods/(?P<goods_id>\d+)/edit$', views.GoodsEditView.as_view(), name="dashboard.goods.edit"),
]
