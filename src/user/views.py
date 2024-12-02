"""

"""

import re
from django.contrib.auth import get_user_model


from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.settings import api_settings

from .serializers import UserCreateSerializer


class CreateUserView(APIView):
    """新しいユーザーを作成する"""

    # serializer_class = UserCreateSerializer

    def post(self, request,format=None):
        # ユーザーのパラメータを取得
        ser = UserCreateSerializer(data=request.data)
        name = ser.get("name")
        email = ser.get("email")
        password = ser.get("password")
        password_confirmation = ser.get("password_confirmation")
        # パラメータを検証する
        if not all([name, email, password, password_confirmation]):
            return Response(
                {"error": "ユーザーが必要の情報が入力してください｡"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # ユーザー名がすでに登録したかどうか検証する
        if get_user_model.objects.filter(name=name):
            return Response(
                {"error": "入力したユーザー名すでに登録されました｡"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # メールアドレスがすでに登録したかどうか検証する
        if get_user_model.objects.filter(email=email):
            return Response(
                {"error": "入力したメールアドレスすでに登録されました｡"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # メールアドレスのの正規表現を検証する
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$",
            email,
        ):
            return Response(
                {"error": "入力したメールの形式が間違っています｡"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 入力したパスワードが一致しているかどうかを検証する
        if password != password_confirmation:
            return Response(
                {"error": "入力したパスワードは一致していません｡"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # パスワードの長さを検証する
        if not (6 < len(password) < 18):
            return Response(
                {"error": "パスワードの長さは6桁から18桁までです｡"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ユーザーをを作成する
        obj = get_user_model.create_user(name=name, password=password)
        res = {"name": obj.name, "id": obj.id, "email": obj.email}
        return Response(res, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """ユーザーログイン"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        """ログイン後ユーザーを返す"""
        result = serializer.validated_data
        result["name"] = serializer.user.name
        result["email"] = serializer.user.email
        result["token"] = result.pop("access")

        return Response(result, status=status.HTTP_200_OK)


# class CreateTokenView(ObtainAuthToken):
#     """ユーザーの新しい認証用トークンを作成する"""

#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class ManageUserView(generics.RetrieveUpdateAPIView):
#     """認証されたユーザーを管理する"""

#     serializer_class = UserSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         """認証されたユーザーを取得する"""
#         return self.request.user
