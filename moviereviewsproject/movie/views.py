from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Review
from .forms import ReviewForm


def home(request):
    # retrieve input of a search
    searchTerm = request.GET.get('searchMovie')

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, "home.html", {'searchTerm': "" if searchTerm is None else searchTerm, 'movies': movies})


def detail(request, movie_id):
    # get movie object depends on movie_id
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'detail.html', {'movie': movie, 'reviews': reviews})


@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        return render(request, 'createreview.html', {'form': ReviewForm(), 'movie': movie})

    try:
        form = ReviewForm(request.POST)
        # just retrieve, not save to database
        newReview = form.save(commit=False)
        newReview.user = request.user
        newReview.movie = movie
        newReview.save()
        return redirect('detail', newReview.movie.id)
    except ValueError:
        return render(request, 'createreview.html', {'form': ReviewForm(), 'error': 'bad data passed in, please try again.'})


@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', {'review': review, 'form': form})

    try:
        form = ReviewForm(request.POST, instance=review)
        form.save()
        return redirect('detail', review.movie.id)
    except ValueError:
        return render(request, 'updatereview.html', {'review': review, 'form': form, 'error': 'Bad data in form'})


@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if review.user == request.user:
        review.delete()
        return redirect('detail', review.movie.id)


def about(request):
    return HttpResponse('<h1>movie.about</h1>')


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})
