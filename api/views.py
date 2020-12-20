from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import exceptions, filters, status, viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from users.models import User

from .models import Category, Genre, Title, Review, Comment

from .permissions import IsAdmin, IsAnon, IsModerator, IsAdminOrReadOnly, \
    RetrieveUpdateDestroyPermission, MyCustomPermissionClass

from .filters import TitlesFilter

from .serializers import CategorySerializer, GenreSerializer, \
    ReviewSerializer, CommentSerializer, TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (
        MyCustomPermissionClass,
        IsAuthenticatedOrReadOnly,
    )
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        categories = Category.objects.all()
        return categories

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = (
        MyCustomPermissionClass,
        IsAuthenticatedOrReadOnly,
    )
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        genres = Genre.objects.all()
        return genres

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(ratings=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter


class ReviewListCreateSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [IsAnon | IsAdmin | IsModerator | IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        author = self.request.user
        text = self.request.data.get('text')

        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)

        reviews = Review.objects.filter(author=author, title=title)
        if reviews.count() > 0:
            return True

        serializer.save(title=title, author=author, text=text)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        not_create_success = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if not_create_success:
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST,
                            headers=headers)
        else:
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)


class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [
        RetrieveUpdateDestroyPermission,
    ]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                pk=self.kwargs['review_id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset


class CommentListCreateSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [IsAnon | IsAdmin | IsModerator | IsAuthenticated]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        author = self.request.user
        text = self.request.data.get('text')

        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(title.reviews, id=review_id)
        serializer.save(review=review, author=author, text=text)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(title.reviews.all(), id=review_id)
        queryset = review.comments.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        not_create_success = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if not_create_success:
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST,
                            headers=headers)
        else:
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)


class CommentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [
        RetrieveUpdateDestroyPermission,
    ]

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                pk=self.kwargs['comment_id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(title.reviews.all(), id=review_id)
        queryset = review.comments.all()
        return queryset
