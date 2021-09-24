from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required

#from django.contrib.auth.models import User

# Create your views here.


def register(request):
    if request.method =='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.error(request, f'Given email is already used! Try another one.')
    else:
        form = UserRegistrationForm()
    return render(request,'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method =='POST':

        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)


        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated!')
            return redirect('profile')

    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
            'u_form': u_form,
            'p_form': p_form
            }

    return render(request,'users/profile.html',context)


#
# def register(request):
#     if request.method =='POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             ile_maili = len(User.objects.filter(email = request.POST['email']))     #proteza do weryfikacji czy email jest unikatowy
#             if ile_maili == 0:
#                 form.save()
#                 username = form.cleaned_data.get('username')
#                 messages.success(request, f'Account created for {username}!')
#                 return redirect('login')
#             else:
#                 messages.error(request, f'Given email is already used! Try another one.')
#     else:
#         form = UserRegistrationForm()
#     return render(request,'users/register.html', {'form':form})
#
# @login_required
# def profile(request):
#     if request.method =='POST':
#
#         u_form = UserUpdateForm(request.POST,instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
#
#         ile_maili = len(User.objects.filter(email=request.POST['email'])) # proteza do weryfikacji czy email jest unikatowy
#
#         if ile_maili == 0:
#             if u_form.is_valid() and p_form.is_valid():
#                 u_form.save()
#                 p_form.save()
#                 messages.success(request, f'Account updated! {ile_maili}')
#                 return redirect('profile')
#         else:
#             messages.error(request, f'Given email is already used!')
#     else :
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#             'u_form': u_form,
#             'p_form': p_form
#             }
#
#     return render(request,'users/profile.html',context)
