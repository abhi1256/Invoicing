from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
# @user_passes_test
def handleLogin(request):

    if request.method == 'POST':
        print(request.POST)
        email_id = request.POST['email']
        print(email_id)
        password = request.POST['password']
        print(password)
        a = authenticate(email=email_id, password=password)
        # print(a)
        if a is not None:
            if a.approvals == 1:
                login(request, a)
                messages.success(request, "")
                return redirect('/')
            else:
                messages.error(request, "Account has not been approved.")         
        else:
            messages.error(request, "Incorrect credentials. Please try again.")

    return render(request, 'listview/login.html')

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('/user/login/')