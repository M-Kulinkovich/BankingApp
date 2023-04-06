import csv
import json
import os
import requests

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView, LoginView
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView

from banking.forms import RegisterUserForm, TransferForm, AddMoneyForm
from banking.models import Account, Transfer


class TransactionsPageView(ListView):
    template_name = 'banking/transactions.html'
    context_object_name = 'transfer_list'
    paginate_by = 25

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transfer.objects.all()
        else:
            user = self.request.user
            account = get_user_model().objects.get(username=user.username).account
            transfer_list = Transfer.objects.filter(Q(sender=account) | Q(recipient=account))
            return transfer_list


class TransactionsCsvView(ListView):
    model = Transfer

    def render_to_response(self, context, **response_kwargs):
        transfer_list = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.request.user.username}_transactions.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'sender', 'recipient', 'amount', 'timestamp'])
        for transfer in transfer_list:
            writer.writerow([transfer.id,
                             transfer.sender.user.username,
                             transfer.recipient.user.username,
                             transfer.amount,
                             transfer.date,
                             ])
        return response


class IndexPageView(TemplateView):
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


class AccountPageView(View):
    template_name = 'banking/account.html'

    def get(self, request):
        user = request.user.account
        users = Account.objects.exclude(user=request.user)

        if request.user.is_staff:
            form = AddMoneyForm()
        else:
            form = TransferForm(sender=user)

        context = {
            'user': user,
            'users': users,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        users = Account.objects.exclude(user=request.user)
        user = request.user.account

        if request.user.is_staff:
            form = AddMoneyForm(request.POST)
            if form.is_valid():
                recipient = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']

                if amount == 0:
                    messages.error(request, 'cant send 0 funds')
                    return redirect('account')
                elif amount < 0:
                    messages.error(request, 'cant send negative')
                    return redirect('account')

                Account.objects.filter(pk=recipient.pk).update(balance=F('balance') + amount)

                Transfer.objects.create(
                    sender=user,
                    recipient=recipient,
                    amount=amount,
                )

                messages.success(request, f'{amount} $ has been added to {recipient.user.username} account.')
                return redirect('account')
        else:
            form = TransferForm(request.POST, sender=user)

            if form.is_valid():
                recipient = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']

                sender = request.user.account
                if sender.balance < amount:
                    messages.error(request, 'Not enough money')
                    return redirect('account')
                elif amount == 0:
                    messages.error(request, 'cant send 0 funds')
                    return redirect('account')
                elif amount < 0:
                    messages.error(request, 'cant send negative')
                    return redirect('account')

                Account.objects.filter(pk=sender.pk).update(balance=F('balance') - amount)
                Account.objects.filter(pk=recipient.pk).update(balance=F('balance') + amount)

                Transfer.objects.create(
                    sender=sender,
                    recipient=recipient,
                    amount=amount,
                )

                messages.success(request, f'{amount} $ has been added to {recipient.user.username}.')
                return redirect('account')

        context = {
            'user': user,
            'users': users,
            'form': form,
        }

        return render(request, self.template_name, context)


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



