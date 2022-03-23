from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser , name='logout'),
    path('dataentry/', views.dataEntry, name='dataentry'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('viewdata/', views.viewdata, name='viewdata'),
    path('replacecomponents/', views.replaceComp, name='replacecomponents')
]
