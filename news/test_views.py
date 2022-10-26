from django.test import TestCase
from .models import Article, Comment, Category
from django.contrib.auth.models import User
from django.utils.text import slugify


class TestViews(TestCase):

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
                                              visible=True)
        self.comment = Comment.objects.create(body=self.item,
                                              visible=True,
                                              article=self.article,
                                              author=self.user)

    # views > categories_to_base
    def test_categories_to_base(self):

        categories = ('Test Category', 'Second Test Category')
        for category in categories:
            entry = Category.objects.create(name=category,
                                            slug=slugify(category))
            response = self.client.get('/')
            self.assertContains(
                response,
                '<a class="dropdown-item" href="/category/'
                f'{entry.slug}/">{entry.name}</a>',
                status_code=200
            )
            self.assertTemplateUsed(response, 'base.html')

    # views > ArticleList
    def test_article_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # views > CategoryList
    def test_category_list(self):
        response = self.client.get(f'/category/{self.category.slug}',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_listing.html')

    # views > ArticleView get
    def test_article_view_get(self):
        response = self.client.get(f'/article/{self.article.slug}',
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')

    # views > ArticleView post
    def test_article_view_post(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(f'/article/{self.article.slug}/',
                                    {'body': 'test'})
        comment = Comment.objects.all()
        # 2 instead of 1, due to SetUp already creating a comment
        self.assertEqual(len(comment), 2)

    # views > updateComment
    def test_can_edit_comment(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(f'/article/{self.article.slug}/comment/'
                                    f'{self.comment.id}/modify/',
                                    {'body': 'Modified Test Comment'})
        u_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(u_comment.body, "Modified Test Comment")

    # views > deleteComment
    def test_can_delete_comment(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(f'/article/{self.article.slug}/'
                                    f'comment/{self.comment.id}/delete/')
        comment = Comment.objects.all()
        # similar to test_article_view_post, this one uses SetUp comment
        self.assertEqual(len(comment), 0)
