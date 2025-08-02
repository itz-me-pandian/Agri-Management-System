import datetime
import os
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
import numpy as np
import tensorflow as tf
from . import modelTest
from .models import Remedy,User
import random
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .Remedy_populate import createRemedy as cr
from django.conf import settings
import requests
import pandas as pd
import json
from .models import Remedy
from django.shortcuts import render
import requests
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
#import joblib
#import pickle
#import io
#from PIL import Image, UnidentifiedImageError

def home(request):
    return render(request,"myapp/index.html",{})


def detect_disease(image_path):
    if not os.path.exists(image_path):
        return HttpResponse("Image file not found.", status=404)
    
    else:
        image=tf.keras.preprocessing.image.load_img(image_path,target_size=(128,128))
        input_arr=tf.keras.preprocessing.image.img_to_array(image)
        input_arr=np.array([input_arr])
        print(image_path)
        disease=modelTest.fun(image_path)
        disease_info = read(disease)
        
        data = {
        "dname": disease_info[0],
        "dcause": disease_info[1],
        "dtype": disease_info[2],
        "dremedy": disease_info[3] }

        print(input_arr.shape)
        #createRemedy()
        context = {
        "image_url": image_path, 
        "predicted_disease": disease,
        "data": data }

        return context
    
    '''else:
        try:
            # Read image into memory
            image_bytes = image_file.read()
            image = Image.open(io.BytesIO(image_bytes))
            image.verify()  # Ensure it is a valid image

            # Reset file pointer
            image_file.seek(0)

            # Load and preprocess image
            image = tf.keras.preprocessing.image.load_img(io.BytesIO(image_bytes), target_size=(128, 128))
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr])

            print("Image shape:", input_arr.shape)

            # Call your ML model
            disease = modelTest.fun(io.BytesIO(image_bytes))  # Ensure your model can handle `io.BytesIO`
            disease_info = read(disease)

            data = {
            "dname": disease_info[0],
            "dcause": disease_info[1],
            "dtype": disease_info[2],
            "dremedy": disease_info[3],
            }

            context = {
            "image_url": image_file.name,  # Keep track of the file name
            "predicted_disease": disease,
            "data": data,
            }
            return context

        except UnidentifiedImageError:
                return {"error": "Invalid image file. Please upload a valid image."}
        except Exception as e:
                return {"error": f"Error processing image: {str(e)}"}'''

def show_remedy(request):
    if request.method == "POST":
        disease_name = request.POST.get("dname")
        # Fetch remedy from database (assuming you have a model for it)
        disease = Remedy.objects.get(dname=disease_name)
        return render(request, "myapp/remedy.html", {"data": disease})


def populate_remedy():
    cr(1)
    
def read(disease):
    data=Remedy.objects.get(dname=disease)
    return data.dname,data.dcause,data.dtype,data.dremedy


'''My Work'''

# function for fetching the otp and verifying the otp and then storing the user details in the database
def otp_verify(request):
    otp1=request.POST.get('otp1')
    otp2=request.POST.get('otp2')
    otp3=request.POST.get('otp3')
    otp4=request.POST.get('otp4')
    votp=otp1+otp2+otp3+otp4
    uotp=request.session.get('otp')
    vuname = request.session.get('vuname')
    print(uotp,votp)
    if(votp==uotp):
        vuid = request.session.get('vuid')
        vuname = request.session.get('vuname')
        vuemail = request.session.get('vuemail')
        vupass = request.session.get('vpass')
        us=User(id=vuid,uname=vuname,upass=vupass,uemail=vuemail);
        us.save()
        send_mail(
                'Password for login',
                f'Hi {vuname},\n\nYour details are verified, please use the following Password for login\n\nPassword:{vupass}\n\nPlease reach out us for any Queries\n\nThank You.',
                'alloteasyregofficial@gmail.com',
                [vuemail],
                fail_silently=True,
            )
        messages.error(request, 'Successfully Registered ! ')
        messages.error(request, 'See your email for login details !!')
        return render(request,'myapp/login.html',{'messages':messages.get_messages(request),'user':vuname})
    else:
        messages.error(request, 'Enter correct OTP !!')
        return render(request,'myapp/otp.html',{'messages':messages.get_messages(request),'user':vuname})


