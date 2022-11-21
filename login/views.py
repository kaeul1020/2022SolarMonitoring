from django.shortcuts import render, redirect
from login.forms import UserForm, UserPasswordResetForm
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('done/')
    else:
        form = UserForm()
    return render(request, 'login/register.html', {'form': form})

class UserPasswordResetView(auth_views.PasswordResetView):
    template_name='login/password_reset.html'
    email_template_name="login/password_reset_email.html"
    success_url=reverse_lazy('login:password_reset_done')
    form_class = UserPasswordResetForm
