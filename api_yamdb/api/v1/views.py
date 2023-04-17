"""Views in API app."""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters, generics, mixins, permissions, status, viewsets,)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .permissions import (
    IsAdmin, IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly,)
from .serializers import (
    CategorySerializer, CommentSerializer, CreateUpdateTitleSerializer,
    GenreSerializer, MeSerializer, NewTokenSerializer, ReviewSerializer,
    SignUpSerializer, TitleSerializer, UserSerializer,)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class GetPatchView(generics.UpdateAPIView, generics.RetrieveAPIView):
    """Get+Patch mix View."""


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """Create+Destroy+list mix ViewSet."""


class CategoryViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Category instances."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """A viewset for viewing and editing Genre instances."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing Title instances."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """A viewset for Reviews."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsOwnerAdminModeratorOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    """A viewset for Comments."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsOwnerAdminModeratorOrReadOnly)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        return review.comments.all()


class SignUpView(generics.CreateAPIView):
    """Class for registration and retrive conconfirmation_code."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def send_code(self, code, email):
        """Send email with confirmation_code."""
        send_mail(
            'code',
            f'confirmation_code = {code}',
            'admin@yamdb.ru',
            [email],
            fail_silently=False,
        )

    def post(self, request):
        """GET confirmation_code."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if User.objects.filter(username=username, email=email).exists():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if (User.objects.filter(email=email).exists()
           or User.objects.filter(username=username).exists()):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        user, _ = User.objects.get_or_create(
            username=username, email=email
        )
        user.confirmation_code = default_token_generator.make_token(user)
        user.save(update_fields=['username', 'email', 'confirmation_code'])
        self.send_code(user.confirmation_code, user.email)


class NewTokenView(generics.CreateAPIView):
    """Class for retrive new Auth token."""

    serializer_class = NewTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user=user,
                                               token=confirmation_code):
            response = {
                'token': str(AccessToken.for_user(user)),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Users ViewSet."""

    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'list', 'delete', 'patch')


class MeView(GetPatchView):
    """View for /me."""

    queryset = User.objects.all()
    serializer_class = MeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        resp = MeSerializer(request.user, context=request).data
        return Response(resp, status=status.HTTP_200_OK)

    def partial_update(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        resp = MeSerializer(request.user).data
        return Response(resp, status=status.HTTP_200_OK)
