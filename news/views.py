from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
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


# detailed article view
class ArticleView(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(visible=True)
        article = get_object_or_404(queryset, slug=slug)
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
