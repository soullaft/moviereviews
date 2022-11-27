from django.contrib import admin
from .models import Movie, Review

# added movie model to admin panel
admin.site.register(Movie)
admin.site.register(Review)
