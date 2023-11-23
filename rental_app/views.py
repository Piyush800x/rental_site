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


def listing(request):
    return render(request, "listing.html")


def rental(request):
    return render(request, "rental.html")


def contact(request):
    return render(request, "contact.html")


def create_data(request):
    if request.user.is_authenticated:
        query = collection.find_one({"username": f"{request.user}"})
        print(query)
        if query is None:
            dic = {
                "username": f"{request.user}",
            }
            collection.insert_one(dic)

    print("Done")


def createproduct(request):
    if request.user.is_authenticated:
        data = {
            "name": f"{request.POST.get('name')}",
            "email": f"{request.POST.get('email')}"
        }
        update_data = collection.update_one(
            {"username": f"{request.user}"},  {'$push': {"listings": data}})
        print("Updated")

    return render(request, "create.html")