# function for caling login template for user
def login(request):
    return render(request,"myapp/login.html",{'messages':messages.get_messages(request)})


# function for verifying the login credentials with the existing data in the database (user)
def login_check(request):
    if request.method == 'POST':
        id=request.POST.get('contact_number')
        uname = request.POST.get('name')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(id=id)

        except User.DoesNotExist:
            print('Invalid Username!!!')
            messages.error(request, "Username Doesn't exist !")
            return render(request,"myapp/login.html",{'messages': messages.get_messages(request)})
        
        except ValueError:
            messages.error(request, 'Invalid user ID format !')
            return redirect('login')
        
        print(user.upass,user.uname,password,uname)
        
        if user.upass==password and user.uname==uname:
            user1=User.objects.get(id=id)
            print(user.upass,user.uname,password,uname)
            return render(request,"myapp/viewprofile.html",{'user':user1})
        else:
            print('Invalid Password!!!')
            messages.error(request, 'Invalid username or password !!')
            return render(request,"myapp/login.html",{'messages': messages.get_messages(request)})
    else:
        return redirect('login')
    

# function for calling the user registration template 
def userreg(request):
    return render(request,"myapp/userreg.html",{})

# function for getting new user details from the template and sending otp to the registered mail 
def insertuser(request):
    vuid = request.POST.get('tuid')
    vuname = request.POST.get('tuname')
    vuemail = request.POST.get('tuemail')
    vpass=request.POST.get('tpassword')
    vconpass=request.POST.get('tconfirmpassword')

    try:
        us=User.objects.get(id=vuid)
        Us=User(id=vuid,uname=vuname,upass=vpass)
       
        messages.error(request, 'Already registered with the same contact number !')
        return render(request,'myapp/userreg.html',{'messages':messages.get_messages(request)})

    except:
        otp=str(random.randint(1000,9999))
        request.session['otp']=otp
        request.session['vuid']=vuid
        request.session['vuname']=vuname
        request.session['vuemail']=vuemail
        request.session['vpass']=vpass

        send_mail(
                    'OTP for Validating',
                    f'To complete your verification, please use the following OTP\n\nOTP:{otp}\n\nThis OTP is valid for 10 minutes.\n\nPlease do not share this OTP with anyone for security reasons.\n\nIf you did not request this OTP or have any concerns, ignore this mail.',
                    'alloteasyregofficial@gmail.com',
                    [vuemail],
                    fail_silently=False,
                )
        print("OTP has been sent Successfully!")
        return render(request,"myapp/otp.html",{'user':vuname})

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        upload_dir = os.path.join(os.getcwd(), 'UploadedImages')  # Specifing the directory inside the current working directory

        os.makedirs(upload_dir, exist_ok=True)           # Creating the directory if it doesn't exist

        fs = FileSystemStorage(location=upload_dir)      # Saving the image using FileSystemStorage
        name, ext = os.path.splitext(image.name)
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")  # Generating a unique filename with date & time (format: YYYYMMDD_HHMMSS)
        new_filename = f"{name}_{timestamp}{ext}"
        filename = fs.save(new_filename, image)  
        image_path = os.path.join(upload_dir, filename)  # Getting full path of saved image

        context = detect_disease(image_path)             # Passing image_path to detect_disease

        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "UploadedImages"))
        filename = fs.save(new_filename, image)

        image_url = f"{settings.MEDIA_URL}UploadedImages/{filename}"

        context["image_url"] = image_url

        return render(request, "myapp/disease_result.html", context)
    
    return JsonResponse({'error': 'No image uploaded'}, status=400)

def getImage(request):
    return render(request,"myapp/imageinput.html",{})


# Define the API URL (replace with an actual working API endpoint if available)
API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?format=json&api-key=579b464db66ec23bdd000001fbdefd9819584455608a9f1f1c1126ac&limit=1000"

