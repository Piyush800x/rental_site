from django.shortcuts import render
from rental_site.settings import DB_NAME
from pymongo.mongo_client import MongoClient
from django.core.files.storage import default_storage
from google.cloud import storage
from django.conf import settings
from bson.json_util import dumps

# Create your views here.

client = MongoClient(DB_NAME)
db = client['rentaldata']
collection = db['userdata']
placedata = db['placedata']


def home(request):
    create_data(request)
    return render(request, 'index.html')


def about(request):
    return render(request, "about.html")


def create(request):
    return render(request, "create.html")

def rent(request):
    return render(request, "rent.html")

def rental(request):
    # places = ["Kolkata", "Burdwan", "Ranaghat", "Kalyani", "Naihati", "Barrackpur", "Krishnanagar", "Burdwan",
    #           "Shantipur", "Nabadwip", "Mayapur"]
    # final_list = []
    # full_list = []
    # for i in range(len(places)):
    #     query = placedata.find({"place": places[i]})
    #     data_list = [result for result in query]
    #     for j in range(len(data_list)):
    #         # print(data_list[j].get("listings"))
    #         # final_list.append(data_list[j]["listings"])
    #         # print(data_list[j])
    #         # print(type(data_list[j]))
    #         final_list.append(data_list[j].get("listings"))
    # print("------------------")
    # print(final_list)

    # for i in range(len(final_list)):
    #     print(final_list[i])
    #     if final_list[i] != None:
    #         for j in range(len(final_list[i])):
    #             if final_list[i][j]:
    #                 full_list.append(final_list[i][j])
    #             else:
    #                 full_list.append(final_list[i])

    # print("*************************")
    # print(full_list[0])
    context = get_all(request)
    return render(request, "rental.html", {"context": context})


def get_all(request):
    places = ["Kolkata", "Burdwan", "Ranaghat", "Kalyani", "Naihati", "Barrackpur", "Krishnanagar", "Burdwan",
              "Shantipur", "Nabadwip", "Mayapur"]
    final_list = []
    full_list = []
    for i in range(len(places)):
        query = placedata.find({"place": places[i]})
        data_list = [result for result in query]
        for j in range(len(data_list)):
            # print(data_list[j].get("listings"))
            # final_list.append(data_list[j]["listings"])
            # print(data_list[j])
            # print(type(data_list[j]))
            final_list.append(data_list[j].get("listings"))
    print("------------------")
    print(final_list)

    for i in range(len(final_list)):
        print(final_list[i])
        if final_list[i] != None:
            for j in range(len(final_list[i])):
                if final_list[i][j]:
                    full_list.append(final_list[i][j])
                else:
                    full_list.append(final_list[i])

    print("*************************")
    print(full_list[0])

    return full_list

def search(request):
    place = request.POST.get("place")
    final_list = []
    full_list = []
    query = placedata.find({"place": place})
    data_list = [result for result in query]
    for j in range(len(data_list)):
            # print(data_list[j].get("listings"))
            # final_list.append(data_list[j]["listings"])
            # print(data_list[j])
            # print(type(data_list[j]))
        final_list.append(data_list[j].get("listings"))
    # print("------------------")
    # print(final_list)

    for i in range(len(final_list)):
        print(final_list[i])
        if final_list[i] != None:
            for j in range(len(final_list[i])):
                if final_list[i][j]:
                    full_list.append(final_list[i][j])
                else:
                    full_list.append(final_list[i])

    print("*************************")
    print(full_list[0])

    return render(request, "rental.html", {"context": full_list})

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
            "username": f"{request.user}",
            "name": f"{request.POST.get('name')}",
            "email": f"{request.POST.get('email')}",
            "address": f"{request.POST.get('address')}",
            "city": f"{request.POST.get('city')}",
            "house": f"{request.POST.get('house')}",
            "food": f"{request.POST.get('food')}",
            "cost": f"{request.POST.get('cost')}",
            "comments": f"{request.POST.get('comments')}",
            "image": f"{request.POST.get('image')}",    # need bucket
        }
        update_data = placedata.update_one(
            {"place": f"{request.POST.get('city')}"},  {'$push': {"listings": data}})
        print("Updated")

    return render(request, "create.html")

# def upload(request):
#     UploadView.as_view()


def upload_image(request):
    if request.method == 'POST' and request.POST.get('image'):
        image = request.POST.get('image')
        print("---------------")
        print(image)
        print(type(image))
        blob_name = f"images/{image}"  # Define the blob name within the bucket

        # Upload the image to Google Cloud Storage
        client = storage.Client.from_service_account_json(
            settings.GOOGLE_APPLICATION_CREDENTIALS)
        bucket = client.get_bucket(settings.GOOGLE_CLOUD_STORAGE_BUCKET_NAME)
        blob = bucket.blob(blob_name)

        # Check if 'image' is a file path or an opened file
        if isinstance(image, str):
            # 'image' is a file path, open and read the file
            with open(image, 'rb') as file:
                blob.upload_from_file(file)
        else:
            # 'image' is already an opened file, use its content directly
            blob.upload_from_file(image)

        # Get the public URL of the uploaded image
        public_url = f"https://storage.googleapis.com/{settings.GOOGLE_CLOUD_STORAGE_BUCKET_NAME}/{blob_name}"
        print("--------------------")
        print(public_url)
        return render(request, 'create.html')

    return render(request, 'create.html')
