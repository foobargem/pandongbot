from django.conf.urls import url
from . import views 


urlpatterns = [
    url(r'^$', views.index, name="linebot_index"),
    url(r'^webhook/', views.webhook, name="linebot_webhook"),
]
