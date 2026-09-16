from django.shortcuts import render
from dashboard.models import Review

# Create your views here.

def index(request):
    # Pulls up to 3 random reviews from the database to display
    random_reviews = Review.objects.all().order_by('?')[:3]
    
    context = {
        'random_reviews': random_reviews,
    }
    return render(request, 'main/index.html', context)
def test(request):
    return render(request, 'base_copy.html')