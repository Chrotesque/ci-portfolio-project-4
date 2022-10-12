from django.contrib import admin
from .models import Category, Article, Comment
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):

    fields = ('title', 'slug', 'body', 'author', 'category', 'header_image',
              'visible')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = [('visible'), ('category', RelatedDropdownFilter),
                   ('created_date'), ('author', RelatedDropdownFilter)]
    list_display = ('title', 'slug', 'category', 'updated_date',
                    'created_date', 'visible')
    search_fields = ['title', 'body', 'slug']
    summernote_fields = ('body')
    actions = ['publish_articles']

    def publish_articles(self, request, queryset):
        queryset.update(visible=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    fields = ('body', 'author', 'article', 'visible')
    list_display = ('author', 'body', 'article', 'created_date', 'visible')
    list_filter = [('visible'), ('created_date'),
                   ('author', RelatedDropdownFilter)]
    search_fields = ['author', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(visible=True)
