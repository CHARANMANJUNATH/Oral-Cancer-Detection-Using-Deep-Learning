from flask import Flask,request, url_for, redirect, render_template
import pickle
import pandas as pd

from fastai import *
from fastai.vision import *


import os
from werkzeug.utils import secure_filename
#for toxic app
from flask import Flask, render_template, url_for, request, jsonify      
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer 
import pickle
import numpy as np
#from extract import exx
import glob
import shutil


PEOPLE_FOLDER = os.path.join('static', 'people_photo')
# Define a flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER



def model_predict(img_path,thr):
    """
       model_predict will return the preprocessed image
    """
    
    path=r"C:\FinalYear2023\OralCancerProjectFolderFinal"
    learn = load_learner(path)
    img = open_image(img_path)
    pred_class,pred_idx,outputs = learn.predict(img)
    result=int(pred_class)
    thr=float(outputs[result])
    thr=round(thr,4)
    return result,thr
    

#first file 
@app.route('/')
def hello_world():
    return render_template('page1.html') #file to upload the data



#second file
@app.route('/predict',methods=['POST','GET'])
def predict():
     #calculation of zone done

        
        
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        thr=0
        preds = model_predict(file_path,thr)
        print(preds)
        a=preds[0]
        b=preds[1]
        print(a)
        print(type(a))
        print(b)
        b=round(b,2)
        print(b)



        if a==0 and b>0.70:
            return render_template('hp.html',a="ORAL IMAGE-CLASS CANCER ")
        elif a==1 and b>0.70:
            return render_template('hp.html',a="ORAL IMAGE-CLASS NON-CANCER")
        elif a==2 and b>0.70:
            return render_template('hp.html',a="HISTOPATHOLOGICAL IMAGE-CLASS NORMAL")
        elif a==3 and b>0.70:
            return render_template('hp.html',a=" HISTOPATHOLOGICAL IMAGE-ORAL SQUAMOUS CELL CARCINOMA")
        else:
            return render_template('hp.html',a="Please upload a proper image")
		



    return None    

@app.route("/predicts", methods=['POST'])
def predicts():
    return render_template('page1.html', pred_tox = 'Prob (Toxic): {}'.format(out_tox))
if __name__ == '__main__':
    app.run(debug=True)

