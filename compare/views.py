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

# Script for scraping all categories in JUMIA website
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

# Script for scraping all Subcategories in jumia website
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

# Script for scraping all categories and Subcategories in Discount website
def scrapCatDiscount():
    tableau=[]
    URL = 'https://discount-senegal.com/'    
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser') 
        category = soup.find_all('li',class_='menu-item-object-product_cat')
        for cat in category:
            catName=cat.text
            catLink=cat.a['href']
            tableau.append({'catName':catName,'catLink':catLink})
    except:
        print("An error occured")
    result = []
    for cat in tableau:
        if cat not in result:
           result.append({'catName':cat['catName'],'catLink':cat['catLink']})

    return result


# Script for scraping all Categories in expat website
def scrapCatExpat():
        tableau=[]
        URL = 'https://www.expat-dakar.com/'    
        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser') 
            category = soup.find_all('div',class_='home-category')
            for cat in category:                
               catLink=cat.a['href']
               catName=cat.find('span',class_='home-category__header__title').text.strip()
               tableau.append({'catName':catName,'catLink':catLink})
        except Exception as e:
                trace_back = traceback.format_exc()
                message = str(e)+ " " + str(trace_back)
                print (message)
        result = []
        for cat in tableau:
           if cat not in result:
               result.append({'catName':cat['catName'],'catLink':cat['catLink']})
        return result

# Script for scraping all Subcategories in expat website
def scrapSubCatExpat():
        categories=scrapCatExpat()
        tableau=[]   
        try:
            for categoryEl in categories:
                page2 = requests.get(categoryEl['catLink'])
                soup2 = BeautifulSoup(page2.content, 'html.parser') 
                category2 = soup2.find_all('li',class_='filter__category-list-item')
                for cat in category2:
                    tableau.append({'catName':categoryEl['catName'],'subCatName':cat.a.text.strip(),'subCatLink':cat.a['href']})
        except Exception as e:
                    trace_back = traceback.format_exc()
                    message = str(e)+ " " + str(trace_back)
                    print (message)
        result = []
        for cat in tableau:
            if cat not in result:
                 result.append({'catName':cat['catName'],'subCatName':cat['subCatName'],'subCatLink':cat['subCatLink']})
        print(result)


# Script for scraping products in jumia website
def scrapJumia(keyWord):
    URL = 'https://www.jumia.sn/catalog/?q='+str(keyWord)
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
            tableau.append({"image":image,"price":price,"name":name,"src":src,"category":category}) 
        return tableau  
    except:
        return []


# Script for scraping products in senAchat website
def scrapSenAchat(keyWord):
    
    URL = "https://www.senachat.com/search?q="+keyWord
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


# Script for scraping products in coniAfrique website
def scrapCoinAfrique(keyWord):
    URL = "https://sn.coinafrique.com/search?category=&keyword="+keyWord
    baseUrl="https://sn.coinafrique.com"
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
        

# Script for scraping product in expat website
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


# Script for scraping products in wellmah website
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

def scraptDiscountSenegal():
    
    tableau=[]
    URL ='https://discount-senegal.com/categorie-produit/maison-et-deco/'
    try:
        page= requests.get(URL)
        soup=BeautifulSoup(page.content,'html.parser')
        products=soup.find_all('li',class_='product')
        for product in products:
            srcEl=product.find('div',class_='mf-product-thumbnail')
            src=srcEl.a['href']
            image=srcEl.a.img['src']
            infoEl=product.find('div',class_='mf-product-content')
            name= infoEl.h2.text
            priceEl=product.find('span',class_='price')
            price= priceEl.find('span',class_='woocommerce-Price-amount amount').text.strip()
            tableau.append({"image":image,"price":price,"name":name,"src":src,"category":''}) 
    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e)+ " " + str(trace_back)
        print (message)
    return tableau
    
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
