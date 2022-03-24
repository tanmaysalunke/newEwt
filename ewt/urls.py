from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser , name='logout'),
    path('dataentry1', views.test_data, name='dataentry1'),
    path('dataentry/', views.dataEntry, name='dataentry'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('viewdata/', views.viewdata, name='viewdata'),
    path('viewdata1', views.sendToData, name='viewdata1'),
    path('replace/', views.replaceComp, name='replacecomponents'),
    path('senddata', views.sendData, name="senddata")
]
