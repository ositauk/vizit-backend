from django.shortcuts import render
from .forms import User_form
from .models import profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import uuid
from .helper import send_forget_password_mail
from datetime import datetime
import pytz
from visiters.models import visit


# Login User
def user_login(request):
    if request.method == 'POST':
        User_form(request=request, data=request.POST)
        user_n = request.POST['username']
        user_p = request.POST['password']
        user = authenticate(username=user_n, password=user_p)
        print(user)
        intz = pytz.timezone('Africa/Lagos')
        current_time = datetime.now(intz)
        if user is not None:
            login(request, user)
            obj = profile.objects.get(user=user)
            obj.login_time = current_time
            obj.logout_time = None
            obj.save()
            # messages.success(request, 'User Login')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'username or password not correct')
            return HttpResponseRedirect('/user/login/')
    else:
        form = User_form()
        return render(request, 'users/login_page.html', {'form': form})

# Logout User
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login/')

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    prof = profile.objects.get(user=user)
    prof.is_online = True
    prof.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    print('=======>', logout)
    intz = pytz.timezone('Africa/Lagos')
    current_time = datetime.now(intz)
    prof = profile.objects.get(user=user)
    prof.is_online = False
    prof.logout_time = current_time
    prof.save()




# Register New User
def user_register(request):
    visit_obj = visitobj()
    if request.user.profile.role == 'admin':
        if request.method == 'POST':
            us = request.POST['username'].lower()
            user_exist = User.objects.filter(username=us)
            if not user_exist:
                if request.POST['password1'] == request.POST['password2']:
                    ps = request.POST['password1']
                    rl = request.POST['role'].lower()
                    nm = request.POST['first_name'].lower()
                    em = request.POST['email'].lower()
                    user = User.objects.create_user(username=us, password=ps, email=em)
                    val = profile(user=user, role=rl, email=em, fname=nm)
                    val.save()
                    return HttpResponseRedirect('/user/show_user/')
                else:
                    messages.error(request, 'Password not matched')
                    return HttpResponseRedirect('/user/create/')
            else:
                messages.error(request, 'username is already exist')
                return HttpResponseRedirect('/user/create/')
        else:
            return render(request, 'users/create_user.html', {'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        return HttpResponseRedirect('/user/show_user/')


# View Users
def show_users(request):
    visit_obj = visitobj()
    if 'search' in request.GET:
        val = request.GET.get('search').lower().strip()
        form = profile.objects.filter(fname__contains=val)
        if not form:
            messages.error(request, 'No User Found')
            form1 = profile.objects.all()
            return render(request, 'visiters/users.html', {'form': form1, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
        else:
            return render(request, 'visiters/users.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        form = profile.objects.all()
        return render(request, 'visiters/users.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})


# Edit User
def edit_user(request, id):
    visit_obj = visitobj()
    if request.user.profile.role == 'admin':
        if request.method == 'POST':
            us = request.POST['username'].lower()
            rl = request.POST['role'].lower()
            nm = request.POST['f_name'].lower()
            em = request.POST['email'].lower()
            val = profile.objects.get(pk=id)
            val1 = User.objects.get(pk=id)
            if not val1.username == us:
                user_exist = User.objects.filter(username=us)
                if not user_exist:
                    val1.username = us
                    val1.save()
                else:
                    messages.error(request, 'Username already exist')
                    val = profile.objects.get(pk=id)
                    return render(request, 'users/update_user.html', {'form': val, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
            val.role = rl
            val.fname = nm
            val.email = em
            val.save()
            return HttpResponseRedirect('/user/show_user/')
        else:
            val = profile.objects.get(pk=id)
            return render(request, 'users/update_user.html', {'form': val, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        return HttpResponseRedirect('/user/show_user/')


# Delete User
def delete_users(request, id):
    val = profile.objects.get(pk=id)
    val.delete()
    return HttpResponseRedirect('/user/show_user/')


# Forget Password
def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if not User.objects.filter(username=username).first():
                print("User Not Found!!")
                messages.error(request, "No User Found!!")
                return HttpResponseRedirect('/user/forget_password/')
            print("user found!!")
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(profile_obj.email, token)
            messages.success(request, "Email Sent")
            return HttpResponseRedirect('/user/forget_password/')

    except Exception as e:
        print(e)
    return render(request, 'users/forget_password.html')


# Change Password
def change_password(request, token):
    context = {}
    try:
        profile_obj = profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_newpassword')
            user_id = request.POST.get('user_id')
            if new_password != confirm_password:
                messages.success(request, "Password not match!!")
                return HttpResponseRedirect(f'/user/change_password/{token}/')
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return HttpResponseRedirect('/user/login/')
    except Exception as e:
        print(e)
    return render(request, 'users/change_password.html', context)


# it gives value of Current,Complete Visit
def visitobj():
    count = visit.objects.filter(cheakedINinfo=1).count()
    CCount = visit.objects.filter(cheakedINinfo=2).count()
    Scount = visit.objects.filter(schedukevisit=1).count()
    return count, CCount, Scount


def demo(request):
    form = User.objects.all()
    return render(request, 'users/demo.html', {'form': form})

