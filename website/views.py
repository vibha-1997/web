# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render,redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render,render_to_response
from django.contrib.auth import login
import json
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from website.forms import UserForm, UserProfileForm
from website.tokens import account_activation_token
from .models import room_category,room_category_size,product_category,products,selection
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.conf import settings
import hashlib
import logging, traceback
from random import randint
from django.views.decorators.csrf import csrf_exempt
import constants as constants
import config as config
# Create your views here.

def welcome(request):
    return render(request,'welcome.html')

@login_required
def  welcome2(request):
    return render(request,'welcome2.html')

@login_required
def create_design(request):
    latest_category_list = room_category.objects.all()
    product_cat=product_category.objects.all()
    product_ids=products.objects.all()
    context = {'latest_category_list': latest_category_list,'product_cat':product_cat,'product_ids':product_ids}
    return render(request, 'create_design.html',context)


@login_required
def selected_products(request,u_pk,c_pk,p_pk):
    p=selection(user_cat=u_pk,product_cat=c_pk,product_pk=p_pk)

    product = products.objects.get(id=p_pk)
    print(c_pk)
    q=selection.objects.all().filter(product_cat=c_pk)
    r=q.count()
    if(r>=1):
        q.delete()
        p.save()
        return HttpResponse(product.photo)
  
    else:
        p.save()
        return HttpResponse(product.photo)
    
    
#def home(request):
#    latest_category_list = room_category.objects.all()
#    context = {'latest_category_list': latest_category_list}
#    return render(request, 'welcome.html',context)

    
@login_required
def details(request,pc_name_id):
    product_cat_list=product_category.objects.all()
    products_list=products.objects.all()
    context={'products_list':products_list}




@login_required
def get_cart(request,u_pk):
    r=selection.objects.filter(user_cat=u_pk)
    context=[]
    total=0
    for pro in r:
        q=products.objects.filter(id=pro.product_pk)
        context.append(q[0])
        total=total+q[0].price
    context={'user_products':context,'total_price':total}
    return render(request,'cart.html',context)
@login_required
def remove_from_cart(request,u_pk,p_pk):
    r=selection.objects.filter(user_cat=u_pk,product_pk=p_pk)
    r.delete()

    return render(request, 'create_design.html')


def register(request):
    #registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_active = False
            user.save()

            profile = profile_form.save()
            profile.user = user
            profile.save()

            current_site = get_current_site(request)
            subject = 'activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
         #   registered = True
          #  user_form = UserForm()
           # profile_form = UserProfileForm()
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/registration_form.html', {'user_form':user_form, 'profile_form': profile_form})

def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('activation_complete')
    else:
        return render(request, 'registration/account_activation_invalid.html')

def activation_complete(request):
    return render(request, 'registration/activation_complete.html')


def payment(request):   
    data = {}
    a=request.user.id
    r=selection.objects.filter(user_cat=a)
    total=0
    for pro in r:
        q=products.objects.filter(id=pro.product_pk)
        total=total+q[0].price
    user=User.objects.get(pk=a)
    txnid = get_transaction_id()
    hash_ = generate_hash(request, txnid)
    hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = constants.PAYMENT_URL_LIVE 
    data["amount"] = float(total)
    data["productinfo"]  = constants.PAID_FEE_PRODUCT_INFO
    data["key"] = config.KEY
    data["txnid"] = txnid
    data["hash"] = hash_
    data["hash_string"] = hash_string
    data["firstname"] = user
    data["email"] = user.email
    #data["phone"] = user.phone_no
    data["service_provider"] = constants.SERVICE_PROVIDER
    data["furl"] = request.build_absolute_uri(reverse("payment_failure"))
    data["surl"] = request.build_absolute_uri(reverse("payment_success"))
    
    return render(request, "payment_form.html", data)

def generate_hash(request, txnid):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

# create hash string using all the fields
def get_hash_string(request, txnid):
    a=request.user.id
    r=selection.objects.filter(user_cat=a)
    user=User.objects.get(pk=a)
    total=0
    for pro in r:
        q=products.objects.filter(id=pro.product_pk)
        total=total+q[0].price
    hash_string = config.KEY+"|"+txnid+"|"+str(float(total))+"|"+constants.PAID_FEE_PRODUCT_INFO+"|"
    hash_string += str(user)+"|"+str(user.email)+"|"
    hash_string += "||||||||||"+config.SALT

    return hash_string

# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid

# no csrf token require to go to Success page. 
# This page displays the success/confirmation message to user indicating the completion of transaction.
@csrf_exempt
def payment_success(request):
    data = {}
    return render(request, "success.html", data)

# no csrf token require to go to Failure page. This page displays the message and reason of failure.
@csrf_exempt
def payment_failure(request):
    data = {}
    return render(request, "failure.html", data)
def display_uid(request):
    name=request.user.id
    user=User.objects.get(pk=name)
    return HttpResponse(user.phone_no)

