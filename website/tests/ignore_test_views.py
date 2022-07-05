from django.test import TestCase, RequestFactory, Client
from website.views import core_templates
from website.models import Templates, TemplateChoice, Posts
from django.contrib.auth.models import AnonymousUser, User
from django.urls import reverse
import json

class TestCoreTemplates(TestCase):
    def setUp(self):
        self.client = Client()
        self.index = reverse("index")
        self.all_posts = reverse("all_posts")
        self.add_post = reverse("add_post")


        self.user1 = User.objects.create_user(id=1, username="test1", password="test1")
        self.user2 = User.objects.create_user(id=2, username="test2", password="test2")
        # self.client1.post("/log_in/", {"email":"test@test.com", "password":"password123"})
        self.template_choice1 = TemplateChoice(template_choice="test_template1")
        self.template_choice1.save()
        self.template_choice2 = TemplateChoice(template_choice="test_template2")
        self.template_choice2.save()
        self.template1 = Templates.objects.create(user_id=self.user1, template=self.template_choice1)
        self.template1.save()
        self.template2 = Templates.objects.create(user_id=self.user2, template=self.template_choice2)
        self.template2.save()
        self.post1 = Posts.objects.create(id=1, user_id=self.user1, message="testMessage")
        self.post1.save()
        self.post2 = Posts.objects.create(id=2, user_id=self.user2, message="testMessage2")
        self.post2.save()


    def test_index_GET(self):
        response = self.client.get(self.index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "website/index.html")

    def test_all_posts_GET(self):
        response = self.client.get(self.all_posts)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "website/all_posts.html")

    def test_all_posts_delete_POST(self):
        response = self.client.post(self.all_posts, {
            "delete_post" : 1
        })
        # self.assertRaises(Posts.DoesNotExist)
        self.assertEquals(response.status_code, 200)
        with self.assertRaises(Posts.DoesNotExist):
            Posts.objects.get(id=1)

    def test_add_post_POST(self):
        response = self.client.post(self.add_post, {
            "new_post" : "test_post_message"
        })

        self.assertEquals(response.status_code, 302)
        print(Posts.objects.all())
        print(self.client)



