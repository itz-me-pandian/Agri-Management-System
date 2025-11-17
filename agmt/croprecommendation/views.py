from django.shortcuts import render
import pickle
import json
import os
from django.http import JsonResponse


map_data={}

def load_crop_recommendation_model():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "templates", "recommendation_model.pkl")

    with open(model_path, "rb") as file:
        recommendation_model= pickle.load(file)
    print("recommendation model loaded succesfull")

    t = float(map_data["temperature"])
    h = float(map_data["humidity"])
    r = float(map_data["rainfall"])

    n = float(map_data["nitrogen"])
    p = float(map_data["phosphorous"])
    k = float(map_data["potassium"])
    ph = float(map_data["ph"])

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
    return render(request,"map.html")

def save_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            temperature = data.get("temperature")
            humidity = data.get("humidity")
            rainfall = data.get("rainfall")
            nitrogen = data.get("nitrogen")
            phosphorous = data.get("phosphorus")
            potassium = data.get("potassium")
            ph = data.get("ph")
            '''
            nitrogen,
            phosphorus,
            potassium,
            ph
            '''

            print(f"Received Data: Temperature={temperature}, Humidity={humidity}, Rainfall={rainfall}")
            map_data["temperature"]=temperature
            map_data["humidity"]=humidity
            map_data["rainfall"]=rainfall
            map_data["nitrogen"]=nitrogen
            map_data["phosphorous"]=phosphorous
            map_data["potassium"]=potassium
            map_data["ph"]=ph

            recommend_crop(request)

            return JsonResponse({"message": "Data received", "temperature": temperature, "humidity": humidity, "rainfall": rainfall})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def recommend_crop(request):
    crop = load_crop_recommendation_model()
    print(crop)

    context = {
        'temperature': map_data['temperature'],
        'humidity': map_data['humidity'],
        'rainfall': map_data['rainfall'],
        'nitrogen': map_data['nitrogen'],
        'phosphorus': map_data['phosphorous'],
        'potassium': map_data['potassium'],
        'ph': map_data['ph'],
        'predicted_crop': crop
    }
    return render(request, 'recommendation_result.html', context)
    
