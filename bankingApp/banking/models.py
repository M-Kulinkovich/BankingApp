from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField('balance', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username}'


class Transfer(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recipient')
    amount = models.DecimalField('amount', max_digits=10, decimal_places=2)
    date = models.DateTimeField('date', auto_now_add=True)
