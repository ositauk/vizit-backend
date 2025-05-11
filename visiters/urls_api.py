from django.urls import path
from . import views_api

urlpatterns = [
    path('search_visitors/<int:pk>/', views_api.search_visitor.as_view()),
    path('user_checkin/<int:pk>/', views_api.search_visitor.as_view()),
    path('visit/', views_api.visitapi.as_view()),
    path('host_details/', views_api.host_details.as_view()),
    path('<int:pk>/upload_image/', views_api.image_upload.as_view()),
    path('print/<int:pk>/', views_api.printtag_details.as_view()),
]
