from django.conf.urls import patterns, include, url
urlpatterns = patterns(
    '',
    url(r'$', views.promotions_view, name='api.v5.promotions.scene'), 
)
