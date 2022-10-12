from . import views
from django.urls import path


# urlpatterns = [
#     path('', views.ArticleList.as_view(), name='home'),
# ]

urlpatterns = [
    path('', views.view_items, name='home'),
]