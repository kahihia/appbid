__author__ = 'rulongwang'
import json

from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render_to_response,HttpResponse,  RequestContext, HttpResponseRedirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.db.models import Q
from django.contrib.auth.models import User
from account import models
from account_form import RegisterForm,UserDetails, PublicProfile,EmailItems


def login_view(request):
    initParam = {}
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    redirect_to = request.POST.get('next', '/')
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect(redirect_to)
    else:
        initParam['user_name'] = request.POST.get('username')
        initParam['login_error'] = _('username or password is not correct.')
        return render_to_response("account/login.html", initParam, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    redirect_to = '/'
    return render_to_response('account/login.html', {"redirect_to": redirect_to}, context_instance=RequestContext(request))


def auth_home(request):
    redirect_to = request.GET.get('next', '/')
    return render_to_response("account/login.html", {'redirect_to': redirect_to}, context_instance=RequestContext(request))


def register(request):
    """user register method"""
    initParam = {}
    registerForm = RegisterForm()
    if request.method == "POST":
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            username = (registerForm.cleaned_data["username"]).strip()
            email = (registerForm.cleaned_data["email"]).strip()
            password = (registerForm.cleaned_data["password"]).strip()
            if models.User.objects.filter(Q(username=username) | Q(email=email)):
                initParam['register_error'] = _('%(name)s or %(email)s has been used.') % {'name': username, 'email': email}
            else:
                user = User.objects.create_user(username, email, password)
                if user is not None:
                    user.save()
                    userProfile = models.UserProfile()
                    userProfile.user = user
                    userProfile.is_bid_approved = False
                    userProfile.save()
                    return HttpResponseRedirect("/account/home/")
                else:
                    initParam['register_error'] = _('Register failed, please try again.')
    initParam['register_form'] = registerForm
    return render_to_response("account/register.html", initParam, context_instance=RequestContext(request))


def ajaxUserVerified(request, *args, **kwargs):
    """Verified user name or email in register user."""
    data = {}
    try:
        dict = request.POST
    except:
        dict = request.GET
    try:
        if dict.get('username') is not None:
            if models.User.objects.filter(username=dict.get('username')):
                data['message'] = _('%(name)s has been used.') % {'name': dict.get('username')}
                raise
            else:
                data['message'] = _('%(name)s is valid.') % {'name': dict.get('username')}
        if dict.get('email') is not None:
            if models.User.objects.filter(email=dict.get('email')):
                data['message'] = _('%(email)s has been used.') % {'email': dict.get('email')}
                raise
            else:
                data['message'] = _('%(email)s is valid.') % {'email': dict.get('email')}
        data['ok'] = 'true'
    except:
        data['ok'] = 'false'
    return HttpResponse(json.dumps(data), mimetype=u'application/json')


def _login(request, username, password):
    pass


def myprofile(request):
    pass



def account_settting(request):
    detail_form = UserDetails()
    return render_to_response("account/accountsetting.html",{"form":detail_form},
                        context_instance=RequestContext(request))




def user_detail(request):
    return render_to_response("account/accountsetting.html",{"test":"test"},
                        context_instance=RequestContext(request))


def user_public_profile(request):
    form = PublicProfile()
    return render_to_response("account/account_profile.html",{'form':form},context_instance=RequestContext(request))


def email_notification(request):
    email_items = models.email_setting.objects.all()
    return render_to_response("account/account_email_setting.html",{"email_items":email_items},
                        context_instance=RequestContext(request))


def change_password(request):
    return render_to_response("account/account_password.html",{"test":"test"},
                        context_instance=RequestContext(request))


def social_connection(request):
    return render_to_response("account/social_connection.html",{"test":"test"},
                        context_instance=RequestContext(request))


