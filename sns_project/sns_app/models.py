from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

REQUEST_STATUS = [
    (0, "pending"),
    (1, "Accepted"),
    (2, "Rejected")
]


class CustomUser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    date_joined = None
    last_login = None
    is_staff = None
    is_superuser = None
    is_active = models.BooleanField(default=True)
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=500)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'


class FriendRequests(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.SET_NULL, null=True)
    requested = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.SET_NULL,
                                  null=True)
    request_status = models.SmallIntegerField(choices=REQUEST_STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'friend_requests'

    def clean(self):
        if self.sender_id == self.requested_id:
            raise ValidationError("Sender and recipient cannot be the same user.")
