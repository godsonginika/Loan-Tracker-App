from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Contacts
    path('contact/', views.ContactListView.as_view(), name='contact_list'),
    path('contact/add/', views.ContactCreateView.as_view(), name='create_contact'),
    path('contact/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('contact/<int:pk>/edit/', views.ContactUpdateView.as_view(), name='edit_contact'),
    path('contact/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='delete_contact'),
    
    # Loans
    path('loan/', views.LoanListView.as_view(), name='loan_list'),
    path('loan/add/', views.LoanCreateView.as_view(), name='add_loan'),
    path('loan/<int:pk>/', views.LoanDetailView.as_view(), name='loan_detail'),
    path('loan/<int:pk>/edit/', views.LoanUpdateView.as_view(), name='edit_loan'),
    path('loan/<int:pk>/delete/', views.LoanDeleteView.as_view(), name='delete_loan'),
    
    # Payment
    path('loan/<int:pk>/payment/add/', views.PaymentCreateView.as_view(), name='add_payment'),
    path('payment/<int:pk>/edit/', views.PaymentUpdateView.as_view(), name='edit_payment'),
    path('payment/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='delete_payment'),
    
]