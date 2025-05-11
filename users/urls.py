from . import views
from django.urls import path, include

urlpatterns = [
    path('login/', views.user_login),
    path('logout/', views.user_logout, name='logout_user'),
    path('create/', views.user_register, name='user_create'),
    path('show_user/', views.show_users, name='show_user'),
    path('edit_user/<int:id>', views.edit_user, name='update_user'),
    path('delete_user/<int:id>', views.delete_users, name='remove_user'),
    # path('', include('visiters.urls')),

    # forget password section
    path('forget_password/', views.forget_password, name='forget_password'),
    path('change_password/<token>/', views.change_password, name='change_password'),
    path('demo/', views.demo, name='demo'),
]
