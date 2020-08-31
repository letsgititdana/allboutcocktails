import csv
import urllib
import certifi
import ssl
import pandas as pd
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from .forms import *

# Create your views here.

def index(request):
    with urllib.request.urlopen('https://www.thecocktaildb.com/api/json/v1/1/random.php', context=ssl.create_default_context(cafile=certifi.where())) as response:
        data = json.loads(response.read().decode())
        cocktailname = data.get('drinks')[0].get('strDrink')
        cocktailcategory = data.get('drinks')[0].get('strCategory')
        cocktailinstruction = data.get('drinks')[0].get('strInstructions')
        cocktailpic = data.get('drinks')[0].get('strDrinkThumb')

        ingredient_list = []
        for i in range(1, 15):
            element = data.get('drinks')[0].get('strIngredient'+str(i))
            if not (element is None):
                ingredient_list.append(element)
            else:
                pass


    with open('/Users/Dana/allboutcocktails/wineapp/static/koreancocktails1.csv', mode='r', encoding='ISO-8859-1') as k_cocktail:
        reader = csv.reader(k_cocktail)

        kcocktail_list = []
        for i in reader:
            kcocktail_list.append(i)

    contents = {}
    contents['cocktailofday'] = cocktailname
    contents['cocktailofdayimage'] = cocktailpic
    contents['cocktailofdaycategory'] = cocktailcategory
    contents['cocktailofdayinstruction'] = cocktailinstruction
    contents['cocktailofdayingredients'] = ingredient_list
    contents['monthlycocktail'] = kcocktail_list[8]

    return render(request,'index.html', contents)

def generic(request):
    return render(request,'generic.html')

def elements(request):
    return render(request,'elements.html')

def ranking(request):
    contents = []

    with open('/Users/Dana/allboutcocktails/wineapp/static/cocktail2020.csv', mode='r') as cocktail_lists:
        reader = csv.reader(cocktail_lists)
        for i in reader:
            contents.append(i)

    return render(request, 'ranking.html', {'data': contents})

def recommendation(request):
    return render(request,'recommendation.html')

def ingredient(request):
    return render(request,'ingredient.html')

def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def mypage(request):
    return render(request,'mypage.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account successfully created for ' + user)

                return redirect('login')

        context = {'form':form}
        return render(request,'register.html', context)

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('index')

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request,'login.html', context)

def userlogout(request):
    logout(request)
    return redirect('login')
