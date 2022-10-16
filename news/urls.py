from . import views
from django.urls import path


urlpatterns = [
    path('', views.ArticleList.as_view(), name='home'),
    path('about/', views.ArticleList.as_view(), name='about'),
    path('contact/', views.ArticleList.as_view(), name='contact'),
    path('<slug:slug>/', views.ArticleView.as_view(), name='article_detail'),
]
