from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

admin.site.register(Account)  # Register the Account model

