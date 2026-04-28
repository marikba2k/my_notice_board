
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
        self.assertEqual(notice.body, "This is a test notice body")
        self.assertEqual(notice.author, self.user)


    def test_logged_out_user_is_redirected_from_create_notice(self):
        response = self.client.get(reverse("notices:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


    def test_user_can_edit_own_notice(self):
        self.client.login(username="mark", password="testpass123")
        notice = Notice.objects.create(
            title="Test notice",
            body="This is a test notice body",
            author=self.user
        )

        response = self.client.post(reverse("notices:edit", args=[notice.id]), {
            "title": "Updated notice",
            "body": "This is an updated notice body",
        })

        notice = Notice.objects.get(id=notice.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(notice.title, "Updated notice")
        self.assertEqual(notice.body, "This is an updated notice body")
        self.assertEqual(notice.author, self.user)
        self.assertRedirects(response, reverse("notices:list"))

    def test_user_cannot_edit_other_users_notice(self):
        
        other_user =get_user_model().objects.create_user(
            username="john",
            password="pass1234"
        )
        notice = Notice.objects.create(
            title="Test notice",
            body="This is a test notice body",
            author=other_user
        )

        self.client.login(username="mark", password="testpass123")

        response = self.client.post(reverse("notices:edit", args=[notice.id]), {
            "title": "Hacked",
            "body": "This is an updated notice body",
        })

        notice.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(notice.title, "Test notice")
        self.assertEqual(notice.body, "This is a test notice body")
        self.assertEqual(notice.author, other_user)

    def test_user_can_delete_own_notice(self):

        self.client.login(username="mark", password="testpass123")
        notice = Notice.objects.create(
            title="Test notice",
            body="This is a test notice body",
            author=self.user
        )

        response = self.client.post(reverse("notices:delete", args=[notice.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Notice.objects.count(), 0)
        self.assertRedirects(response, reverse("notices:list"))


        
