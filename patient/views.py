from django.db.models.fields import DateField
from patient.models import log, patient
from django.shortcuts import render
from django.db.models import F, Max
import datetime

import pandas as pd
import numpy as np

import plotly.express as px
from plotly.offline import plot

def patient(request):
    #filter the data for currently login user
    patientLog = log.objects.filter(patient__doctor=request.user)
    #filter the date must be the same with the latest appointment
    patientrecent = patientLog.filter(date = F('patient__appointment'))
    #get the latest date in the log model
    latest_date = patientLog.latest('date').date
    #filter the
    patient_latest = patientLog.filter(date = latest_date)

    name = []
    for item in patientLog:
        name.append(item.patient.full_name)
    
    ldl = []
    for item1 in patientLog:
        ldl.append(float(item1.ldl.ldl))
    
    tc = []
    for item2 in patientLog:
        tc.append(float(item2.tc.total_cholesterol))
    
    hdl = []
    for item3 in patientLog:
        hdl.append(float(item3.hdl.hdl))
    
    tg = []
    for item4 in patientLog:
        tg.append(float(item4.tg.tg))

    date= []
    for item3 in patientLog:
        date.append(item3.date)
    

    

    #store patient detail in dataframe
    dict_pt = {'name':name, 'date':date, 'LDL':ldl, 'Total Cholesterol':tc, 'HDL':hdl, 'Triglyceride level': tg}
    df_pt = pd.DataFrame(dict_pt, columns=['name','date', 'LDL', 'Total Cholesterol', 'HDL', 'Triglyceride level'])
    df_sorted = df_pt.sort_values(by='date', ascending=False)
    dfinfo = df_pt.sort_values('date').groupby('name').tail(1)
    info = dfinfo.to_html(classes="table table-dark table-hover")

    fig1 = px.line(df_sorted, x= 'date', y='LDL', color='name', line_group='name', hover_name='name')
    fig1.update_layout(title='LDL-C Level for All Patient')
    plot_fig1 = plot({'data': fig1}, output_type='div')

    fig2 = px.line(df_sorted, x= 'date', y='Total Cholesterol', color='name', line_group='name', hover_name='name')
    fig2.update_layout(title='Total Cholesterol level for All Patient')
    plot_fig2 = plot({'data': fig2}, output_type='div')

    fig3 = px.line(df_sorted, x= 'date', y='HDL', color='name', line_group='name', hover_name='name')
    fig3.update_layout(title='HDL-C Level for All Patient')
    plot_fig3 = plot({'data': fig3}, output_type='div')

    fig4 = px.line(df_sorted, x= 'date', y='Triglyceride level', color='name', line_group='name', hover_name='name')
    fig4.update_layout(title='Triglyceride Level for All Patient')
    plot_fig4 = plot({'data': fig4}, output_type='div')

    context = {'patientinfo':info, 'patientrecent': patientrecent, 'patient_latest':patient_latest, 'figure':plot_fig1, 'figure2':plot_fig2, 'figure3':plot_fig3, 'figure4':plot_fig4}
    return render(request, 'patient/patient.html', context)

def edit(request, name, id):
    #filter the log table with patient name
    obj = log.objects.filter(patient__full_name = name)

    #iterate to obtain the patient name that need to be passed to <title>
    for item in obj:
        title=item.patient.full_name
    
    #list to store queryset result
    date = []
    for y in obj:
        date.append(y.date)

    ldl = []
    for x in obj:
        ldl.append(float(x.ldl.ldl))

    tc = []
    for k in obj:
        tc.append(float(k.tc.total_cholesterol))

    hdl = []
    for i in obj:
        hdl.append(float(i.hdl.hdl))

    tg = []
    for j in obj:
        tg.append(float(j.tg.tg))

    #combine two list to one dict
    dict_ldl = {'date':date, 'LDL (mmog/L)': ldl}
    dict_tc = {'date': date, 'Total Cholesterol (mmog/L)': tc}
    dict_hdl = {'date':date, 'HDL (mmog/L)':hdl}
    dict_tg = {'date':date, 'Triglycerides Level (mmog/L)':hdl}

    df_ldl = pd.DataFrame(dict_ldl, columns=['date', 'LDL (mmog/L)'])
    dataldl = df_ldl.sort_values(by='LDL (mmog/L)', ascending=False)

    df_tc = pd.DataFrame(dict_tc, columns=['date', 'Total Cholesterol (mmog/L)'])
    datatc = df_tc.sort_values(by='Total Cholesterol (mmog/L)', ascending=False)

    df_hdl = pd.DataFrame(dict_hdl, columns=['date', 'HDL (mmog/L)'])
    datahdl = df_hdl.sort_values(by='HDL (mmog/L)', ascending=False)

    df_tg = pd.DataFrame(dict_tg, columns=['date', 'Triglycerides Level (mmog/L)'])
    datatg = df_tg.sort_values(by='Triglycerides Level (mmog/L)', ascending=False)

    #declare variable for figure
    fig1 = px.area(dataldl, x='date', y="LDL (mmog/L)")
    #variable that need to be pass as context
    plot_div1 = plot({'data': fig1}, output_type='div')

    fig2 = px.area(datatc, x='date', y="Total Cholesterol (mmog/L)")
    plot_div2 = plot({'data': fig2}, output_type='div')

    fig3 = px.area(datahdl, x='date', y="HDL (mmog/L)")
    plot_div3 = plot({'data': fig3}, output_type='div')

    fig4 = px.area(datatg, x='date', y="Triglycerides Level (mmog/L)")
    plot_div4 = plot({'data': fig4}, output_type='div')

    context = {'plot_div1': plot_div1, 'plot_div2':  plot_div2, 'plot_div3':plot_div3, 'plot_div4':plot_div4, 'title':title}
    return render(request, 'patient/graph.html', context)