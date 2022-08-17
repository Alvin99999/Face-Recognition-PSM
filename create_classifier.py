import numpy as np
from PIL import Image
import os 
import cv2



# Method to train custom classifier to recognize face
def train_classifer(name):
    # Read all the images in custom dataset from current working directory and join various path
    path = os.path.join(os.getcwd()+"/data/"+name+"/")

    faces = [] #initialize empty face sample
    ids = []   #intialize empty id sample (list)
    pictures = {} #dictionary



    for root,dirs,files in os.walk(path):
            pictures = files


    for pic in pictures :

            imgpath = path+pic
            img = Image.open(imgpath).convert('L') #turn image to grayscale
            imageNp = np.array(img, 'uint8') #store the image in numpy array in uint8
            id = int(pic.split(name)[0]) #get the image name only and discard jpg
            #names[name].append(id)

            #add the faces to imageNp to faces
            faces.append(imageNp)
            #add the ID to IDs
            ids.append(id)

    ids = np.array(ids)

    #Train and create/save classifier with user name
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("./data/classifiers/"+name+"_classifier.xml")

