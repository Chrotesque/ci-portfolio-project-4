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
              'comment_mode', 'visible')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = [('visible'), ('category', RelatedDropdownFilter),
                   ('created_date'), ('author', RelatedDropdownFilter)]
    list_display = ('title', 'slug', 'category', 'author', 'updated_date',
                    'created_date', 'comment_mode', 'visible')
    search_fields = ['title', 'body', 'slug']
    summernote_fields = ('body')
    actions = ['publish_articles', 'comments_off', 'comments_moderation',
               'comments_autoapprove']

    def publish_articles(self, request, queryset):
        queryset.update(visible=True)

    def comments_off(self, request, queryset):
        queryset.update(comment_mode='OFF')

    def comments_moderation(self, request, queryset):
        queryset.update(comment_mode='MOD')

    def comments_autoapprove(self, request, queryset):
        queryset.update(comment_mode='AAC')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    fields = ('body', 'author', 'article', 'visible')
    list_display = ('author', 'article', 'body', 'created_date', 'visible')
    list_filter = [('visible'), ('created_date'),
                   ('author', RelatedDropdownFilter)]
    search_fields = ['author', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(visible=True)
