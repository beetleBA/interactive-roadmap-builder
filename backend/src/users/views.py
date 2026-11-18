from rest_framework import views, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import Stack, UserStack
from .serializers import LoginSerializer, RegisterSerializer, StackSerializer, UpdateSerializer, UserSerializer, UserStackSerializer
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema


@extend_schema(
    summary="Вход в систему",
    request=LoginSerializer,
    responses=UserSerializer,
    tags=["Пользователи"],
)
class LoginViews(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)
        return Response(UserSerializer(user).data, status=200)


@extend_schema(
    summary="Регистрация",
    request=RegisterSerializer,
    responses=UserSerializer,
    tags=["Пользователи"],
)
class RegisterViews(views.APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        login(request, user)

        return Response(
            UserSerializer(
                user,
                context={"request": request},
            ).data,
            status=201,
        )


@extend_schema(
    summary="Выход из системы",
    tags=["Пользователи"],
    responses={204: None},
)
class LogoutViews(views.APIView):
    def post(self, request):
        logout(request)
        return Response(status=200)


class UsersViews(views.APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(
        summary="Текущий пользователь",
        responses=UserSerializer,
        tags=["Пользователи"],
    )
    def get(self, request):
        serializer = UserSerializer(
            request.user,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=200,
        )

    @extend_schema(
        summary="Изменение профиля",
        request=UpdateSerializer,
        responses=UserSerializer,
        tags=["Пользователи"],
    )
    def patch(self, request):
        serializer = UpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            UserSerializer(
                user,
                context={"request": request},
            ).data,
            status=200,
        )


@extend_schema(
    summary="Деактивация аккаунта",
    request=None,
    responses={204: None},
    tags=["Пользователи"],
)
class DeactivateViews(views.APIView):
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save(update_fields=["is_active"])

        logout(request)

        return Response(
            status=204,
        )


@extend_schema(
    summary="Список технологий",
    tags=["Справочники"],
)
class StackViewSet(viewsets.ModelViewSet):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer
    search_fields = ['name']
    ordering_fields = ['name']


@extend_schema(
    summary="Список технологий пользователя",
    tags=["Пользователи"],
)
class UserStackViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserStackSerializer
    pagination_class = None

    def get_queryset(self):
        return UserStack.objects.filter(
            user=self.request.user
        ).select_related("stack")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
