from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name=""),
    path('register/',views.register,name='register'),
    path('user-login/',views.login,name='user-login'),
    path('dashboard/',views.Dashboard,name='dashboard'),
    path('log-out/',views.user_logout,name='log-out'),
    path('create-record/',views.create_record,name='create-record'),
    path('update-record/<int:pk>/',views.update_record,name='update-record'),
    path('view-record/<int:pk>',views.view_record,name='view-record'),
    path('delete-record/<int:pk>',views.delete_record,name='delete-record'),
    
]