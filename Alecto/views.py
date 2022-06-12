from random import Random
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm  
from pathlib import Path
import pandas as pd 
import os
import mimetypes
import json
from sklearn.ensemble import RandomForestClassifier
import joblib

cols = ['kepid', 'tce_plnt_num', 'tce_rogue_flag', 'tce_period','tce_period_err', 'tce_time0bk', 'tce_time0bk_err', 'tce_impact','tce_impact_err', 'tce_duration', 'tce_duration_err', 'tce_depth','tce_depth_err', 'tce_model_snr', 'tce_prad', 'tce_prad_err', 'tce_eqt','tce_eqt_err', 'tce_insol', 'tce_insol_err', 'tce_steff','tce_steff_err', 'tce_slogg', 'tce_slogg_err', 'tce_sradius', 'tce_sradius_err']



def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        document = request.FILES['document']
        global df 
        df = pd.read_csv(document)
        global df2
        df2 = df
        json_records = df.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_records)
        data2 = data[0:8]
        rf = RandomForestClassifier()
        rf = joblib.load(r"model-1_joblib")
        X = df.drop(['tce_plnt_num', 'tce_rogue_flag', 'kepid', 'tce_insol', 'tce_insol_err', 'tce_duration_err', 'tce_eqt_err', 'tce_sradius_err', 'tce_slogg_err'], axis='columns')
        y = rf.predict(X)
        df2['av_column'] = y
        return render(request, 'result.html', {'dataframe': data2, 'cols':cols})
    else:
        form = UploadFileForm()
    return render(request, 'home.html', {'form': form})

def classify(request):
    return render(request, "classify.html")

def documentation(request):
    return render(request, "documentation.html")

def result(request):
    return render(request, "result.html")

def download_file(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    filename = 'results.csv'
    filepath = os.path.join(BASE_DIR, filename)
    df2.to_csv(filepath)
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response