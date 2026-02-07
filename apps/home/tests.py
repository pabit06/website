from django.test import TestCase, Client


class HomeViewTests(TestCase):
    """Minimal tests for home and coming_soon views."""

    def setUp(self):
        self.client = Client()

    def test_home_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_coming_soon_returns_200(self):
        response = self.client.get('/coming-soon/')
        self.assertEqual(response.status_code, 200)
