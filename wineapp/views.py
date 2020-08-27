from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.

def index(request):
    return render(request,'index.html')

def generic(request):
    return render(request,'generic.html')

def elements(request):
    return render(request,'elements.html')

def ranking(request):
    cocktail_list = ['blood_and_sand','irish_coffee','brandy_alexander','old_cuban',
                    'bamboo','sidecar','vodka_martini','ramos_gin_fizz','caipirinha',
                    'gin_gin_mule','vesper','cosmopolitan','white_lady','rum_old_fashioned',
                    'paloma','tom_collins','vieux_carre','pornstar_martini','the_southside',
                    'pina_colada','gin_fizz','last_word','pisco_sour',"bee's_knees",
                    'bramble','americano','mai_tai','amaretto_sour','sazerac','aviation',
                    "dark_'n'_stormy",'penicillin','french_75','clover_club','boulevardier',
                    'bloody_mary',"tommy's_margarita",'gimlet','moscow_mule','aperol_spritz',
                    'mojito','manhattan','margarita','espresso_martini','whiskey_sour',
                    'dry_martini','daiquiri','negroni','old_fashioned']
    final_list = []
    for i in cocktail_list:
        with urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v1/1/search.php?s="+i) as url:
            data = json.loads(url.read().decode())
            if data.get('drinks') is None:
                continue
            else:
                final_list.append(data.get('drinks')[0])
    print(final_list)

    return render(request, 'ranking.html', {'final_list':final_list})

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
