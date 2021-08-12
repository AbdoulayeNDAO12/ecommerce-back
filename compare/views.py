from django.contrib.auth.models import User, Group
from rest_framework import viewsets,permissions 
from .models import Searchs
from .serializers import SearchSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.files.storage import default_storage
import requests
from bs4 import BeautifulSoup
import dateutil.parser
import datetime

# Create your views here.
tableau = []
parametre="angular"
jumiaURLTab=["?page=2#catalog-listing","?page=3#catalog-listing"]

def scrapCatJumia():
    tableau=[]
    URL = 'https://www.jumia.sn/'    
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser') 
        category = soup.find_all('main')
        for article in category:   
            listCat= article.find_all('div',class_='flyout')
            for cat in listCat:   
                catName=cat.find_all('a',{"href":True},class_='itm')
                for item in catName: 
                        catName=item.text
                        catLink=item['href']
                        if 'https' not in   catLink:
                            catLink='https://www.jumia.sn'+catLink
                        tableau.append({'catName':catName,'catLink':catLink})
    except:
        print("An error occured")
    return tableau

def scrapSubCatJumia():
    table=scrapCatJumia()
    listSubCat=[]
    try:
        for cat in table:        
            URL = cat['catLink']  
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')    
            category = soup.find_all('main')
            for article in category:        
                categoryName = article.find('a',class_='-db -pvs -phm -m -hov-bg-gy05')
                subCategoryName = article.find_all('a',class_='-db -pvs -phxl -hov-bg-gy05') 
                for item in subCategoryName: 
                    catName=cat['catName']  
                    catLink=cat['catLink']  
                    subCategoryName=item.text
                    subCategoryLink=item['href']
                    listSubCat.append({'name':subCategoryName,'link':subCategoryLink,'catName':catName,'catLink':catLink})
    except:
        print("An error occured")
    return listSubCat


def scrapJumia(keyWord):
    URL = 'https://www.jumia.sn/catalog/?q='+str(keyWord)
    #https://www.jumia.sn/ordinateurs-accessoires-informatique/
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        articles = soup.find_all('article',class_="prd _fb col c-prd")
        for article in articles:
            image = article.find('div',class_='img-c').img['data-src']
            src = article.find('a')['href']
            info = article.find('div',class_='info')
            name = info.find('h3',class_='name').text
            price = info.find('div',class_='prc').text
            category=article.find('a')['data-category']
            # old_price = info.find('div',class_='old').text
            # tableau.append(name)
            # tableau.append(price)
            # tableau.append(old_price.text.strip())
            tableau.append({"image":image,"price":price,"name":name,"src":src,"category":category}) 
        return tableau  
    except:
        return []

def scrapSenAchat(keyWord):
    
    URL = "https://www.senachat.com/search?q="+keyWord
    #https://www.senachat.com/category/informations
    try:        
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        jobs = soup.find_all('div',class_='aiz-card-box border border-light rounded shadow-sm hov-shadow-md mb-2 has-transition bg-white')
        for article in jobs:
            price = article.find('span',class_='fw-700 text-primary').text
            name = article.find('h3',class_='fw-600 fs-13 text-truncate-2 lh-1-4 mb-0').text
            more_info = article.find('h3',class_='fw-600 fs-13 text-truncate-2 lh-1-4 mb-0').a['href']
            image = article.find('div',class_='position-relative').img['data-src']
            tableau.append({"image":image,"price":price,"name":name,"src":image}) 
        return tableau
    except:
        return []

def scrapCoinAfrique(keyWord):
    URL = "https://sn.coinafrique.com/search?category=&keyword="+keyWord
    baseUrl="https://sn.coinafrique.com"
    #https://sn.coinafrique.com/categorie/mode-et-beaute
    try:         
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        jobs = soup.find_all('div',class_='col s6 m4 l3')
        for article in jobs:
            image = article.find('img',class_='ad__card-img')['src']
            more_info =  baseUrl+article.find('a',class_='card-image ad__card-image waves-block waves-light')['href']
            price = article.find('p',class_='ad__card-price').text
            name = article.find('p',class_='ad__card-description').text
            category= article.find('span',class_='btn-floating card-fav halfway-fab')['data-ad-category']
            tableau.append({"name":name,"image":image,"more_info":more_info,"price":price,"category":category})
        return tableau 
    except:
        return []
        

def scrapExpatDakar(keyWord):    
    URL = "https://www.expat-dakar.com/dernieres-annonces?txt="+keyWord
    baseUrl="https://www.expat-dakar.com"
    #https://www.expat-dakar.com/informatique-telecoms
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        jobs = soup.find_all('div',class_='listing-card')
        for article in jobs:
            image = article.find('img',class_='listing-card__image__resource vh-img')['src']
            more_info = article.find('a')['href']
            name = article.find('div',class_='listing-card__header__title').text.strip()
            try:            
                price = article.find('span',class_='listing-card__price__value').text.strip()
            except:
                price=''
            category = article.find('a')['data-t-listing_category_slug']
            tableau.append({"name":name,"image":image,"more_info":more_info,"price":price,'category':category})
        return  tableau
    except:
        return []

def scrapWellmah(keyWord):
    URL = "https://www.wellmah.com/?s="+keyWord+"&v=92666505ce75"
    #https://www.wellmah.com/boutique/electronique/?v=92666505ce75
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        jobs = soup.find_all('li',class_='ast-article-post')
        for article in jobs:
            name = article.find('h2',class_='woocommerce-loop-product__title').text
            more_info = article.find('div',class_='astra-shop-thumbnail-wrap').a['href']
            image = article.find('div',class_='astra-shop-thumbnail-wrap').img['src']
            price = article.find('span',class_='price').text.strip()
            tableau.append({"name":name,"image":image,"more_info":more_info,"price":price})
        return tableau
    except:
        return []
    
# Create your views here.
@csrf_exempt
def SearchApi(request,id=0):
    global tableau
    if request.method=='GET':
        word = request.GET.get('searchName', None)
        tableauRendered = scrapWellmah(word) 
        tableau = []
        print(word)
        return JsonResponse(tableauRendered, safe=False)  

    elif request.method=='POST':
        Search_data=JSONParser().parse(request)
        Search_serializer = SearchSerializer(data=Search_data)
        if Search_serializer.is_valid():
            # Search_serializer.save()
            word = Search_data["searchName"]
            #return JsonResponse(scrapmonster(word), safe=False) 
           # return JsonResponse([scrapmonster(word), scrapptimesjobs(word)], safe=False)
            tableauRendered = scrapJumia(word) 
            print(word)
            tableau = []
            return JsonResponse(tableauRendered, safe=False)
        return JsonResponse("Failed to Add.",safe=False)
    
    elif request.method=='PUT':
        Search_data = JSONParser().parse(request)
        Search=Searchs.objects.get(searchId=Search_data['searchId'])
        Search_serializer=SearchSerializer(Search,data=Search_data)
        if Search_serializer.is_valid():
            Search_serializer.save()
            return JsonResponse("Updated Successfully!!", safe=False)
        return JsonResponse("Failed to Update.", safe=False)

    elif request.method=='DELETE':
        Search=Searchs.objects.get(searchId=id)
        Search.delete()
        return JsonResponse("Deleted Succeffully!!", safe=False)
