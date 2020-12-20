from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import User
from .permissions import IsAdminPermissions
from .serializers import UserSerializer, ConfirmationCodeSerializer, \
    UserCreationSerializer

EMAIL_AUTH = 'authorization@yamdb.fake'


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    """
    Receiving a JWT token in exchange for email and confirmation_code. 
    """

    serializer = ConfirmationCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response({'confirmation_code': 'Неверный код подтверждения'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirm_code(request):
    """
    Sending confirmation_code to the transmitted email.
    Get or Creating an User object.
    """

    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user = User.objects.get_or_create(
        email=email,
        username=username,
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(subject='Yours confirmation code',
              message=f'confirmation_code: {confirmation_code}',
              from_email=EMAIL_AUTH,
              recipient_list=(email, ),
              fail_silently=False)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    1) [GET] Get list of users objects. [POST] Create user object. 'users/'
    2) [GET]Get user object by username. [PATCH] Patch user data by username.
    [DELETE] Delete user object by username. 'users/{username}/'
    3) [GET] Get your account details. [PATCH] Change your account details.
    'users/me/'
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminPermissions]
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=(IsAuthenticated, ),
            url_path='me')
    def me(self, request):
        user_profile = get_object_or_404(User, email=self.request.user.email)
        if request.method == 'GET':
            serializer = UserSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user_profile,
                                    data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
