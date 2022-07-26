from asyncio.windows_events import NULL
import json
from logging.config import valid_ident
import random
from urllib import response
from django.conf import settings
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import PasswordModel
from django.views.decorators.csrf import csrf_exempt
from .forms import PasswordEntryForm, UserRegisterForm
from .aes import *
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def index(request):
    return render(request,'website/index.html')

def login(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = auth_login(request,user)
            messages.success(request, f' welcome {username} !!',extra_tags='log_success')
            return redirect('dashboard')
        else:
            messages.info(request, f'Invalid Credentials',extra_tags='cred_error')
    form = AuthenticationForm()
    return render(request, 'website/login.html',{'form':form, 'title':'log in'})   

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db() 
            #user.profile.email = form.cleaned_data.get('email')
            user.save()
           
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('log_in')
        else:
            messages.warning(request, f'Invalid Credentials')
    else:
        form = UserRegisterForm()
    return render(request, 'website/registration.html', {'form': form, 'title':'reqister here'})

@login_required(login_url='login')
def generator(request):
    return render(request, 'website/generator.html')#, {'password':thepassword, 'selected':selected,'length':length})

def key_gen():
    length=28
    random_key=''
    characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?><:;0123456789')
    for x in range(length):
           random_key += random.choice(characters)

    return random_key

@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    messages.warning(request, f'You have succefully logged out!')
    return redirect('home')

def dashboard(request):
    ans=return_entries(request.user)
    return render(request,'website/dashboard.html',{'objects':ans})

@login_required(login_url='login')
def new_entry(request):
   if request.method == 'POST':
       form=PasswordEntryForm(request.POST)
       if form.is_valid():
            f = form.save(commit=False)
            f.username = request.user
            f.login_url = request.POST.get('url')
            f.name = request.POST.get('name')
            login_pass= request.POST.get('password')
            f.login_username = request.POST.get('username')
            key='5Zy0gKVE(@J$GVtZcWilxil^h47&'
            key_new=key_gen()
            key_new=key_new[0:28]
            d=AESCipher(key_new)
            f.login_password=d.encrypt(d._pad(login_pass))
            e=AESCipher(key)
            f.aes_key=e.encrypt(e._pad(key_new))
            print(f.aes_key)
            print(f.login_password)
            f.save()
            messages.success(request, f'You have succefully made a post!')
            return redirect('dashboard')


   return render(request,'website/newEntry.html')  

def return_entries(user):
    return PasswordModel.objects.filter(username=user)


val=None

@csrf_exempt
def request_access(request):
    if request.method=="POST":
      a = request.POST.get('request_data')
      a=a.split("_")
      a=int(a[1])
      ans= PasswordModel.objects.filter(username=request.user,id=a)
      global val
      def val():
        return ans
      print(ans)
      return HttpResponse('ok')
    else:
      print("WTF")


def view_details(request):
    ans=val()
    print(ans)
    for i in ans:
        key='5Zy0gKVE(@J$GVtZcWilxil^h47&'
        d=AESCipher(key)
        e=AESCipher(d._unpad(d.decrypt(i.aes_key)))
        i.login_password=e._unpad(e.decrypt(i.login_password))
        print(i.login_password)
        return render(request,'website/viewDetails.html',{'i':i})

def anonymous(request):
    return redirect('dashboard')

def delete_entry(request,pk):
    a = PasswordModel.objects.filter(username=request.user,id=pk)
    a.delete()
    return redirect('dashboard')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "website/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'carwarstars@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="website/password_reset.html", context={"password_reset_form":password_reset_form})