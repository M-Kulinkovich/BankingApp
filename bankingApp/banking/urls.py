from django.urls import path

from banking.views import (
    IndexPageView,
    LoginUser,
    RegisterUser,
    LogoutUser,
    AccountPageView,
    TransactionsPageView,
    TransactionsCsvView,
    )

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('account/', AccountPageView.as_view(), name='account'),
    path('transactions/', TransactionsPageView.as_view(), name='transactions'),
    path('transactions_csv/', TransactionsCsvView.as_view(), name='transactions_csv'),
]