from django.urls import path
from .import views

urlpatterns = [
    path('<int:movie_id>', views.detail, name='detail'),
    path('create/<int:movie_id>', views.createreview, name='createreview'),
    path('review/<int:review_id>', views.updatereview, name='updatereview'),
    path('review/delete/<int:review_id>',
         views.deletereview, name='deletereview'),
]
