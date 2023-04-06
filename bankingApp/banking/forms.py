from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField, DecimalField

from .models import Transfer, Account


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TransferForm(ModelForm):
    class Meta:
        model = Transfer
        fields = ['recipient', 'amount']

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender')
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = Account.objects.exclude(user=self.sender.user)


class AddMoneyForm(ModelForm):
    class Meta:
        model = Transfer
        fields = ['recipient', 'amount']

    recipient = ModelChoiceField(queryset=Account.objects.all())
    amount = DecimalField(max_digits=10, decimal_places=2)
