"""
モデルのテスト
"""

from django.test import TestCase
from django.contrib.auth import get_user_model



def create_user(email="user@example.com", password="Testpass123"):
    """新しいユーザーを作成する"""
    return get_user_model().objects.create(email=email, password=password)


class Model_Tests(TestCase):
    """モデルをテストする"""

    def test_create_user_with_email_successful(self):
        """メールを使用してユーザーを作成して成功したテスト"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """新規ユーザー向けにテストメールが標準化されたテスト。"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """電子メールなしでユーザーを作成すると ValueError が発生することをテストします。"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """スーパーユーザーを作成しテストする"""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "testPass123",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
