from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('account_type', 'premium')
        return super().create_superuser(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    BASIC = 'basic'
    PREMIUM = 'premium'
    ACCOUNT_TYPE_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
    ]

    BUYER = 'buyer'
    SELLER = 'seller'
    MANAGER = 'manager'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
        (MANAGER, 'Manager'),
        (ADMIN, 'Admin'),
    ]

    phone = models.CharField(max_length=20, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=BUYER,
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=BASIC,
    )

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.role} / {self.account_type})'

    @property
    def is_seller(self):
        return self.role == self.SELLER

    @property
    def is_buyer(self):
        return self.role == self.BUYER

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    @property
    def is_premium(self):
        return self.account_type == self.PREMIUM