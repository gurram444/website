from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from random import randint
import urllib
from urllib import request
import urllib.request
import urllib.parse
from contextlib import closing
from django.db.models import Q
import hashlib


# Create your views here.
def Home(request):
    return render(request, 'index.html')


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr


resp = sendSMS('vV4ixMZmyok-YTys5TMHMljOCzBrfZDYc6aQzUED2B', '917406096991',
               'IUNGO', 'Hi, Bharath.')
print(resp)


def clientcreation(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)

        if form.is_valid():
            # import pdb;pdb.set_trace()
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            request.session['user'] = username
            return redirect('userauthentication')

    else:
        form = ClientRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def customercreation(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            request.session['user'] = username
            return redirect('userauthentication')

    else:
        form = CustomerRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def userauthentication(request):
    if request.session.has_key('user'):
        username = request.session['user']
        user = Client.objects.get(username=username)
        return render(request, 'user.html', {'user': user})
    return redirect('userpage')


def userpage(request):
    if request.method == 'POST':
        password = request.POST['password']
        if request.POST['mobile_phone']:
            mobile_phone = request.POST['mobile_phone']
            user = authenticate(username=mobile_phone, password=password)
        else:
            email = request.POST['email']
            mobile_phone = Client.objects.get(email=email).mobile_phone
            user = authenticate(username=mobile_phone, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['user'] = user.username
                return redirect('userauthentication')
            messages.add_message(request, messages.INFO, 'User is Not Active.')
            return redirect('userpage')
        messages.add_message(request, messages.INFO, 'Please Check Your Login Credentials.')
        return redirect('userpage')

    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def search(request):
    users = New_Portfolio.objects.all()
    query = request.GET.get('q')

    if query:
        users = users.objects.filter(
            Q(sub_category__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)).distinct()
        # remove duplicates
    context = {'users': users}

    return render(request, 'listingPage.html', context)

    #  return render(request,'index.html')


def user_list(request, category_id, user_type):
    sub_category = Sub_category.objects.get(name=user_type, category=category_id)
    users = New_Portfolio.objects.filter(sub_category=sub_category)
    page = request.GET.get('page', 1)

    paginator = Paginator(users, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'listingPage.html', {'users': users})


def login_register(request):
    return render(request, 'registration/login.html')


def portfolio(request):
    # form = New_PortfolioForm()
    # return render(request,'portfolio.html',{'form':form})
    if request.session.has_key('user'):
        if request.method == 'POST':
            user = request.session['user']
            user = Client.objects.get(username=user)
            form = New_PortfolioForm(request.POST, request.FILES)
            # import pdb;pdb.set_trace()
            if form.is_valid():
                user_portfolio = form.save(commit=False)
                user_portfolio.user = user
                user_portfolio.save()
                return HttpResponse('details saved successfully.')
            return HttpResponse('error')
        else:
            form = New_PortfolioForm()
            return render(request, 'portfolio.html', {'form': form})