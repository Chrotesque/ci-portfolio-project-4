from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.utils.text import slugify
from .models import Article, Category


# adds categories to navigation on base.html
def categories_to_base(request):
    categories = Category.objects.order_by('name')
    context = {'categories', }
    return render(request, "base_html", context)


# listing of articles in index.html
class ArticleList(generic.ListView):
    model = Article
    queryset = Article.objects.filter(visible=True).order_by('-created_date')
    template_name = 'index.html'
    paginate_by = 2


# listing of articles per category
class CategoryList(generic.ListView):
    model = Article
    template_name = 'index.html'
    paginate_by = 1

    def get_queryset(self, *args, **kwargs):
        queryset = self.model.objects.all()
        if self.kwargs.get('slug'):
            category_id = Category.objects.get(slug=self.kwargs['slug'])
            queryset = queryset.filter(category=category_id)

        return queryset


# detailed article view
class ArticleView(View):

    def get(self, request, slug, *args, **kwargs):
        article_query = Article.objects.filter(visible=True)
        article = get_object_or_404(article_query, slug=slug)
        comments = article.comments.filter(visible=True) \
            .order_by('created_date')

        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments
            }
        )
