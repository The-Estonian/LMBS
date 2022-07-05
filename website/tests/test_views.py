from django.test import TestCase, RequestFactory, Client
from website.views import (core_templates, 
                           index, 
                           all_posts, 
                           add_post, 
                           user_posts, 
                           edit_post, 
                           public_posts)
from django.contrib.auth.models import AnonymousUser, User
from website.models import Templates, TemplateChoice, Posts
from django.urls import reverse
from django.template.loader import render_to_string


class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        self.index = reverse("index")
        self.all_posts = reverse("all_posts")
        self.add_post = reverse("add_post")  
        self.user_posts = reverse("user_posts")  
        self.edit_post = reverse("edit_post", args=[1])  
        self.public_posts = reverse("public_posts", args=[2])  

        self.user1 = User.objects.create_user(id=1, username="test1", password="test1")
        self.user2 = User.objects.create_user(id=2, username="test2", password="test2")

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

    def test_core_templates_anon(self):
        """
        Tests:
        Test if default template extension is loaded for the site.
        """
        self.request = self.factory.get("")
        self.request.user = AnonymousUser()
        response = core_templates(self.request)
        self.assertEqual(response["templates"], Templates.objects.get(user_id=1))

    def test_core_templates(self):
        """
        Test:
        Test to see if user picked template extension is being loaded for the site.
        """
        self.request = self.factory.get("")
        self.request.user = self.user2
        response = core_templates(self.request)
        self.assertEqual(response["templates"], Templates.objects.get(user_id=2))

    def test_index(self):
        """
        Tests:
        Test if connection is OK
        Test if correct template is loaded
        """
        request = self.factory.get(self.index)
        request.user = AnonymousUser()
        response = index(request)
        self.assertEquals(response.status_code, 200)
        with self.assertTemplateUsed("website/index.html"):
            render_to_string("website/index.html")

    def test_all_posts_GET(self):
        """
        Tests:
        Test if connection is OK
        Test if correct template is loaded
        Test if correct models are forwarded by context
        """
        response = self.client.get(self.all_posts)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "website/all_posts.html")
        self.assertIsInstance(response.context["all_posts"][0], Posts)

    def test_all_posts_POST(self):
        """
        Tests:
        Test if correct Model and ID of that Model is deleted
        """
        request = self.factory.get(self.all_posts)
        request.user = self.user1
        request.method = "POST"
        request.POST = {
            "delete_post" : 1
        }
        all_posts(request)
        with self.assertRaises(Posts.DoesNotExist):
            Posts.objects.get(id=1)

    def test_add_post_GET(self):
        """
        Tests:
        Test if connection is OK
        Test if correct template is loaded
        """
        request = self.factory.get(self.add_post)
        request.user = self.user1
        request.method = "GET"
        response = add_post(request)
        self.assertEquals(response.status_code, 200)
        with self.assertTemplateUsed("website/add_post.html"):
            render_to_string("website/add_post.html")


    def test_add_post_POST(self):
        """
        Tests:
        Test if connection redirect is OK
        Test if correct Module object is created with correct input
        """
        request = self.factory.get(self.add_post)
        request.user = self.user1
        request.method = "POST"
        request.POST = {
            "new_post" : "test_post_message"
        }
        response = add_post(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Posts.objects.filter(user_id=self.user1).latest("id").message, "test_post_message")
        

    def test_user_posts_POST(self):
        """
        Tests:
        Test if connection is OK
        Test if correct template is used
        Test if the right Module object is deleted with correct ID
        """
        request = self.factory.get(self.user_posts)
        request.user = self.user1
        request.method = "POST"
        request.POST = {
            "delete_post" : 2
        }
        response = user_posts(request)
        self.assertEquals(response.status_code, 200)
        with self.assertTemplateUsed("website/user_posts.html"):
            render_to_string("website/user_posts.html")
        with self.assertRaises(Posts.DoesNotExist):
            Posts.objects.get(id=2)

    def test_edit_post_GET(self):
        """
        Tests:
        Test if connection is OK
        Test if correct template is used
        """
        request = self.factory.get(self.edit_post)
        request.user = self.user1
        request.method = "GET"
        response = edit_post(request, 1)
        with self.assertTemplateUsed("website/edit_post.html"):
            render_to_string("website/edit_post.html")
        self.assertEquals(response.status_code, 200)

    def test_edit_post_POST(self):
        request = self.factory.get(self.edit_post)
        request.user = self.user1
        request.method = "POST"
        request.POST = {
            "edit_post" : "edited_post"
        }
        self.assertEquals(Posts.objects.get(id=1).message, "testMessage")
        response = edit_post(request, 1)
        self.assertEquals(Posts.objects.get(id=1).message, "edited_post")
        self.assertEquals(response.status_code, 302)

    def test_public_posts(self):
        response = self.client.get(self.public_posts)
        self.assertEquals(response.context["public_post"][0].user_id, self.user2)
        self.assertEquals(response.status_code, 200)
        with self.assertTemplateUsed("website/public_posts.html"):
            render_to_string("website/public_posts.html")

