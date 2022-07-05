from django.test import TestCase, RequestFactory, Client
from accounts.views import (email_validator,
                            username_validator,
                            name_validator,
                            name_cleaner,
                            sign_up,
                            reg_success,
                            edit_accounts)
from website.models import Templates, TemplateChoice
from django.contrib.auth.models import AnonymousUser, User                            
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.sessions.middleware import SessionMiddleware




class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

        self.user_account_info = reverse("user_account_info")
        self.log_out = reverse("log_out")
        self.log_in = reverse("log_in")
        self.sign_up = reverse("sign_up")
        self.reg_success = reverse("reg_success")
        self.edit_accounts = reverse("edit_accounts")
        self.public_account = reverse("public_account", args=[1])

        self.user1 = User.objects.create_user(id=1, username="test1", password="test1", email="test1@test1.com")
        self.user2 = User.objects.create_user(id=2, username="test2", password="test2", email="test2@test2.com")
        self.user3 = User.objects.create_user(id=3, 
                                            username="test_username", 
                                            email="test.email@mail.com", 
                                            password="test_password",
                                            first_name = "FirstNameTest",
                                            last_name = "Lastnametest")

        self.template_choice1 = TemplateChoice(template_choice="test_template1")
        self.template_choice1.save()
        self.template_choice2 = TemplateChoice(template_choice="test_template2")
        self.template_choice2.save()
        self.template_choice3 = TemplateChoice(template_choice="test_template3")
        self.template_choice3.save()

        self.template1 = Templates.objects.create(user_id=self.user1, template=self.template_choice1)
        self.template1.save()
        self.template2 = Templates.objects.create(user_id=self.user2, template=self.template_choice2)
        self.template2.save()
        self.template3 = Templates.objects.create(user_id=self.user3, template=self.template_choice3)
        self.template3.save()

    def test_email_validator(self):
        email1 = "first.last@name.com"
        email2 = "firstlast@name.com"
        email3 = "FiRsT.lAsT@naMe.com"
        email4 = "fIrStLaSt@name.CoM"
        email5 = "12fir.sTl2st@nam3.com"
        email6 = "first.last.name.com"
        email7 = "first.Last@Name"
        self.assertTrue(email_validator(email1))
        self.assertTrue(email_validator(email2))
        self.assertTrue(email_validator(email3))
        self.assertTrue(email_validator(email4))
        self.assertTrue(email_validator(email5))
        self.assertFalse(email_validator(email6))
        self.assertFalse(email_validator(email7))
        
    def test_username_validator(self):
        username1 = "UserNameOne"
        username2 = "usEr_name"
        username3 = "User.Name"
        username4 = "uSer-Name"
        username5 = "Us3r.Na-M3"
        username6 = "User Name"
        username7 = "uSER&name"
        username8 = "abcde"

        self.assertTrue(username_validator(username1))
        self.assertTrue(username_validator(username2))
        self.assertTrue(username_validator(username3))
        self.assertTrue(username_validator(username4))
        self.assertTrue(username_validator(username5))
        self.assertFalse(username_validator(username6))
        self.assertFalse(username_validator(username7))
        self.assertFalse(username_validator(username8))

    def test_name_validator(self):
        name1 = "Name"
        name2 = "nAmE"
        name3 = "NAME"
        name4 = "name"
        name5 = "na me"
        name6 = "na&me"

        self.assertTrue(name_validator(name1))
        self.assertTrue(name_validator(name2))
        self.assertTrue(name_validator(name3))
        self.assertTrue(name_validator(name4))
        self.assertFalse(name_validator(name5))
        self.assertFalse(name_validator(name6))

    def test_name_cleaner(self):
        name1 = "Name"
        name2 = "nAmE"
        name3 = "NAME"
        name4 = "name"

        self.assertEquals(name_cleaner(name1), "Name")
        self.assertEquals(name_cleaner(name2), "Name")
        self.assertEquals(name_cleaner(name3), "Name")
        self.assertEquals(name_cleaner(name4), "Name")

    def test_log_out(self):
        response = self.client.post(self.log_out)
        self.assertEquals(response.status_code, 302)

    def test_reg_success(self):
        request = self.factory.get(self.reg_success)
        request.user = self.user1
        response = reg_success(request)
        self.assertEquals(response.status_code, 200)
        with self.assertTemplateUsed("accounts/reg_success.html"):
            render_to_string("accounts/reg_success.html")

    def test_sign_up_POST(self):
        request = self.factory.get(self.sign_up)
        request.user = AnonymousUser()
        request.method = "POST"
        request.POST = {
            "username": "test_username2",
            "email": "test.email@mail.com",
            "password": "test_password",
            "password2": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest"
        }
        response = sign_up(request)
        self.assertEquals(User.objects.get(id=4).username, "test_username2")
        self.assertEquals(response.status_code, 302)
        with self.assertTemplateUsed("accounts/sign_up.html"):
            render_to_string("accounts/sign_up.html")
        
    def test_sign_up_POST_errors(self):
        response = self.client.post(self.sign_up, {
            "username": "test_username",
            "email": "test.email@mailcom",
            "password": "test_password",
            "password2": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest"
        })
        self.assertTrue(response.context["email_error"])

        response = self.client.post(self.sign_up, {
            "username": "test_username",
            "email": "test.email@mail.com",
            "password": "test_password_one",
            "password2": "test_password_two",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest"
        })
        self.assertTrue(response.context["password_match"])

        response = self.client.post(self.sign_up, {
            "username": "test username",
            "email": "test.email@mail.com",
            "password": "test_password",
            "password2": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest"
        })
        self.assertTrue(response.context["username_error"])

        response = self.client.post(self.sign_up, {
            "username": "test_username",
            "email": "test.email@mail.com",
            "password": "test_password",
            "password2": "test_password",
            "first_name": "First NameTest",
            "last_name": "Lastnametest"
        })
        self.assertTrue(response.context["name_error"])

        response = self.client.post(self.sign_up, {
            "username": "test_username",
            "email": "test.email@mail.com",
            "password": "test_password",
            "password2": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Last nametest"
        })
        self.assertTrue(response.context["name_error"])

    def test_edit_accounts_POST(self):
        request = self.factory.post(self.edit_accounts)
        request.user = self.user3
        request.method = "POST"
        request.POST = {
            "username": "test_username",
            "email": "test.email@mail.com",
            "old_password": "test_password",
            "new_password": "test_password",
            "new2_password": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest2"
        }
        edit_accounts(request)
        self.assertEquals(User.objects.get(id=3).last_name, "Lastnametest2")

    def test_log_in_POST(self):
        self.client.post(self.log_in, {"email": "test.email@mail.com", "password": "test_password"})
        response = self.client.post(self.log_in, {
            "email": "test email@mail.com",
            "password": "test_password"
        })
        self.assertTrue(response.context["email"])

        response = self.client.post(self.log_in, {
            "email": "test_email@mail.com",
            "password": "test_password"
        })
        self.assertTrue(response.context["user_error"])

        response = self.client.post(self.log_in, {
            "email": "test.email@mail.com",
            "password": "est_password"
        })
        self.assertTrue(response.context["password_error"])

        with self.assertTemplateUsed("accounts/login.html"):
            render_to_string("accounts/login.html")

    def test_log_in_GET(self):
        self.client.get(self.log_in)
        with self.assertTemplateUsed("accounts/login.html"):
            render_to_string("accounts/login.html")

    def test_edit_accounts_POST_errors(self):
        self.client.post(self.log_in, {"email": "test.email@mail.com", "password": "test_password"})
        response = self.client.post(self.edit_accounts, {
            "username": "test_username4",
            "email": "test.email@mail.com",
            "old_password": "test password",
            "new_password": "test_password",
            "new2_password": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest2"
        })
        self.assertTrue(response.context["wrong_password"])

        response = self.client.post(self.edit_accounts, {
            "username": "test_username4",
            "email": "test.email@mail.com",
            "old_password": "test_password",
            "new_password": "testpassword",
            "new2_password": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest2"
        })
        self.assertTrue(response.context["password_missmatch"])

        response = self.client.post(self.edit_accounts, {
            "username": "test_username4",
            "email": "test.emailmail.com",
            "old_password": "test_password",
            "new_password": "test_password",
            "new2_password": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest2"
        })
        self.assertTrue(response.context["email"])

        response = self.client.post(self.edit_accounts, {
            "username": "test username4",
            "email": "test.email@mail.com",
            "old_password": "test_password",
            "new_password": "test_password",
            "new2_password": "test_password",
            "first_name": "FirstNameTest",
            "last_name": "Lastnametest2"
        })
        self.assertTrue(response.context["username_error"])

    def test_public_account_GET(self):
        self.client.get(self.public_account)
        with self.assertTemplateUsed("accounts/public_account.html"):
            render_to_string("accounts/public_account.html")

    def test_accounts_GET(self):
        self.client.post(self.log_in, {"email": "test.email@mail.com", "password": "test_password"})
        response = self.client.get(self.user_account_info)
        with self.assertTemplateUsed("accounts/accounts.html"):
            render_to_string("accounts/accounts.html")
        self.assertEquals(response.context["account_info"][0].username, "test_username")
        # print(response.context)

    def test_accounts_POST_delete(self):
        self.client.post(self.log_in, {"email": "test.email@mail.com", "password": "test_password"})
        self.client.post(self.user_account_info, {
            "delete-account": "3"})
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=3)
        
    def test_accounts_POST_template1(self):
        self.client.post(self.log_in, {"email": "test1@test1.com", "password": "test1"})
        self.client.post(self.user_account_info, {
            "orange": ""})
        user_template = Templates.objects.get(user_id=1)
        self.assertEquals(user_template.template, TemplateChoice.objects.get(id=1))
        
    def test_accounts_POST_template2(self):
        self.client.post(self.log_in, {"email": "test2@test2.com", "password": "test2"})
        self.client.post(self.user_account_info, {
            "green": ""})
        user_template = Templates.objects.get(user_id=2)
        self.assertEquals(user_template.template, TemplateChoice.objects.get(id=2))
        
    def test_accounts_POST_template3(self):
        self.client.post(self.log_in, {"email": "test.email@mail.com", "password": "test_password"})
        self.client.post(self.user_account_info, {
            "purple": ""})
        user_template = Templates.objects.get(user_id=3)
        self.assertEquals(user_template.template, TemplateChoice.objects.get(id=3))
