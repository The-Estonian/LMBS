from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import (accounts, 
                            log_out, 
                            log_in, 
                            sign_up, 
                            reg_success, 
                            edit_accounts, 
                            public_account)

class TestUrls(SimpleTestCase):

    def test_user_account_info_is_resolved(self):
        url = reverse("user_account_info")
        self.assertEquals(resolve(url).func, accounts)
    
    def test_log_out_is_resolved(self):
        url = reverse("log_out")
        self.assertEquals(resolve(url).func, log_out)
    
    def test_log_in_is_resolved(self):
        url = reverse("log_in")
        self.assertEquals(resolve(url).func, log_in)
    
    def test_sign_up_is_resolved(self):
        url = reverse("sign_up")
        self.assertEquals(resolve(url).func, sign_up)
    
    def test_reg_success_is_resolved(self):
        url = reverse("reg_success")
        self.assertEquals(resolve(url).func, reg_success)
    
    def test_edit_accounts_is_resolved(self):
        url = reverse("edit_accounts")
        self.assertEquals(resolve(url).func, edit_accounts)
    
    def test_public_account_is_resolved(self):
        url = reverse("public_account", args=[1])
        self.assertEquals(resolve(url).func, public_account)
    
