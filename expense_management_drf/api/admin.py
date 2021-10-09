from rest_framework.authtoken.admin import TokenAdmin
from django.contrib import admin
from .models import Category

TokenAdmin.raw_id_fields = ['user']

admin.site.register(Category)