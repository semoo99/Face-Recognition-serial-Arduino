import numpy as np
import cv2
import os
import json



def detect_face(img_path):
    """
    input image path

    """
    img = cv2.imread(img_path)
    face_detector_path = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +face_detector_path)
    detected_faces = faceCascade.detectMultiScale(img, 1.1, 5)
    try:
        x, y, w, h = detected_faces[0] #focus on the 1st face in the image
    except:
        return []
    img = img[y:y+h, x:x+w] #focus on the detected area
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    return img

def cut_faces():
    personsdir = os.listdir('images')
    print(personsdir)
    faces = []
    persons = {}
    id =0
    for img_dir in personsdir:
        try:
            img_files =os.listdir(os.path.join('images',img_dir))
        except:
            continue
        for img_path in img_files :
            if not img_path.endswith(('.jpg','.jpeg','.png')):
                continue
            print(id,img_dir, img_path)
            img = detect_face(os.path.join('images',img_dir, img_path))
            if len(img)==0:
                continue
            faces.append(img)
            persons[id] = img_dir
            id+=1
    with open('allawed.json', 'w') as outfile:

        json.dump(persons, outfile)

    return np.arange(len(faces)), faces


def start_training():
    print('start')
    model = cv2.face.LBPHFaceRecognizer_create() #Local Binary Patterns Histograms
    pre_built_model = "pre-built-model.yml"
    ids, faces = cut_faces()
    model.train(faces, ids)
    model.save(pre_built_model)


def predict_face():
    model = cv2.face.LBPHFaceRecognizer_create()
    pre_built_model = "pre-built-model.yml"
    model.read(pre_built_model)
    target_file = os.path.join('images','person.jpg')
    img = detect_face(target_file)

    id,conf=model.predict(img)
    
    with open('allawed.json') as allawed:
        names= json.load(allawed)

    with open('logs.txt','a') as loggsfile :
        loggsfile.write(f"{id}, {conf},{names[str(id)]}\n")
    return (conf, names[str(id)])