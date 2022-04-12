from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileUpdateForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.contrib.auth.models import User
import datetime
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def home(request):
     return render(request, 'home.html')

def landing(request):
     return render(request, 'landing.html')

@login_required(login_url='/landing')
def matchingroom(request):
     Users = get_user_model()
     myprofile= request.user.userprofile
     c_k = myprofile.current_check
     next = Users.objects.filter()[(c_k):(c_k + 1)].get()
     context = {'next':next}
     return render(request,'dislikenext.html',context)

def accountlogin(request):
     if request.method == 'POST':
         user_name = request.POST.get('username')
         user_password = request.POST.get('password')
         user = authenticate(request, username=user_name, password=user_password)
         if user is not None:
             login(request, user)
             return redirect('hunny-profile')
         else:
             messages.info(request, "Username or Password is incorrect!")
     context = {}
     return render(request, 'login.html', context)

@login_required(login_url='/landing')
def like_next(request):
    return searching_process(request, 1)

@login_required(login_url='/landing')
def dislike_next(request):
    return searching_process(request, 0)

def searching_process(request, like):
     Users = get_user_model()
     myprofile= request.user.userprofile
     current_check = myprofile.current_check
     next_check = next_check_index(Users, Users.objects.count(), request.user, current_check)
     myprofile.current_check = next_check
     myprofile.save()
     next = Users.objects.filter()[(next_check):(next_check + 1)].get()
     if like == 1:
        current_check_user = Users.objects.filter()[(current_check):(current_check + 1)].get()
        myprofile.who_like_me.add(current_check_user)
        match = add_match_if_bothlike(request.user, current_check_user)
        context = {'next':next, 'match':match}
        return render(request, 'likenext.html', context)
     if like == 0:
        context = {'next':next}
        return render(request, 'dislikenext.html',context)

def add_match_if_bothlike(user1, user2):
    if user1 in user2.userprofile.who_like_me.all():
        user1.userprofile.matches.add(user2)
        user2.userprofile.matches.add(user1)
        user2.userprofile.who_like_me.remove(user1)
        user1.userprofile.who_like_me.remove(user2)
        return 1
    return 0
def gender_condition(user1,user2):
    gender_pre1 = user1.userprofile.gender_preference
    gender_pre2 = user2.userprofile.gender_preference
    gender1 = user1.userprofile.gender
    gender2 = user2.userprofile.gender
    if (gender_pre1 == 'No Preference'):
        gen_con1 = True
    else:
        gen_con1 = (gender_pre1 == gender2)
    if (gender_pre2 == 'No Preference'):
        gen_con2 = True
    else:
        gen_con2 = (gender_pre2 == gender1)
    return ((gen_con1) and (gen_con2))

def relationship_condtition(user1,user2):
    rel_pre1 = user1.userprofile.relationship_preference
    rel_pre2 = user2.userprofile.relationship_preference
    return (rel_pre1 == rel_pre2)

def meet_condition(user1, user2):
    return (relationship_condtition(user1, user2) and gender_condition(user1,user2))

def next_check_index(Users, max, user, current_index):
    if current_index == (max - 1):
        next_index = 0
    else:
        next_index = current_index + 1
    while (True):
        next_user = Users.objects.filter()[(next_index):(next_index + 1)].get()
        if ((user != next_user) and meet_condition(user, next_user)):
            return next_index
        else:
            if next_index == (max - 1):
                next_index = 0
            else:
                next_index = next_index + 1


def terms_service(request):
     context = {}
     return render(request, 'terms_service.html',context)

@login_required(login_url='/landing')
def editProfile(request):
    p_form = ProfileUpdateForm()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        city = request.POST.get('city')
        gender = request.POST.get('gender')
        birthday = request.POST.get('gender')
        bio = request.POST.get('bio')
        image0 = request.FILES.get('image0')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')

        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        p_form.first_name = first_name
        p_form.last_name = last_name
        p_form.city = city
        p_form.gender = gender
        p_form.birthday = birthday
        p_form.bio = bio
        p_form.image0 = image0
        p_form.image1 = image1
        p_form.image2 = image2
        if p_form.is_valid():
            p_form.save()
            return redirect('hunny-profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    context = {'p_form': p_form}
    return render(request, 'profile_edit.html', context)

def accountlogout(request):
    logout(request)
    return redirect('/landing')

@login_required(login_url='/landing')
def chat(request):
    myprofile = request.user.userprofile
    matches = myprofile.matches.all()
    context = {'matches': matches}
    return render(request, 'chat.html', context)

@login_required(login_url='/landing')
def chat_room(request, room_name):
    Users = get_user_model()
    myprofile= request.user.userprofile
    c_k = myprofile.current_check
    next = Users.objects.filter()[(c_k):(c_k + 1)].get()
    matches = myprofile.matches.all()

    return render(request,'chat_room.html',{
        'matches': matches, 
        'next': next,
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })

@login_required(login_url='/landing')
def user(request):
    return render(request, 'user.html')

def home(request):
     return render(request, 'home.html')

@login_required(login_url='/landing')
def profile(request):
     return render(request, 'profile.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    form = CreateUserForm();
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request,'Account was created successfully for ' + user_name )
            return redirect('hunny-login')
    context = {'form': form}
    return render(request, 'signup.html', context)

@login_required(login_url='/landing')
def preferences(request):
    return render(request, 'preferences.html')

@login_required(login_url='/landing')
def editPreferences(request):
    p_form = ProfileUpdateForm()
    if request.method == 'POST':
        gender = request.POST.get('gender_preference')
        relationship = request.POST.get('relationship_preference')
        age_range = request.POST.get('age_range')
        distance = request.POST.get('match_radius')

        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        p_form.gender_preference = gender
        p_form.relationship_preference = relationship
        p_form.age_range = age_range
        p_form.match_radius = distance
        if p_form.is_valid():
            p_form.save()
            return redirect('hunny-preferences')
    else:
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    context = {'p_form':p_form}
    return render(request, 'preferences_edit.html', context)

@login_required(login_url='/landing')
def settings(request):
    return render(request, 'settings.html')
