from django.shortcuts import render,redirect
from .helpers import scrape_reviews,sign_up
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages #For sending out flash messages
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.decorators import login_required #Needed to restrict access

from .forms import CreateUserForm

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('user_interface/')
    else:
        form=CreateUserForm()
        if request.method=='POST':
            form=UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,'Account was created for '+ user)
                return redirect('login')
        context={}
        context['form']=form
        return render(request,'SignUp.html',context)

@csrf_protect
def login(request):
     if request.user.is_authenticated:
        return redirect('user_interface/')
     else: 
        context={}
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)

            if user is not None:
                auth_login(request,user)
                return redirect('user_interface/')
            else:
                messages.info(request,'Username OR Password is incorrect')
                return render(request,'SignIn.html',context)
        return render(request,'SignIn.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')
    
@login_required(login_url='login')
def user_interface(request):
    if request.method=="POST":
        product_url=request.POST.get('product_url')
        print("Our product URL:",product_url)
        scrape_reviews(product_url)

    return render(request,'Main_Page.html')

@login_required(login_url='login')
def contact_us(request):
    return render(request,'ContactUsPage.html')

@login_required(login_url='login')
def user_history(request):
    return render(request,'History.html')

@login_required(login_url='login')
def about_us(request):
    return render(request,'Contact.html')