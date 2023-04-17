"""URLs for API V1."""

from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet, MeView,
                    NewTokenView, ReviewViewSet, SignUpView, TitleViewSet,
                    UserViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('users', UserViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/signup/', SignUpView.as_view()),
    path('auth/token/', NewTokenView.as_view()),
    path('users/me/', MeView.as_view()),
    path('', include(router_v1.urls)),
]
