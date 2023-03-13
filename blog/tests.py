from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser')
        cls.post1 = Post.objects.create(
            title='Test title',
            text='This is test description',
            author=cls.user,
            status=Post.STATUS_CHOICES[0][0],

        )
        cls.post2 = Post.objects.create(
            title='Test title2',
            text='lorem ipsum description',
            author=cls.user,
            status=Post.STATUS_CHOICES[1][0]

        )

    def test_post_model_str(self):
        self.assertEqual(str(self.post1), self.post1.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'Test title')
        self.assertEqual(self.post2.text, 'lorem ipsum description')

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('blog'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('blog'))
        self.assertContains(response, self.post1.title)

    def test_post_detail_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_on_blog_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_404_for_detail_page(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_drf_post_not_show_in_post_list(self):
        response = self.client.get(reverse('blog'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('create_post'), {


            'title': 'this is test title',
            'text': 'this is test text',
            'status': 'pup',
            'author': self.user.id,
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'this is test title')
        self.assertEqual(Post.objects.last().text, 'this is test text')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update',  args=[self.post2.id]), {
            'title': 'this is update title',
            'text': 'this is text update',
            'status': 'pup',
            'author': self.post2.author.id,

        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'this is update title')
        self.assertEqual(Post.objects.last().text, 'this is text update')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)



