# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile', primary_key=True)
    email_confirmed = models.BooleanField(default=False)
    college = models.CharField(max_length=10,blank=False)
    branch = models.CharField(max_length=10,blank=False)
    year = models.CharField(max_length=10,blank=False)

    def __unicode__(self):
        return unicode(self.user)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()

# Create your models here.
class room_category(models.Model):
    cat_name=models.CharField(max_length=200)
    img_file_name=models.CharField(max_length=200)


    def __str__(self):
        return self.cat_name
class product_category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class products(models.Model):
    pc_name=models.ForeignKey(product_category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=200)
    photo=models.CharField(max_length=200)
    price=models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class selected_productss(models.Model):
    u_pk=models.IntegerField()
    p_pk=models.IntegerField()
    c_pk=models.IntegerField()

    def __str__(self):
        return "{0} {1}".format(self.u_pk,self.p_pk)


class room_category_size(models.Model):
    category = models.ForeignKey(room_category, on_delete=models.CASCADE)
    cat_width=models.IntegerField(default=0)
    cat_height=models.IntegerField(default=0)

    def __str__(self):
        return  "{0} {1}  X {2}".format(self.category,self.cat_width,self.cat_height)

class dimensions(models.Model):
    category=models.ForeignKey(room_category, on_delete=models.CASCADE)
    size=models.ForeignKey(room_category_size,on_delete=models.CASCADE)
    dim_w=models.IntegerField(default=0)
    dim_h=models.IntegerField(default=0)

    def __str__(self):
        return "{0} {1} {2} X {3}".format(self.category,self.size,self.dim_w,self.dim_h)
