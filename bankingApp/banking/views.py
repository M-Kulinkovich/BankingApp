import json
import os

import requests
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from banking.forms import RegisterUserForm


class IndexPage(TemplateView):
    template_name = 'banking/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = "https://api.apilayer.com/currency_data/live?source=USD&currencies=EUR,GBP,BYN,PLN"
        headers = {
            "apikey": os.environ.get('API_KEY')
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        eur_rate = data['quotes']['USDEUR']
        gbp_rate = data['quotes']['USDGBP']
        byn_rate = data['quotes']['USDBYN']
        pln_rate = data['quotes']['USDPLN']

        context['eur_rate'] = eur_rate
        context['gbp_rate'] = gbp_rate
        context['byn_rate'] = byn_rate
        context['pln_rate'] = pln_rate

        return context


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



