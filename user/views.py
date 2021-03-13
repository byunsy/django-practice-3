from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from .forms import RegisterForm, LoginForm
from .models import User


def index(request):
    return render(request, 'index.html', {'username': request.session.get('user')})


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    return redirect('/')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            username=form.data.get('username'),
            useremail=form.data.get('email'),
            password=make_password(form.data.get('password'))
        )
        user.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    # Load the current user info to the current session
    def form_valid(self, form):
        self.request.session['user'] = form.data.get('username')
        return super().form_valid(form)
