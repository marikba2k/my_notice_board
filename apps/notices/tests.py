from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notice


User = get_user_model()


class NoticeTestMixin:
    password = "testpass123"

    def create_user(self, username="mark"):
        return User.objects.create_user(
            username=username,
            password=self.password
        )

    def login_user(self, username="mark"):
        return self.client.login(
            username=username,
            password=self.password
        )

    def create_notice(self, author, title="Test notice", body="This is a test notice body"):
        return Notice.objects.create(
            title=title,
            body=body,
            author=author
        )


class NoticeListViewTests(NoticeTestMixin, TestCase):
    def test_notice_list_is_paginated(self):
        user = self.create_user("pagination_user")

        for i in range(15):
            self.create_notice(
                author=user,
                title=f"Notice {i}",
                body="Test body"
            )

        response = self.client.get(reverse("notices:list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["notices"]), 10)


    def test_notice_list_second_page_contains_remaining_notices(self):
        user = self.create_user("pagination_user_2")

        for i in range(15):
            self.create_notice(
                author=user,
                title=f"Notice {i}",
                body="Test body"
            )

        response = self.client.get(reverse("notices:list") + "?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["notices"]), 5)

    


class NoticeCreateViewTests(NoticeTestMixin, TestCase):
    def setUp(self):
        self.user = self.create_user("mark")

    def test_logged_in_user_can_create_notice(self):
        self.login_user("mark")

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


class NoticeUpdateViewTests(NoticeTestMixin, TestCase):
    def setUp(self):
        self.user = self.create_user("mark")

    def test_user_can_edit_own_notice(self):
        self.login_user("mark")

        notice = self.create_notice(author=self.user)

        response = self.client.post(reverse("notices:edit", args=[notice.id]), {
            "title": "Updated notice",
            "body": "This is an updated notice body",
        })

        notice.refresh_from_db()

        self.assertRedirects(response, reverse("notices:list"))
        self.assertEqual(notice.title, "Updated notice")
        self.assertEqual(notice.body, "This is an updated notice body")
        self.assertEqual(notice.author, self.user)

    def test_user_cannot_edit_other_users_notice(self):
        other_user = self.create_user("john")
        notice = self.create_notice(author=other_user)

        self.login_user("mark")

        response = self.client.post(reverse("notices:edit", args=[notice.id]), {
            "title": "Hacked",
            "body": "This is an updated notice body",
        })

        notice.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(notice.title, "Test notice")
        self.assertEqual(notice.body, "This is a test notice body")
        self.assertEqual(notice.author, other_user)


class NoticeDeleteViewTests(NoticeTestMixin, TestCase):
    def setUp(self):
        self.user = self.create_user("mark")

    def test_user_can_delete_own_notice(self):
        self.login_user("mark")

        notice = self.create_notice(author=self.user)

        response = self.client.post(reverse("notices:delete", args=[notice.id]))

        self.assertRedirects(response, reverse("notices:list"))
        self.assertEqual(Notice.objects.count(), 0)

    def test_user_cannot_delete_other_users_notice(self):
        other_user = self.create_user("john")
        notice = self.create_notice(author=other_user)

        self.login_user("mark")

        response = self.client.post(reverse("notices:delete", args=[notice.id]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Notice.objects.filter(id=notice.id).exists())