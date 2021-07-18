from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import CategorySerializer

# Create your views here.
    
# Create your views here.
@csrf_exempt
def CategoryApi(request,id=0):
    if request.method=='GET':
       
        return JsonResponse({}, safe=False)  