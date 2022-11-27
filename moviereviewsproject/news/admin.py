from django.contrib import admin
from .models import News

# added movie model to admin panel
admin.site.register(News)
