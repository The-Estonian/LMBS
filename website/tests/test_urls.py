from django.test import SimpleTestCase
from django.urls import reverse, resolve
from website.views import index, all_posts, add_post, user_posts, edit_post, public_posts

class TestUrls(SimpleTestCase):

    def test_index_is_resolved(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, index)

    def test_all_posts_is_resolved(self):
        url = reverse("all_posts")
        self.assertEquals(resolve(url).func, all_posts)

    def test_add_post_is_resolved(self):
        url = reverse("add_post")
        self.assertEquals(resolve(url).func, add_post)

    def test_user_posts_is_resolved(self):
        url = reverse("user_posts")
        self.assertEquals(resolve(url).func, user_posts)

    def test_edit_post_is_resolved(self):
        url = reverse("edit_post", args=[1])
        self.assertEquals(resolve(url).func, edit_post)

    def test_public_posts_is_resolved(self):
        url = reverse("public_posts", args=[1])
        self.assertEquals(resolve(url).func, public_posts)

