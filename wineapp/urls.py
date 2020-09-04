from django.urls import path
from.import views

urlpatterns = [
    path('elements/', views.elements, name='elements'),
    path('generic/', views.generic, name='generic'),
    path('index/', views.index, name='index'),
    path('ranking/', views.ranking, name='ranking'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('ingredient/', views.ingredient, name='ingredient'),
    path('about/',  views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('mypage/', views.mypage, name='mypage'),
    path('individual/', views.individual, name='individual'),
    path('ingredient_detail/', views.ingredient_detail, name='ingredient_detail'),
    #path('ingredient_detail/gin/', views.gin, name='gin'),
    #path('ingredient_detail/vodka/', views.vodka, name='vokda'),
    #path('ingredient_detail/whiskey/', views.whiskey, name='whiskey'),
    #path('ingredient_detail/rum/', views.rum, name='rum'),
]
