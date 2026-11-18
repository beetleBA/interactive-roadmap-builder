from django.urls import path
from .views import (
    LoginViews,
    LogoutViews,
    StackViewSet,
    UsersViews,
    RegisterViews,
    DeactivateViews,
    UserStackViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'stack', StackViewSet, basename='stack')
router.register(r'user-stack', UserStackViewSet, basename='user-stack')

urlpatterns = [
    path('register', RegisterViews.as_view(), name='register'),
    path('login', LoginViews.as_view(), name='login'),
    path('logout', LogoutViews.as_view(), name='logout'),
    path('current', UsersViews.as_view(), name='current'),
    path('deactivate', DeactivateViews.as_view(), name='deactivate'),
] + router.urls
