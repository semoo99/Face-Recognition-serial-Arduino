import cv2
from faceopen import start_training, predict_face
from logging import PlaceHolder
import numpy as np
import os
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import uuid
import light


ikkuna=tkinter.Tk()
ikkuna.title("Example about handy CV2 and tkinter combination...")

frame=np.random.randint(0,255,[100,100,3],dtype='uint8')
img = ImageTk.PhotoImage(Image.fromarray(frame))

paneeli_image=tkinter.Label(ikkuna) #,image=img)
paneeli_image.grid(row=0,column=0,columnspan=3,pady=1,padx=10)

message="1-take Image \n 2-traning new image \n 3-take photo"
paneeli_text=tkinter.Label(ikkuna,text=message)
paneeli_text.grid(row=2,column=1,pady=1,padx=10)

global cam

def otakuva():
    global frame
    global cam
    cam = cv2.VideoCapture(0)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")

    #cv2.namedWindow("Experience_in_AI camera")
    while True:
        ret, frame = cam.read()

        #Update the image to tkinter...
        if not ret:
            print("failed to grab frame")
            break

        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        faces = faceCascade.detectMultiScale(
                                    frame,
                                    scaleFactor=1.1,
                                    minNeighbors=5,
                                    minSize=(30, 30),
                                    )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y),
                    (x+w, y+h), (0, 255, 0), 2)

        frame = cv2.resize(frame, (800,500))
        img_update = ImageTk.PhotoImage(Image.fromarray(frame))
        paneeli_image.configure(image=img_update)
        paneeli_image.image=img_update
        paneeli_image.update()


        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")

            cam.release()
            cv2.destroyAllWindows()
            break

def lopeta():
    global cam
    cam.release()
    cv2.destroyAllWindows()
    print("Stopped!")

def take_image():
    name = nametxt.get(1.0, "end-1c")
    if not os.path.isdir('images'):
        os.mkdir('images')
    if len(name)<5 :
        paneeli_text.configure(text='Write the name ')
    else:
        name_path = os.path.join('images',name)
        if not os.path.isdir(name_path):
            os.mkdir(name_path)
        
        ret, framen = cam.read()
        cv2.imwrite(os.path.join('images',name,f'{uuid.uuid4().hex[:7]}.jpg'), framen)

        paneeli_text.configure(text="Click save after you finish") 

def train_new():
    try:
        paneeli_text.configure(text="Wait to be ready") 
        start_training()
        paneeli_text.configure(text="ready to use") 
    except Exception as err:
        paneeli_text.configure(text="Error \n Check images train") 
        print(str(err))

def opendoor():
    try:
        ret, framen = cam.read()
        cv2.imwrite(os.path.join('images','person.jpg'), framen)
        conf, name = predict_face()
        if conf < 60 :
            paneeli_text.configure(text=f"Welcome {name}\n conf{conf}")
            light.led_on(True)
        else:
            paneeli_text.configure(text=f"Sorry try again\n conf{conf}")

    except:
        paneeli_text.configure(text="Error \n Check images") 

    pass

namelbl = tkinter.Label(ikkuna, text="Person Name",  height=3, width=20,)
namelbl.grid(row=1,column=0,pady=10,padx=10)
nametxt = tkinter.Text(ikkuna, height=3, width=20,)
nametxt.grid(row=1,column=1,pady=10,padx=10)

painike_korkeus=5
painike_0=tkinter.Button(ikkuna,text="start",command=otakuva,height=5,width=20)
painike_0.grid(row=2,column=0,pady=10,padx=10)
painike_0.config(height=1*painike_korkeus,width=20)

# painike_korkeus=10
painike_1=tkinter.Button(ikkuna,text="Stop",command=lopeta,height=5,width=20)
painike_1.grid(row=2,column=2,pady=10,padx=10)
painike_1.config(height=1*painike_korkeus,width=20)

painike_2=tkinter.Button(ikkuna,text="take",command=take_image, height=5, width=20)
painike_2.grid(row=3,column=0,pady=10,padx=10)

painike_3=tkinter.Button(ikkuna,text="Save Images",command=train_new, height=5, width=20)
painike_3.grid(row=3,column=1,pady=10,padx=10)

painike_4=tkinter.Button(ikkuna,text="open",command=opendoor, height=5, width=20)
painike_4.grid(row=3,column=2,pady=10,padx=10)


ikkuna.mainloop()