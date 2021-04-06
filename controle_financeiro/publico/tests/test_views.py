from django.test import TestCase


class IndexViewTest(TestCase):

    def test_status_code_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
