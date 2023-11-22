from django.shortcuts import render
from rental_site.settings import DB_NAME
from pymongo.mongo_client import MongoClient

# Create your views here.

client = MongoClient(DB_NAME)
db = client['rentaldata']
collection = db['userdata']


def home(request):
    create_data(request)
    return render(request, 'index.html')


def about(request):
    return render(request, "about.html")


def create(request):
    return render(request, "create.html")


def create_data(request):
    if request.user.is_authenticated:
        print(request.user)
