from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic
from .models import Article, Category


# class ArticleList(generic.ListView):
#     model = Article
#     queryset = Article.objects.filter(visible=1).order_by('-created_date')
#     template_name = 'index.html'
#     paginate_by = 10


# class CategoryList(generic.ListView):
#     model = Category
#     queryset = Category.objects.order_by('name')
#     template_name = 'index.html'

def view_items(request):
    articles = Article.objects.filter(visible=1).order_by('-created_date')
    categories = Category.objects.order_by('name')

    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': articles,
        'categories': categories,
        'page_obj': page_obj
    }

    return render(request, 'index.html', context)
