from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topq/', views.topQueries, name='topQueries'),
    path('topqd/<int:days>/', views.topQueries, name='topQueries'),
    path('user/<int:idx>/', views.userInfo, name='userInfo'),
    path('host/<int:idx>/', views.hostInfo, name='hostInfo'),
    path('prgm/<int:idx>/', views.prgmInfo, name='prgmInfo'),
    path('qry/<int:qidx>/', views.qryInfo, name='qryInfo'),

]
