from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Article, Category, Comment
from django.contrib.auth.models import User
from .forms import CommentForm


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
    paginate_by = 9


# listing of articles per category
class CategoryList(generic.ListView):
    model = Article
    template_name = 'index.html'
    paginate_by = 9

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
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm()
            }
        )

    def post(self, request, slug, *args, **kwargs):
        user_name = User.objects.get(username=request.user.username)
        article_query = Article.objects.filter(visible=True)
        article = get_object_or_404(article_query, slug=slug)
        comments = article.comments.filter(visible=True) \
            .order_by('created_date')
        comment_form = CommentForm(data=request.POST)
        user = request.POST.get("author")

        if comment_form.is_valid():
            message = "Comment successfully created."
            messages.add_message(request, messages.SUCCESS, message)
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = user_name
            if article.comment_mode == "AAC":
                comment.visible = True
                commented = False
            else:
                comment.visible = False
                commented = True
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "article_detail.html",
            {
                "article": article,
                "comments": comments,
                "commented": commented,
                "comment_form": CommentForm()
            }
        )


# edit comment page
def updateComment(request, slug, id):
    article = get_object_or_404(Article, slug=slug)
    comment = get_object_or_404(Comment, id=id)
    form = CommentForm(instance=comment)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            message = "Comment successfully edited."
            messages.add_message(request, messages.SUCCESS, message)
            form.save()
        return HttpResponseRedirect(reverse('article_detail', args=[slug]))

    context = {'comment_form': form, 'comment': comment, }
    return render(
        request,
        'update_comment.html',
        context
    )


# delete comment page
def deleteComment(request, slug, id):
    article = get_object_or_404(Article, slug=slug)
    comment = get_object_or_404(Comment, id=id)

    if request.method == 'POST':
        message = "Comment successfully deleted."
        messages.add_message(request, messages.SUCCESS, message)
        comment.delete()
        return HttpResponseRedirect(reverse('article_detail', args=[slug]))

    context = {'comment': comment, 'article': article}
    return render(
        request,
        'delete_comment.html',
        context
    )
