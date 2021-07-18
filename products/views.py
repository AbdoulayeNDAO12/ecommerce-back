from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import requests
from .serializers import ProductSerializer

# Create your views here.
    
# Create your views here.
@csrf_exempt
def ProductApi(request,id=0):
    if request.method=='GET':
       
        return JsonResponse({}, safe=False)  

    # elif request.method=='POST':
    #     Product_data=JSONParser().parse(request)
    #     Product_serializer = ProductSerializer(data=Product_data)
    #     if Product_serializer.is_valid():
            # Product_serializer.save()
            # word = Product_data["ProductName"]
            #return JsonResponse(scrapmonster(word), safe=False) 
           # return JsonResponse([scrapmonster(word), scrapptimesjobs(word)], safe=False)
        #     tableauRendered = scrapJumia(word) 
        #     print(word)
        #     tableau = []
        #     return JsonResponse(tableauRendered, safe=False)
        # return JsonResponse("Failed to Add.",safe=False)


