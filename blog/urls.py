from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('posts/', views.post_list, name='post_list'),
    path('tag/<str:tag>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
