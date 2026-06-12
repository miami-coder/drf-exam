from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .permissions import IsAdminUserRole
from .serializers import ManagerCreateSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ManagerCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ManagerCreateSerializer
    permission_classes = [IsAdminUserRole]


class UpgradeToPremiumView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        if request.user.role not in [CustomUser.MANAGER, CustomUser.ADMIN]:
            return Response(
                {"detail": "Only managers or admins can grant Premium status."},
                status=status.HTTP_403_FORBIDDEN
            )

        target_user = get_object_or_404(CustomUser, pk=pk)

        if target_user.account_type == CustomUser.PREMIUM:
            return Response(
                {"detail": f"User {target_user.username} already has Premium status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        target_user.account_type = CustomUser.PREMIUM
        target_user.save()

        return Response(
            {
                "detail": f"To the user {target_user.username} successfully activated Premium!",
                "user_id": target_user.id,
                "account_type": target_user.account_type
            },
            status=status.HTTP_200_OK
        )


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": "Token is invalid or already expired."},
                status=status.HTTP_400_BAD_REQUEST
            )