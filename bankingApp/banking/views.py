from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from banking.forms import RegisterUserForm


class IndexPage(TemplateView):
    template_name = 'banking/index.html'


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'banking/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'banking/register.html'
    success_url = reverse_lazy('login')


class LogoutUser(LogoutView):
    next_page = 'login'



