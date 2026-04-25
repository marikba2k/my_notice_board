
# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notice


class NoticeCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="mark",
            password="testpass123"
        )

    def test_logged_in_user_can_create_notice(self):
        self.client.login(username="mark", password="testpass123")

        response = self.client.post(reverse("notices:create"), {
            "title": "Test notice",
            "body": "This is a test notice body",
        })

        self.assertRedirects(response, reverse("notices:list"))
        self.assertEqual(Notice.objects.count(), 1)

        notice = Notice.objects.first()
        self.assertEqual(notice.title, "Test notice")
        self.assertEqual(notice.author, self.user)

    def test_logged_out_user_is_redirected_from_create_notice(self):
        response = self.client.get(reverse("notices:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)