from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_cat, name='upload_cat'),
    path('like/<int:cat_id>/', views.like_cat, name='like_cat'),
    path('profile/', views.profile, name='profile'),
    path('delete/<int:cat_id>/', views.delete_cat, name='delete_cat'),
]
