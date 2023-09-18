from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html', {'registration_form': RegisterForm()})

    def post(self, request, *args, **kwargs):
        user_form = RegisterForm(request.POST)

        if not user_form.is_valid():
            return render(request, 'register.html', {'registration_form': user_form})

        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()

        return render(request, 'register_done.html', {'new_user': new_user})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'login_form': LoginForm()})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)

        if not login_form.is_valid():
            return render(request, 'login.html', {'login_form': login_form})

        cd = login_form.cleaned_data
        user = authenticate(username=cd['email'], password=cd['password'])
        if not user or not user.is_active:
            login_form.add_error('email', 'User not found')
            return render(request, 'login.html', {'login_form': login_form})

        login(request, user)
        return render(request, 'register_done.html', {'new_user': login_form})
