from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import numpy as np
from sklearn.model_selection import train_test_split 

from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, StackingRegressor
from xgboost import XGBRegressor, XGBRFRegressor

from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.metrics import r2_score
from sklearn.exceptions import InconsistentVersionWarning
import warnings
import pickle


# Create your views here.
#@login_required(login_url='/login/')
def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == "POST":
        uname = request.POST.get('Username')
        email = request.POST.get('Email')
        pass1 = request.POST.get('Password')
        pass2 = request.POST.get('Confirm Password')

        if pass1!=pass2:
            return HttpResponse("Your Password and Confirm Password are not same!!!")

        else:    
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

        

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        Pass = request.POST.get('Pass')
        user = authenticate(request,username=uname,password=Pass)
        if user is not None:
            login(request,user)
            return redirect("home")
        else: 
            return HttpResponse("Username or Password is incorrect!!!!")

    return render(request, 'login.html')   


def LogoutPage(request):
    logout(request)
    return redirect("login")


# @login_required(login_url='/login/')
def ProfilePage(request):
    return render(request, 'Profiles.html')


def PredictionPage(request):
    return render(request, 'Prediction.html')


def getPredictions(mass_npea, size_npear, malign_ratio, damage_size, exposed_area, std_dev_malign, err_malign, malign_penalty,	damage_ratio,A,B,C,D,E,F,G,H,I,J,K,L,M):

    
    Melamodel = pickle.load(open("Mela_model.sav", "rb"))

    prediction = Melamodel.predict([mass_npea, size_npear, malign_ratio, damage_size, exposed_area, std_dev_malign, err_malign, malign_penalty,	damage_ratio,A,B,C,D,E,F,G,H,I,J,K,L,M])
    return prediction



def result(request):
   
    mass_npea = float(request.GET['mass_npea'])
    size_npear = float(request.GET['size_npear'])
    malign_ratio = float(request.GET['malign_ratio'])
    damage_size = float(request.GET['damage_size'])
    exposed_area = float(request.GET['exposed_area'])
    std_dev_malign = float(request.GET['std_dev_malign'])
    err_malign = float(request.GET['err_malign'])
    malign_penalty = float(request.GET['malign_penalty'])
    damage_ratio = float(request.GET['damage_ratio'])


    A = malign_penalty - err_malign
    B = damage_size - damage_ratio
    C = damage_ratio - malign_ratio
    D = malign_penalty/std_dev_malign
    E = mass_npea/exposed_area
    F = exposed_area/mass_npea
    G = A/std_dev_malign
    H = damage_size / A
    I = std_dev_malign/exposed_area
    J = err_malign/exposed_area
    K = (damage_ratio*100)/exposed_area
    L = (std_dev_malign+1)/(err_malign+1)
    M = (malign_penalty+1)/(err_malign+1)

    exposed_area = np.log1p(exposed_area)

    result = getPredictions(mass_npea, size_npear, malign_ratio, damage_size, exposed_area, std_dev_malign, err_malign, malign_penalty,	damage_ratio, A,B,C,D,E,F,G,H,I,J,K,L,M)

    return render(request, 'result.html', {'result':result})
    