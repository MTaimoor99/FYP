from django.shortcuts import render,redirect #Render page and redirect to another URL upon another action
from .helpers import scrape_reviews,generate_pie_plot #improting helper functions
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages #For sending out flash messages
from django.contrib.auth import authenticate,login as auth_login #For login and registration
from django.contrib.auth import logout #To log the user out
from django.views.decorators.csrf import csrf_protect #Needed to prevent CSRF attacks. Equivalent of {% csrf_token %}

from django.contrib.auth.decorators import login_required #Needed to restrict access

from .forms import CreateUserForm

#Imports needed for getting the API to work
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .apps import WebScraperConfig

#Imports needed for our prediction logic
from torch.nn.functional import softmax
import torch

import csv #To read our CSV file and send the sentences to our API view.
import requests #To make a GET request to our ML model API.

#API View responsible for calling the ML model
class call_model(APIView):

    def get(self,request):
        if request.method == 'GET':
            
            # sentence is the query we want to get the prediction for
            params =  request.GET.get('sentence')
            # predict logic
 
            input_ids= WebScraperConfig.tokenizer.encode(params,return_tensors='pt')
            attention_mask = torch.ones(input_ids.shape, dtype=torch.long)  
            token_type_ids = torch.zeros(input_ids.shape, dtype=torch.long)
            with torch.no_grad():
                logits = WebScraperConfig.predictor(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)[0]

            # Apply softmax to get probabilities
            probs = max(softmax(logits, dim=-1).tolist())

            # Identify the predicted sentiment class
            predicted_class = torch.argmax(logits).item()

            # Map the predicted class to sentiment labels
            sentiment_labels = ['negative', 'neutral', 'positive']
            predicted_sentiment = sentiment_labels[predicted_class]

            # Print results
            #print(f"Predicted sentiment: {predicted_sentiment}")
            #print(f"Class probabilities: {probs}")

            # returning JSON response
            #return JsonResponse(predicted_sentiment,safe=False)

            return Response({'prediction': predicted_sentiment}, status=status.HTTP_200_OK)

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('user_interface/')
    else:
        form=CreateUserForm()
        if request.method=='POST':
            form=UserCreationForm(request.POST)
            if form.is_valid():
                form.save() #Save to database
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
        csv_file_path=scrape_reviews(product_url) #Scrape reviews from user inputted URL
        predicted_sentiment_list=[]
        #Open the CSV file and read sentences from it.
        with open(csv_file_path, 'r', newline='',encoding='utf-8',errors='replace') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header if exists
            for row in csv_reader:
                sentence = row  # Assuming the sentence is in the first column
                
                #API URL where our ML model will perform predictions.
                api_url = f'http://127.0.0.1:8000/model/?sentence={sentence}'
                 # Make a GET request to the API URL
                response = requests.get(api_url)
                # Handle the response as needed
                if response.status_code == 200:
                    prediction = response.json()  # Assuming the response is JSON
                    predicted_sentiment_list.append(prediction['prediction'])
                else:
                    print(f'Failed to get prediction for "{sentence}"')
        pie_chart_base_64=generate_pie_plot(predicted_sentiment_list) 
        return render(request,'Main_Page.html',{'pie_chart_base_64':pie_chart_base_64})       
                
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