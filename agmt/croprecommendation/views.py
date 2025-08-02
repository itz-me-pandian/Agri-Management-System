from urllib import request
from django.shortcuts import render
import pickle
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
thr_data={}

def load_crop_recommendation_model():
    with open("C:/Users/pandi/OneDrive - SSN-Institute/SEP_Project/demo1/agmt/croprecommendation/templates/recommendation_model.pkl", "rb") as file:
        recommendation_model= pickle.load(file)
    print("recommendation model loaded succesfull")

    t = thr_data["temperature"]
    h = thr_data["humidity"]
    r = float(thr_data["rainfall"])

    n = 35
    p = 66
    k = 81
    ph = 6.13

    test = [[n,p,k,t,h,ph,r]]
    print(test)

    prediction = recommendation_model.predict(test)
    
    label = [
            'rice','maize','chickpea','kidneybeans','pigeonpeas','mothbeans','mungbean','blackgram','lentil','pomegranate','banana','mango','grapes',
            'watermelon','muskmelon','apple','orange','papaya','coconut','cotton','jute','coffee'
        ]
    
    print(prediction[0])
    return label[prediction[0]]

def map(request):
    return render(request,"mapData.html")

def save_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            temperature = data.get("temperature")
            humidity = data.get("humidity")
            rainfall = data.get("rainfall")

            print(f"Received Data: Temperature={temperature}, Humidity={humidity}, Rainfall={rainfall}")
            thr_data["temperature"]=temperature
            thr_data["humidity"]=humidity
            thr_data["rainfall"]=rainfall

            recommend_crop()

            return JsonResponse({"message": "Data received", "temperature": temperature, "humidity": humidity, "rainfall": rainfall})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def recommend_crop():
    crop = load_crop_recommendation_model()
    print(crop)