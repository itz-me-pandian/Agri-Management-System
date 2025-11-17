import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import cv2


def fun(image_path):
    #image_path = "Any Plant Leaf Path if you want to test locally"
    model=tf.keras.models.load_model("./static/images/trained_model.keras")
    image=tf.keras.preprocessing.image.load_img(image_path,target_size=(128,128))
    input_arr=tf.keras.preprocessing.image.img_to_array(image)
    input_arr=np.array([input_arr])
    prediction=model.predict(input_arr)
    result_index=np.argmax(prediction)
    class_name=['Apple Scab', 'Black Rot (Apple)', 'Cedar Apple Rust', 'Apple (Healthy)', 'Blueberry (Healthy)', 'Powdery Mildew (Cherry)', 'Cherry (Healthy)', 'Cercospora Leaf Spot (Corn)', 'Common Rust (Corn)', 'Northern Leaf Blight (Corn)', 'Corn (Healthy)', 'Black Rot (Grape)', 'Esca (Black Measles)', 'Leaf Blight (Grape)', 'Grape (Healthy)', 'Haunglongbing (Citrus Greening)', 'Bacterial Spot (Peach)', 'Peach (Healthy)', 'Bacterial Spot (Pepper)', 'Pepper (Healthy)', 'Early Blight (Potato)', 'Late Blight (Potato)', 'Potato (Healthy)', 'Raspberry (Healthy)', 'Soybean (Healthy)', 'Powdery Mildew (Squash)', 'Leaf Scorch (Strawberry)', 'Strawberry (Healthy)', 'Bacterial Spot (Tomato)', 'Early Blight (Tomato)', 'Late Blight (Tomato)', 'Leaf Mold (Tomato)', 'Septoria Leaf Spot (Tomato)', 'Spider Mites (Tomato)', 'Target Spot (Tomato)', 'Tomato Yellow Leaf Curl Virus', 'Tomato Mosaic Virus', 'Tomato (Healthy)']
    model_prediction=class_name[result_index]
    print(model_prediction)
    return model_prediction
