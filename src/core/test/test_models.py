"""
モデルのテスト
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from . import models

def create_user(email="user@example.com", password="TestPass123"):
    """新しいユーザーを作成する"""
    return get_user_model().objects.create(email=email, password=password)


class Model_Tests(TestCase):
    """モデルをテストする"""
    pass
