from django.test import TestCase
from .models import Article, Comment, Category
from django.contrib.auth.models import User
from django.utils.text import slugify


class TestModels(TestCase):

    def setUp(self):
        self.username = 'Test User'
        self.password = 'testpass'
        self.item = 'Test Item'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.category = Category.objects.create(name=self.item,
                                                slug=slugify(self.item))
        self.article = Article.objects.create(title=self.item,
                                              slug=slugify(self.item),
                                              category=self.category,
                                              visible=False)
        self.comment = Comment.objects.create(body=self.item,
                                              visible=True,
                                              article=self.article,
                                              author=self.user)

        self.categories = Category.objects.all()
        self.articles = Article.objects.all()
        self.comments = Comment.objects.all()

    # category related tests
    def test_category_creation(self):
        self.assertEqual(len(self.categories), 1)

    def test_category_length(self):
        category = Category.objects.create(name='123456789012345678'
                                           '901234567890123')
        self.assertTrue(len(category.name) >= 30)

    # article related tests
    def test_article_creation(self):
        self.assertEqual(len(self.articles), 1)

    def test_article_comment_mode_default(self):
        for article in self.articles:
            self.assertEqual(article.comment_mode, "AAC")

    # comment related & general tests
    def test_comment_creation(self):
        self.assertEqual(len(self.comments), 1)

    def test_commonfield_inheritance(self):
        for article in self.articles:
            self.assertTrue(article.visible is False)

    def test_foreignkey(self):
        for comment in self.comments:
            self.assertEqual(self.user, comment.author)
