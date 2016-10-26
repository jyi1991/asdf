from __future__ import unicode_literals
from django.db import models
from ..login.models import Users

class WishitemManager(models.Manager):
	def verify(self, user, item):#verifcation for item added in create.html file
		if item == "":
			return (False, 'Cannot be blank')
		elif len(item) < 3:
			return (False, 'Product names must be longer than 3 characters')
		else:
			return (True, self.create(item=item, added_by=user))

	def theirwishlist(self, user, mywishlist):
		wishlist = self.exclude(added_by=user)
		for wish in mywishlist:
			wishlist = wishlist.exclude(item=wish.item.item)
		wishlist = wishlist.order_by('created_at') #orders the wishlist order by created at. Delete will be at the bottom of this table.
		return wishlist

class WishlistManager(models.Manager):
	def remove(self, user, item): #allows users to delete
		self.get(user=user, item=item).delete()
		if item.added_by.id == user.id:
			self.filter(item=item).delete()
			return True

	def add(self, user, item):
		self.create(user=user, item=item);

class Wishitems(models.Model):
	item = models.CharField(max_length=45)
	added_by = models.ForeignKey(Users)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	objects = WishitemManager()

class Wishlists(models.Model):
	item = models.ForeignKey(Wishitems)
	user = models.ForeignKey(Users)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	objects = WishlistManager()
