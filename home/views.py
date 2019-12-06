from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import *
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from .serializers import PortfolioSerializers
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


def customercreation(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        con_password = request.POST['con_password']
        data = Customer(phone_number=phone_number, email=email, password=password, con_password=con_password)
        data.save()
        return render(request, 'registration/login.html')
    return render(request, 'registration/register1.html')


def customerpage(request):
    if request.method == 'POST':
        password = request.POST['password']
        if request.POST['phone_number']:
            mobile_phone = request.POST['phone_number']
            user = Customer(phone_number=mobile_phone, password=password)
        else:
            email = request.POST['email']
            mobile_phone = Customer.objects.get(email=email).phone_number
            user = Customer(email=mobile_phone, password=password)
        if user is not None:
            return render(request, 'index1.html', {'user': user})
        else:
            return redirect('customerpage')
    return render(request, 'registration/login.html')


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            users = New_Portfolio.objects.filter(Q(location__icontains=query) |
                                                 Q(sub_category__name__icontains=query) |
                                                 Q(category__name__icontains=query))

            if users:
                return render(request, 'searchlistpage.html', {'users': users})

            else:
                messages.error(request, 'no results found')

        else:
            users = New_Portfolio.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(users, 3)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            return render(request, 'searchlistpage.html', {'users': users})

    #return render(request, 'index.html')


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


class Listing(ListAPIView):
    serializer_class = PortfolioSerializers

    def get_queryset(self):
        querylist = New_Portfolio.objects.all()
        # specialization = self.request.query_params.get('specialization', None)
        location = self.request.query_params.get('location', None)
        sort_by = self.request.query_params.get('sort_by', None)
        if location:
            querylist = querylist.filter(location=location)
        if sort_by == "experience":
            querylist = querylist.order_by("experience")
        # elif sort_by == "location":
        #     querylist = querylist.order_by("location")
        elif sort_by == "budget":
            querylist = querylist.order_by("budget")
        return querylist


def getlocation(request):
    if request.method == "GET" and request.is_ajax():
        locations = New_Portfolio.objects.exclude(location__isnull=True). \
            exclude(location__exact='').order_by('location').values_list('location').distinct()
        locations = [i[0] for i in list(locations)]
        data = {
            "locations": locations,
        }
        return JsonResponse(data, status=200)


def view_profile(request, user_id):
    user = New_Portfolio.objects.get(user_id=user_id)
    return render(request, 'viewprofile.html', {'user': user})


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


def feedback(request):
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return redirect('view_profile')
    return render(request, 'viewprofile.html', {'form': form})


def getfeedback(request, user_id):
    feedback_list = FeedBack.objects.filter(user_id=user_id)
    return render(request, 'feedback.html', {'feedback': feedback_list})


def question(request):
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
    return render(request, 'Q&A.html', {'form': form})


def answer(request):
    question_id = request.POST('question')
    customer_id = request.POST('customer')
    client_id = request.POST('client')
    answer = request.POST('answer')
    pub_date = request.POST('pub_date')
    Answers(question=question_id, customer=customer_id, client=client_id, answer=answer, pub_date=pub_date).save()
    messages.error(request, 'answer submitted successfully')
    return render(request, 'Q&A.html')


def gey_answer(request, user_id):
    ans = Answers.objects.filter(client_id=user_id)
    return render(request, "Q&A.html", {'ans': ans})


def AboutDesigner(request, user_id):
    about = New_Portfolio.objects.filter(user_id=user_id)
    return render(request, 'about.html', {'about': about})
