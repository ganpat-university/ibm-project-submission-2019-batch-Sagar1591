from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from .forms import CreateUserForm, LoginForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import send_otp
from datetime import datetime
#from .forms import FileUploadForm
from pymongo import MongoClient
import pymongo
import csv
import json
import xml.etree.ElementTree as ET
from io import TextIOWrapper
import pyotp

# Create your views here.
def homepage(request):
    data={
        
    }
    return render(request, "index.html",data)

def Login(request):
    
    form = LoginForm(request.POST)
    
    if request.method == 'POST':
        
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
        
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username,password = password)
            
        if user is not None:
            send_otp(request),
            request.session['username'] = username
            return redirect('login-otp')
        else:
            return HttpResponse("Username or password is incorrect!!")
        
    context = {'form': form}
    return render(request,"login.html",context=context)


def logout(request):
    auth.logout(request)
    return render(request,'index.html')

def Login_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']
        
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']
        
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)
                    
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    
                    return redirect('dashboard')
                else:
                    return HttpResponse("Invalid otp")
            else:
                return HttpResponse("otp has expired")
        else:
            return HttpResponse("oops.. something went wrong")

    return render(request,"login-otp.html",{})

def email_verification(request, uidb64, token):
    
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    
    #success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    
    #failed
    else:
        
        return redirect('email-verification-failed')
    
def email_verification_sent(request):
    return render(request, "email-verification-sent.html")

def email_verification_success(request):
    return render(request, 'email-verification-success.html')

def email_verification_failed(request):
    return render(request, 'email-verification-failed.html')

def Signup(request):
    
    form = CreateUserForm()
    
    if request.method == 'POST':
        
        form = CreateUserForm(request.POST)

        if form.is_valid():
            
            user = form.save()
            user.is_active=False
            user.save()
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('email-verification.html', {
                    
                    'user':user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_tokenizer_generate.make_token(user),
                    
            })
                
            user.email_user(subject=subject, message=message)           
            return redirect('email-verification-sent')
    
    context = {'form': form}
    return render(request, "signup.html", context=context)

        

@login_required(login_url='login')
def dashboard(request):
    if 'username' in request.session:
        del request.session['username']
    if request.method == 'POST':
        files = request.FILES['file']
        if files.name.endswith('.csv'):
            # Process CSV file
            reader = csv.DictReader(TextIOWrapper(files, encoding='utf-8'))
            data = [row for row in reader]
        elif files.name.endswith('.json'):
            # Process JSON file
            data = json.load(files)
        elif files.name.endswith('.xml'):
            # Process XML file
            root = ET.fromstring(files.read().decode('utf-8'))
            data = [{elem.tag: elem.text for elem in child} for child in root]
        else:
            # Invalid file type
            return render(request, 'dashboard.html', {'error': 'Invalid file type'})

        # Clean data here
        cleaned_data = []
        for row in data:
            cleaned_row = {}
            for key, value in row.items():
                if value.strip() != '':  # remove empty fields
                    cleaned_row[key] = value.strip()
            if cleaned_row:  # remove empty rows
                cleaned_data.append(cleaned_row)

        # Store cleaned data in MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['prodata_db']
        collection = db['Users']
        collection.insert_many(cleaned_data)

        return render(request, 'upload_success.html', {'success': 'File uploaded successfully'})
    else:
        return render(request, 'dashboard.html')



def proid(request,id):
    return HttpResponse(id)

def aboutus(request):
    return render(request, "aboutus.html")

def security(request):
    return render(request, "security.html")

def confidentiality(request):
    return render(request, "confidentiality.html")

def integrity(request):
    return render(request, "integrity.html")

def availability(request):
    return render(request, "availability.html")

def blog(request):
    return render(request, "blog.html")


# def login(request):
#     # ans=0
#     # data={}
#     # try:
#     #     if request.method=="POST":
#     #         n1=request.POST.get('uname')
#     #         n2=request.POST.get('passwd')
#     #         ans=n1+n2
#     #         data={
#     #             'n1':n1,
#     #             'n2':n2,
#     #             'output':ans
#     #         }
#     #         # url="/dashboard/?output={}".format(ans)
#     #         # return HttpResponseRedirect(url)
#     # except:
#     #     pass
#     # return render(request, "login.html",data)
#     return render(request, "login.html")

# def signin(request):
#     return render(request, "signin.html")

# def dashboard(request):
#     # if request.method=="GET":
#     #     output = request.GET.get('output')
#     # return render(request, "dashboard.html",{'output':output})
#     ans=0
#     data={}
#     try:
#         if request.method=="POST":
#             n1=request.POST.get('uname')
#             n2=request.POST.get('passwd')
#             ans=n1
#             data={
#                 'n1':n1,
#                 'n2':n2,
#                 'output':ans
#             }
#         return render(request,"dashboard.html",data)
#     except:
#         pass
    

