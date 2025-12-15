from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
import math
from .models import Account, HistoryModel
from django.contrib.auth.models import User
from datetime import date
import datetime
from xml.sax.saxutils import *

# Create your views here.
def Login(request):
    if request.method == 'POST':
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')
        user = authenticate(username = ID, password = Pass)
        if user:
            if user.is_active:
                if 'account_record' not in request.POST:
                    request.session.set_expiry(0)
                login(request, user)
                return HttpResponseRedirect(reverse('input'))
            else:
                return HttpResponse("アカウントが有効ではありません")
        else:
            return HttpResponse(
            "ログインIDまたはパスワードが間違っています")
    else:
        params = {}
        initial_dict = dict()
        params["form"] = LoginForm(data = initial_dict)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('input'))
        else:    
            return render(request, 'warikan/login.html', context=params)

@login_required
def Input(request):
    template = "warikan/input.html"
    params = {}
    params['Calculated'] = True
    if request.method == 'POST':
        try:
            numMyside_f = float(request.POST.get('numMyside'))
            numMyside = int(request.POST.get('numMyside'))
            numOtherside_f = float(request.POST.get('numOtherside'))
            numOtherside = int(request.POST.get('numOtherside'))
            amount = int(request.POST.get('amount'))
            ratio = int(request.POST.get('ratio'))
            amountMyside = int(math.ceil(amount * ratio / 10000
            / numMyside_f) * 100)
            amountOtherside = int(math.ceil(amount * (100 - ratio) / 10000
            / numOtherside_f) * 100)
            charge = amountMyside * numMyside + amountOtherside\
            * numOtherside - amount 
            if numMyside < 1 or numMyside > 99\
                    or numOtherside < 1 or numOtherside > 99\
                    or amount < 1 or amount > 999999:
                raise Exception("Input Error")
        except:
            params['Calculated'] = False
            params['ratio'] = 50 
            return render(request, template, context=params)
        else:
            params['numMyside'] = numMyside 
            request.session["numMyside"] = numMyside
            params['numOtherside'] = numOtherside 
            request.session["numOtherside"] = numOtherside 
            params['amount'] = amount 
            request.session["amount"] = amount 
            params['ratio'] = ratio 
            request.session["ratio"] = ratio 
            request.session["ratio2"] = 100 - ratio 
            params['amountMyside'] = amountMyside 
            request.session["amountMyside"] = amountMyside 
            params['amountOtherside'] = amountOtherside 
            request.session["amountOtherside"] = amountOtherside 
            params['charge'] = charge 
            request.session["charge"] = charge 
            return render(request, template, context=params)
    else:
        if 'numMyside' in request.session:
            params['numMyside'] = request.session["numMyside"]
        else:
            params['Calculated'] = False
        if 'numOtherside' in request.session:
            params['numOtherside'] = request.session["numOtherside"]
        else:
            params['Calculated'] = False
        if 'amount' in request.session:
            params['amount'] = request.session["amount"]
        else:
            params['Calculated'] = False
        if 'ratio' in request.session:
            params['ratio'] = request.session["ratio"]
        else:
            params['ratio'] = 50 
            params['Calculated'] = False
        if 'amountMyside' in request.session:
            params['amountMyside'] = request.session["amountMyside"]
        else:
            params['Calculated'] = False
        if 'amountOtherside' in request.session:
            params['amountOtherside'] = request.session["amountOtherside"]
        else:
            params['Calculated'] = False
        if 'charge' in request.session:
            params['charge'] = request.session["charge"]
        else:
            params['Calculated'] = False
        return render(request, template, context=params)

@login_required
def Confirm(request):
    template = "warikan/confirm.html"
    params = {}
    if request.method == 'POST':
        date = datetime.date.today().strftime('%Y-%m-%d')
        request.session["date"] = date 
        return render(request, template, context=params)
    else:
        date = datetime.date.today().strftime('%Y-%m-%d')
        request.session["date"] = date 
        return render(request, template, context=params)

@login_required
def Register(request):
    template = "warikan/register.html"
    params = {}
    username = str(request.user)
    user_id = request.user.id
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        remarks = request.POST.get('remarks')
        numMyside = request.session["numMyside"]
        numOtherside = request.session["numOtherside"]
        amount = request.session["amount"]
        ratio = request.session["ratio"]
        amountMyside = request.session["amountMyside"]
        amountOtherside = request.session["amountOtherside"]
        charge = request.session["charge"]
        record = HistoryModel(date = date, time = time, remarks = remarks,
        numMyside = numMyside, numOtherside = numOtherside,
        amount = amount, ratio = ratio, amountMyside = amountMyside,
        amountOtherside = amountOtherside, charge = charge,
        username = username, user_id = user_id,)
        record.save()
        if HistoryModel.objects.filter(user_id = user_id).count() >= 51:
            record = HistoryModel.objects.filter(user_id = user_id)\
            .order_by('date', '-time')[:1].values()
            HistoryModel.objects.filter(id = record[0]['id']).delete()
        return render(request, template, context=params)
    else:
        return render(request, template, context=params)

@login_required
def Detail(request):
    template = "warikan/detail.html"
    params = {}
    username = str(request.user)
    user_id = request.user.id
    records = HistoryModel.objects.filter(user_id = user_id)\
    .order_by('-date', 'time')[:50].values()
    if request.method == 'POST':
        row = int(request.POST.get('row'))
        params['date'] = records[row]['date']
        params['time'] = records[row]['time']
        params['numMyside'] = records[row]['numMyside']
        params['numOtherside'] = records[row]['numOtherside']
        params['amount'] = records[row]['amount']
        params['ratio'] = records[row]['ratio']
        params['ratio2'] = 100 - records[row]['ratio']
        params['amountMyside'] = records[row]['amountMyside']
        params['amountOtherside'] = records[row]['amountOtherside']
        params['charge'] = records[row]['charge']
        params['remarks'] = records[row]['remarks']
        params['list'] = records 
        return render(request, template, context=params)
    else:
        if records.count() > 0:
            params['date'] = records[0]['date']
            params['time'] = records[0]['time']
            params['numMyside'] = records[0]['numMyside']
            params['numOtherside'] = records[0]['numOtherside']
            params['amount'] = records[0]['amount']
            params['ratio'] = records[0]['ratio']
            params['ratio2'] = 100 - records[0]['ratio']
            params['amountMyside'] = records[0]['amountMyside']
            params['amountOtherside'] = records[0]['amountOtherside']
            params['charge'] = records[0]['charge']
            params['remarks'] = records[0]['remarks']
            params['list'] = records 
        return render(request, template, context=params)

@login_required
def Jaspay(request):
    template = "warikan/jaspay.html"
    params = {}
    user_name = str(request.user)
    if request.method == 'POST':
        return render(request, template, context=params)
    else:
        try:
            jaspay = Account.objects.select_related("user")\
            .filter(user__username = user_name).values()[0]['jaspay']
        except:
            logout(request)
            return HttpResponseRedirect(reverse('login'))
        else:
            params['amountMyside'] = request.session["amountMyside"]
            params['amountOtherside'] = request.session["amountOtherside"]
            params['jaspay'] = str(jaspay)
            return render(request, template, context=params)

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

