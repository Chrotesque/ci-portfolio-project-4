from . import views
from django.urls import path


urlpatterns = [
     path('', views.ArticleList.as_view(), name='home'),
     path('category/<slug:slug>/', views.CategoryList.as_view(),
          name='category_listing'),
     path('article/<slug:slug>/', views.ArticleView.as_view(),
          name='article_detail'),
     path('article/<slug:slug>/comment/<int:id>/modify/',
          views.updateComment, name='update_comment'),
     path('article/<slug:slug>/comment/<int:id>/delete/',
          views.deleteComment, name='delete_comment'),
]
