from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
	def register(self, **kwargs): #**kwargs insted of (self, name,username, etc..)
		errors = {}
		name = kwargs['name']
		username = kwargs['username']
		email = kwargs['email']
		password = kwargs['password']
		con_password = kwargs['password']
		bday = kwargs['bday']
		hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		if len(name) < 2:
			errors['name'] = 'Please enter a name longer than 2 letters'
		try:
			existing_user = self.get(email_iexact=user)
		except:
			existing_user = None
		if existing_user:
			errors['username'] = 'Username already in use.'
		if len(username) < 2:
			errors['username'] = 'User name has to be longer than 2 characters.'
		try:
			existing_email = self.get(email_iexact=email)
		except:
			existing_email = None
		if existing_email:
			errors['email'] = 'Email already in use.'
		if not EMAIL_REGEX.match(email):
			errors['email'] = 'The email you entered is not valid.'
		if len(password) < 8:
			errors['password'] = 'Password must be at least 8 characters long'
		elif not password == con_password:
			errors['password'] = 'Password does not match.'
		elif not bday:
			errors['bday'] = 'Please enter your birthday!'
		if errors:
			return (False, errors)
		else:
			newUser = self.create(name=name, username=username, email=email, password=hashed, bday=bday)
			return (True, newUser.id)

	def login(self, **kwargs):
		errors = {}
		username = kwargs['username']
		password = kwargs['password']
		try:
			user = self.get(username=username)
		except:
			errors['username'] = 'Username does not exist'
			return(False, errors)
		hashed = bcrypt.hashpw(password.encode(), user.password.encode())
		if not username:
			errors['username'] = 'Please enter a valid username'
		elif not user:
			errors['username'] = 'Could not find an account for '+ username
		elif not user.password == hashed:
			errors['password'] = 'Password/Username Invalid'
		else:
			return (True, user.id)
		return (False, errors)

	def everyoneElse(self, id):
		return self.exclude(id=id)

class Users(models.Model):
    name = models.CharField(max_length = 40)
    username = models.CharField(max_length = 40)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    bday = models.DateField(auto_now = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
# Create your models here.
