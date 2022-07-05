from django.test import TestCase
from website.models import TemplateChoice

class TestTemplateChoice(TestCase):
    def setUp(self):
        self.data = TemplateChoice.objects.create(template_choice="Template1")

    def test_template_choice(self):
        self.assertTrue(isinstance(self.data, TemplateChoice))
    
    def test_template_choice_return(self):
        self.assertEqual(str(self.data), "Template1")
