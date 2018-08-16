from django.conf.urls import url
from . import views

app_name = 'blog'  # 视图函数命名空间，区分不同应用之间视图函数命名相同的问题
urlpatterns = [
    # 第一个参数是网址，第二个参数是处理函数，第三个参数是处理函数的别名
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^search/$', views.search, name='search'),




]