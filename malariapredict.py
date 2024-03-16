import keras
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
from keras.layers import Dense
from keras.models import Sequential, load_model
from collections import Counter
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors
import cv2
custom_objects = {
    'BatchNormalization': keras.layers.BatchNormalization,
}
saved_model = load_model("model\F-Malaria.h5",compile=False,custom_objects=custom_objects)
status = True
def rgb_to_hex(rgb_color):
  hex_color="#"
  for i in rgb_color:
    i=int(i)
    hex_color+= ("{:02x}".format(i))

  return hex_color

def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)

  return tuple(rgb)

def x(hex):
  hex1=""
  for i in hex:
    if i!='#':
      hex1+=i

  return hex1
def checkmal(input_img):
        img_name=input_img
        print(img_name)
        img_name="static/images/"+img_name
        raw_img=cv2.imread(img_name)
        print(raw_img)
        raw_img=cv2.cvtColor(raw_img,cv2.COLOR_BGR2RGB)
        img=cv2.resize(raw_img,(900,600),interpolation=cv2.INTER_AREA)
        #img.shape

        img=img.reshape(img.shape[0]*img.shape[1],3)
        #img.shape

        #img

        clf=KMeans(n_clusters=15)
        color_labels=clf.fit_predict(img)
        center_colors=clf.cluster_centers_

        #color_labels

        #center_colors

        counts=Counter(color_labels)
        #counts

        ordered_colors=[center_colors[i] for i in counts.keys()]
        hex_colors=[rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
        colors=[]
        for i in range(len(hex_colors)):
            colors.append(x(hex_colors[i]))


        injury=[]
        status1=True
        for i in colors:
            t=hex_to_rgb(i)
            if (t[0]>=t[1]) and (t[0]>=t[2]):
                status1=status1 and True
            else :
                status1=status1 and False
            injury.append(t)
        return status1


def malar(input_img):
    global status  # Use the global status variable

    print("Your image is: " + input_img)
    img_name = "images/" + input_img

    # Load and preprocess the image
    img = image.load_img(img_name, target_size=(224, 224))
    img = image.img_to_array(img)
    img /= 255.0  # Normalize the image

    # Perform prediction using the loaded model
    img = np.expand_dims(img, axis=0)
    output = saved_model.predict(img)

    print(output)

    if output[0][1] >= 0.9:
        status = True
    else:
        status = False

    print(status)
    return status


