
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from . import models


# Create your views here.
def reroute(request):
	return redirect(reverse('login:login_index'))

def index(request):
	context={'users': models.Users.objects.all()}
	return render(request, 'login/index.html', context)

def register(request):
	name = request.POST['name']
	username = request.POST['username']
	email = request.POST['email']
	bday = request.POST['bday']
	newUser = models.Users.objects.register(name=name, username=username, email=email, password=request.POST['pw'], cpassword=request.POST['confirm_pw'], bday=bday)
	if newUser[0]:
		request.session['user']=newUser[1]
		return redirect(reverse('wishlist:wishlist_index'))
	else:
		context = {'errors':newUser[1], 'name':name, 'username':username, 'email':email}
		return render(request, 'login/index.html', context)

def login(request):
	user = models.Users.objects.login(username=request.POST['username'], password=request.POST['pw'])
	if user[0]:
		request.session['user'] = user[1]
		return redirect(reverse('wishlist:wishlist_index'))
	else:
		context = {'errors2':user[1]}
		return render(request, 'login/index.html', context)

def logout(request):
	request.session.clear()
	return redirect('login:login_index')