def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data")
        return None

def process_data(data, selected_items):
    records = data.get("records", [])
    df = pd.DataFrame(records)

    # Convert price values to numeric
    df["modal_price"] = pd.to_numeric(df["modal_price"], errors='coerce') / 100

    # Extract month and year from date
    df["date"] = pd.to_datetime(df["arrival_date"], dayfirst=True)
    df["month"] = df["date"].dt.strftime("%b")  # Short month names (Jan, Feb, ...)
    df["year"] = df["date"].dt.year

    # Filter data for the latest available year and selected items
    latest_year = df["year"].max()
    df = df[(df["year"] == latest_year) & (df["commodity"].isin(selected_items))]
    return df

def plot_data(df, selected_items):
    plt.figure(figsize=(10, 6))

    # Get the latest date in the dataset
    latest_date = df["date"].max()
    print(latest_date)

    # Filter data for the latest date and selected items
    df_latest = df[(df["date"] == latest_date) & (df["commodity"].isin(selected_items))]

    # Group by commodity and calculate the average price
    avg_prices = df_latest.groupby("commodity")["modal_price"].mean()

    # Ensure all selected items are included, even if missing in data
    avg_prices = avg_prices.reindex(selected_items, fill_value=0)  # Fill missing ones with 0

    # Plot bar graph
    avg_prices.plot(kind="bar", color=["red", "orange", "purple", "green", "yellow"])

    # Labels and title
    plt.xlabel("Commodity")
    plt.ylabel("Average Modal Price Per Kg(₹)")
    plt.title(f"Price Comparison for Selected Commodities on {latest_date.strftime("%d-%m-%Y")}")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    for index, value in enumerate(avg_prices):
        plt.text(index, value + 0.5, f"{value:.2f}", ha="center", fontsize=12, fontweight="bold")

    # Save the plot to a static file
    static_folder = os.path.join(os.getcwd(), "detector", "static","images")
    os.makedirs(static_folder, exist_ok=True)  # Create the directory if it doesn't exist
    save_path = os.path.join(static_folder, "commodity_prices.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def price_visualization(request):
    # Retrieve selected commodities from the session
    selected_commodities = request.session.get('selected_commodities', [])
    print("Selected Commodities in Visualization:", selected_commodities)  # Debugging

    if not selected_commodities:
        return HttpResponseBadRequest("No commodities selected.")

    # Fetch and process data
    data = fetch_data()
    if data:
        processed_df = process_data(data, selected_commodities)
        plot_data(processed_df, selected_commodities)

    # Pass the selected commodities to the template
    context = {
        'selected_commodities': selected_commodities,
        'image_path': 'detector/static/commodity_prices.png'  # Path to the saved image
    }
    return render(request, 'myapp/price_visualization.html', context)

def get_commodities(request):
    commodities = [
        "Banana", "Black Gram Dal (Urd Dal)", "Maize", "Castor Seed", "Cabbage",
        "Ginger(Green)", "Cotton", "Bhindi(Ladies Finger)", "Carrot", "Beetroot",
        "Bottle gourd", "Jack Fruit", "Grapes", "Apple", "Capsicum", "Gram Raw(Chholia)",
        "Mango", "Onion", "Potato", "Apple"
    ]

    return render(request, 'myapp/commodities_selection.html', {'commodities': commodities})


from django.http import JsonResponse
from django.shortcuts import redirect
import json

def handle_selected_commodities(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            selected_commodities = data.get('selectedCommodities', [])  # Retrieve selected values
            print("Received Selected Commodities:", selected_commodities)  # Debugging

            # Store selected commodities in the session
            request.session['selected_commodities'] = selected_commodities
            request.session.modified = True  # Force session update

            # Debugging: Verify session storage
            print("Session After Storing:", request.session.get('selected_commodities', []))

            # Redirect to the price_visualization view
            return JsonResponse({
                'status': 'success',
                'redirect_url': '/visualize/'  # Redirect URL for the frontend
            })
        except Exception as e:
            print("Error:", str(e))  # Debugging
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)