from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class CommonFields(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    visible = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Article(CommonFields):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    header_image = CloudinaryField('image', default='placeholder')
    OFF = 'OFF'
    MOD = 'MOD'
    AAC = 'AAC'
    COMMENT_CHOICES = [
        (OFF, 'Off'),
        (MOD, 'Moderated'),
        (AAC, 'Auto-Approve'),
    ]
    comment_mode = models.CharField(max_length=3, choices=COMMENT_CHOICES,
                                    default=AAC)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.title


class Comment(CommonFields):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='comments')

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
