from django.shortcuts import render, redirect
from django.urls import reverse
import io
import json

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from imblearn.over_sampling import ADASYN   

def prediction(request):
    return render(request, 'prediction/diagnosis.html')

def homepage(request):
    return redirect(reverse("authorize:homepage"))

def result(request):
    #read file from local folder
    data = pd.read_csv("D:\Fyp\data\FH 5248_DLCC_diagnosis.csv")

    X = data.drop(['Order', 'Gender', 'Ethnic','On_LLT', 'Family_Hypercholesterolaemia', 'DLCC_Diagnosis'], axis = 1)
    y = data['DLCC_Diagnosis'] 

    X_train, X_test, Y_train, y_test = train_test_split(X, y,test_size = 0.30, random_state=0)

    oversampler = ADASYN(random_state=0)
    osfeature, oslabel = oversampler.fit_resample(X_train, Y_train)

    clf = RandomForestClassifier(random_state=0)
    clf.fit(osfeature, oslabel)

    age = request.GET['v1']
    personal_PCAD = request.GET['v10']
    personal_PVA_PVD = request.GET['v14']
    baseline_LDL = request.GET['v2']
    TC = request.GET['v3']
    TG = request.GET['v4']
    HDL = request.GET['v5']
    smoking = request.GET['v8']
    diabetes = request.GET['v12']
    family_PCAD = request.GET['v13']
    family_FH = request.GET['v9']
    tendon_xanthoma = request.GET['v7']
    corneal_arcus = request.GET['v11']

    pred = clf.predict(np.array([age, personal_PCAD, personal_PVA_PVD, baseline_LDL, TC, TG, HDL, 
    smoking, diabetes, family_PCAD, family_FH, tendon_xanthoma, corneal_arcus]).reshape(1, -1))
    ##pred = round(pred[0])
    display = str(pred)
    if(pred ==  [0] ):
        display = "unlikely"
    elif(  pred  ==  [1] ):
        display = "probable"
    elif(  pred  == [2] ):
        display = "possible"
    elif( pred  ==  [3]):
        display = "definite"

    dresult = "The diagnosis result for this patient is "+ display
    return render(request, 'prediction/diagnosis.html', {"result2":dresult})

def batch(request):
    upload = request.FILES['csv_file']
    csv_file = pd.read_csv(io.StringIO(upload.read().decode('utf-8')), delimiter=',')
    data = pd.read_csv("D:\Fyp\data\FH 5248_DLCC_diagnosis.csv")

    X = data.drop(['Order', 'Gender', 'Ethnic','On_LLT', 'DLCC_Diagnosis'], axis = 1)
    y = data['DLCC_Diagnosis'] 

    X_train, X_test, Y_train, y_test = train_test_split(X, y,test_size = 0.30, random_state=0)

    oversampler = ADASYN(random_state=0)
    osfeature, oslabel = oversampler.fit_resample(X_train, Y_train)

    clf = RandomForestClassifier(random_state=0)
    clf.fit(osfeature, oslabel)

    pred = clf.predict(csv_file)

    pred1 = []
    for x in pred:
        if x == 0:
            pred1.append('unlikely')
        elif x == 1:
            pred1.append('probable')
        elif x == 2:
            pred1.append('possible')
        elif x == 3:
            pred1.append('definite')

    detail = []
    k = 0
    for i in pred:
        k+=1
        detail.append('patient ' + str(k))

    dict_detail = {'patient':detail, 'diagnosis':pred1}

    df_detail = pd.DataFrame(dict_detail, columns=['patient', 'diagnosis'])
    
    #parsing the dataframe in json format
    json_records = df_detail.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)


    from collections import Counter
    #convert to dict with the prediction output as key
    count_dict = dict(Counter(pred1))
    #convert from dict to pandas dataframe
    result1 = pd.DataFrame(list(count_dict.items()), columns = ['result', 'count'])

    import plotly.express as px
    from plotly.offline import plot
    import plotly.graph_objects as go

    fig = px.bar(result1, x='result', y='count', color='result')
    plot_div = plot({'data': fig}, output_type='div')

    return render(request, 'prediction/diagnosis.html', context={"plot_div":plot_div, "detail":data})