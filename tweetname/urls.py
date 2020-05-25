from django.urls import path,include
from . import views
from django.conf.urls import url

urlpatterns = [
  #path('', views.InputFormView.as_view(), name='input-home'),
  #url('', views.hello_get_query, name='hello_get_query'), # 追加する
  url('^$', views.tweet, name='tweet'),
  #url('^$', views.kakikomi, name='kakikomi'),
]