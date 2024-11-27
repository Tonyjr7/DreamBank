from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/<int:account_id>/deposit', views.deposits, name='deposit'),
    path('account/<int:account_id>/withdraw', views.withdraw, name='withdraw'),
    path('account/<int:account_id>/transfer', views.transfer, name='transfer'),
    path('account/<int:account_id>/details', views.account_details, name='account_details'),
    path('account/<int:account_id>/transactions', views.transactions, name='transactions')
]