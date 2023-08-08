from django.urls import reverse
from django.contrib.auth import get_user_model
from core.tests import BaseTestCase
from .models import Friendship, Profile

User = get_user_model()

class UserTestCase(BaseTestCase):
    def test_login(self):
        self.client.login(username=self.user1.username, password=self.user1.password)

    def test_logout(self):
        self.client.logout()

    def test_register(self):
        payload = {
            "username": "user3",
            "password1": "qwert.1234",
            "password2": "qwert.1234",
            "email": "user3@example.com",
        }
        res = self.client.post(reverse("users:register"), data=payload)
        self.assertEqual(res.url, reverse("users:login"))
        self.assertEqual(res.status_code, 302)
        self.assertEqual(User.objects.count(), 3)

    def test_profile(self):
        self.client.force_login(self.user1)
        res = self.client.get(
            reverse("users:profile", kwargs={"username": self.user1.username})
        )
        self.assertContains(res, self.user1.username, html=True)
        self.assertContains(res, self.user1.email, html=True)
        self.assertNotContains(res, self.user2.email, html=True)

    def test_profile_update(self):
        self.client.force_login(self.user1)
        payload = {
            "username": "user1_updated",
            "email": "user1_updated@example.com",
        }
        res = self.client.post(
            reverse("users:profile", kwargs={"username": self.user1.username}),
            data=payload,
        )
        self.assertEqual(res.status_code, 302)
        self.assertEqual(
            res.url,
            reverse("users:profile", kwargs={"username": payload.get("username")}),
        )

    def test_user_search(self):
        res = self.client.get(reverse("users:user-search"), {"query": "user"})
        self.assertContains(res, self.user1.username, html=True)
        self.assertContains(res, self.user2.username, html=True)

