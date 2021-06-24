"""ExploAR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from Dashboard import views
from django.conf.urls import url
from django.urls import path, include,re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('home/', views.home, name = 'home'),
    path('signIn/', views.signIn, name = 'signIn'),
    path('postSignIn/', views.postSignIn, name = 'postSignIn'),
    path('logout/', views.logout, name = 'logout'),
    path('signUp/', views.signUp, name = 'signUp'),
    path('postSignUp/', views.postSignUp, name = 'postSignUp'),
    re_path(r'^dashboard/(?:(<name>))?', views.dashboard, name='dashboard'),
    path('home/<str:name>', views.dashboard1, name='dashboard1'),
    re_path(r'^dashboard/(?:(<name>))?/(?:(<product>))?', views.dashboard3, name='dashboard3'),
    path('home/<str:name>/<str:product>', views.dashboard4, name='dashboard4'),
    path('rfp/', views.rfp1, name='rfp1'),
    path('incoming_rfp/', views.rfp2, name='rfp2'),
    re_path(r'^rfp_detail/(?:(<name>))?', views.rfp_detail, name='rfp_detail'),
    path('incoming_rfp/<str:name>', views.rfp_detail1, name='rfp_detail1'),
    path('my_view_that_updates_pieFact', views.my_view_that_updates_pieFact, name='my_view_that_updates_pieFact'),
    path('create_rfp/rfp_d/', views.rfp_d, name='rfp_d'),
    path('create_rfp/', views.Createrfp, name="create_rfp"),
    path('insert_data/', views.Insert_data, name="insert"),
    path('delete_data', views.delete_data,name="delete_data"),
    path('user_detail/', views.user_detail, name='user_detail'),
    path('charts/', views.charts, name='charts'),
    path('chart/', views.population_chart, name='chart'),\
]