import csv
import urllib
import certifi
import ssl
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
import wikipedia
import requests
import json
from .models import Post

# Create your views here.

def index(request):
    with urllib.request.urlopen('https://www.thecocktaildb.com/api/json/v1/1/random.php', context=ssl.create_default_context(cafile=certifi.where())) as response:
        data = json.loads(response.read().decode())
        global cocktailname
        global cocktailcategory
        global cocktailinstruction
        global cocktailpic
        global cocktailid
        global ingredient_matching
        cocktailname = data.get('drinks')[0].get('strDrink')
        cocktailcategory = data.get('drinks')[0].get('strCategory')
        cocktailinstruction = data.get('drinks')[0].get('strInstructions')
        cocktailpic = data.get('drinks')[0].get('strDrinkThumb')
        cocktailid = data.get('drinks')[0].get('idDrink')
        #mainingredient1 = data.get('drinks')[0].get('strIngredient1')
        #mainingredient2 = data.get('drinks')[0].get('strIngredient2')
        # idIngrdeidnt는 604까지 있음 (https://www.thecocktaildb.com/api/json/v1/1/lookup.php?iid=604)

        #ingredient1Link = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?i=' + str(mainingredient1)
        #ingredient2Link = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?i=' + str(mainingredient2)

        #with urllib.request.urlopen(ingredient1Link, context=ssl.create_default_context(cafile=certifi.where())) as response:
        #    ingredient1 = json.loads(response.read().decode())
        #    ingredient1description = ingredient1.get('ingredients')[0].get('strDescription')

        ingredient_list = []
        for i in range(1, 15):
            element = data.get('drinks')[0].get('strIngredient' + str(i))
            if not (element is None):
                ingredient_list.append(element)
            else:
                pass
        measure_list = []
        for i in range(1, 15):
            element = data.get('drinks')[0].get('strMeasure' + str(i))
            if not (element is None):
                measure_list.append(element)
            else:
                pass

        ingredient_matching = []
        for i in range(len(ingredient_list)):
            ingredient_matching.append([ingredient_list[i], measure_list[i]])

    #with open('/Users/Dana/allboutcocktails/wineapp/static/koreancocktails1.csv', mode='r', encoding='ISO-8859-1') as k_cocktail:
    #    reader = csv.reader(k_cocktail)
    #    kcocktail_list = []
    #    for i in reader:
    #        kcocktail_list.append(i)

    contents = {}
    contents['cocktailofday'] = cocktailname
    contents['cocktailofdayimage'] = cocktailpic
    contents['cocktailofdaycategory'] = cocktailcategory
    contents['cocktailofdayinstruction'] = cocktailinstruction
    contents['cocktailofdayingredients'] = ingredient_list
    #contents['ingredient1description'] = ingredient1description
    #contents['monthlycocktail'] = kcocktail_list[8]

    return render(request,'index.html', contents)

def individual(request):
    individualcontents = {}
    individualcontents['individualname'] = cocktailname
    individualcontents['individualimage'] = cocktailpic
    individualcontents['individualcategory'] = cocktailcategory
    individualcontents['individualinstruction'] = cocktailinstruction
    individualcontents['individualingredient'] = ingredient_matching

    if request.method == 'POST':
        item = []
        item.append(cocktailname)
        item.append(cocktailpic)
        item.append(cocktailcategory)
        item.append(cocktailinstruction)
        item.append("https://www.thecocktaildb.com/api/json/v1/1/search.php?s="+str(cocktailname.replace(" ", "_")))

        Post(cocktailName=item[0], cocktailPic=item[1], cocktailAPI=item[4], cocktailCategory=item[2], cocktailInst=item[3], user=request.user).save()

    return render(request, 'individual.html', individualcontents)

def generic(request):

    return render(request,'generic.html')

def elements(request):
    return render(request,'elements.html')

def ranking(request):
    contents = []
    with open('../allboutcocktails/wineapp/static/cocktail2020.csv', mode = 'r') as cocktail_lists:
        reader = csv.reader(cocktail_lists)
        for i in reader:
            contents.append(i)

    if request.method == 'POST':
        result = []
        search_keyword = request.POST.get('q')
        if search_keyword:
            if len(search_keyword) > 2:
                search_keyword = (search_keyword.lower()).replace(" ", "")
                for row in contents:
                    cocktail_name = (row[2].lower()).replace(" ", "")
                    if search_keyword in cocktail_name:
                        result.append(row)

            contents = result
    else:
        contents = contents

    if request.method == 'GET':
        result = []
        categorylist = ['Gin', 'Vodka', 'Whiskey', 'Brandy', 'Tequila', 'Rum', 'Etc.']
        sort = request.GET.get('sort', '')
        if sort == 'All':
            contents = contents
        elif sort:
            for a in categorylist:
                if sort == a:
                    for i in range(len(contents)):
                        if sort in contents[i][12]:
                            result.append(contents[i])
            contents = result

    return render(request, 'ranking.html', {'data': contents})


def recommendation(request):

    return render(request,'recommendation.html')


WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
    except:
        return 0

def ingredient(request):
    contents = {}

    search_keyword = request.GET.get('q', '')
    if search_keyword != '':
        search_keyword = search_keyword.replace(" ", "_")

        with urllib.request.urlopen('https://www.thecocktaildb.com/api/json/v1/1/search.php?i='+search_keyword, context=ssl.create_default_context(cafile=certifi.where())) as response:
            data = json.loads(response.read().decode())

            ingredientname = data.get('ingredients')[0].get('strIngredient')
            ingredientdescription = data.get('ingredients')[0].get('strDescription')
            ingredienttype = data.get('ingredients')[0].get('strType')
            ingredientalcohol = data.get('ingredients')[0].get('strAlcohol')
            ingredientabv = data.get('ingredients')[0].get('strABV')

        contents['ingredientname'] = ingredientname
        contents['ingredientDescription'] = ingredientdescription
        contents['ingredienttype'] = ingredienttype
        contents['ingredientalcohol'] = ingredientalcohol
        contents['ingredientabv'] = ingredientabv

        wiki_image = get_wiki_image(ingredientname)
        contents['ingredientimage'] = wiki_image

        with urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="+search_keyword, context=ssl.create_default_context(cafile=certifi.where())) as response:
            data = json.loads(response.read().decode())
            temp = data.get('drinks')

        contents['tempList'] = temp

        return render(request, 'ingredient_detail.html', contents)

    return render(request,'ingredient.html', contents)

def ingredient_detail(request):
    return render(request,'ingredient_detail.html')


def about(request):
    #Post.objects.filter(user_id=12).delete()
    return render(request,'about.html')

@login_required(login_url='login')
def mypage(request):

    if request.user.is_authenticated:
        posts = Post.objects.filter(user=request.user)

    return render(request,'mypage.html', {'posts': posts})


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
