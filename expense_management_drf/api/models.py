from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Category(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_categories')
    name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.name


