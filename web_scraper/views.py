from django.shortcuts import render
from .helpers import scrape_reviews

# Create your views here.
def user_interface(request):
    if request.method=="POST":
        product_url=request.POST['product_url']
        #print("Our product URL:",product_url)
        scrape_reviews(product_url)

    return render(request,'UserInterface.html')