from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from .models import *
from django.template.context_processors import csrf
from django.views.generic import View
from random import randint
import urllib
from urllib import request
import urllib.request
import urllib.parse
from contextlib import closing
from django.db.models import Q


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


def register(request):
    if request.method == "GET":
        context = {}
        context.update(csrf(request))
        context['form'] = RegistrationForm()
        return render_to_response('register.html', context)

    if request.method == 'POST':
        context = {}
        form = RegistrationForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_active = 1
            # obj.save()
            obj.mobile_phone = form.cleaned_data["mobile_phone"]
            obj.save()
            context["user"] = obj.username
            return render(request, 'index.html', context)
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = User.objects.filter(phone_number=phone_number, password=password)
        if user:
            return HttpResponse('login success', 'index.html')
        else:
            return HttpResponse('enter valid username and password')

    return render(request, 'login.html')


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(category__icontains=query) | Q(sub_category=query)

            results = Portfolio.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, '', context)

        else:
            return render(request, '')

    else:
        return render(request, 'index.html')

