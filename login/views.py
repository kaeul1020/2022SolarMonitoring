from django.shortcuts import render, redirect
from login.forms import UserForm
from django.urls import reverse_lazy


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('done/')
    else:
        form = UserForm()
    return render(request, 'login/register.html', {'form': form})