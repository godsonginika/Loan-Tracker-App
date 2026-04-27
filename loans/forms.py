from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Contact, Loan, Payment

class RegisterUser(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long')
        return name
        
     #  For Bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['contact', 'direction', 'principal',
                 'interest_rate', 'loan_date', 'duration', 
                 'duration_type', 'due_date', 'description']
        widgets = {
            'loan_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean_principal(self):
        principal = self.cleaned_data.get('principal')
        if principal <= 0:
            raise forms.ValidationError('Loan amount must be greate than zero.')
        return principal
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        loan_date = self.cleaned_data.get('laon_date')
        if due_date and loan_date and due_date < loan_date:
            raise forms.ValidationError('Due date cannot be before the loan date.')
        return due_date

    # For Bootstrap
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['contact'].queryset = Contact.objects.filter(owner=self.user)
        for field in self.fields.values():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs['class'] = 'form-control'
        self.fields['contact'].widget.attrs['class'] = 'form-select'
        self.fields['direction'].widget.attrs['class'] = 'form-select'
        self.fields['duration_type'].widget.attrs['class'] = 'form-select'
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'date']
        widgets = {
                'date': forms.DateInput(attrs={'type': 'date'}),
            }
    
    def __init__(self, *args, **kwargs):
        self.loan = kwargs.pop('loan', None)
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Payment amount must be greater than zero.')
        if self.loan and amount > self.loan.balance():
            raise forms.ValidationError(f'Amount exceeds remaining balance of {self.loan.balance()}.')
        return amount

    # For Bootstrap
    def __init__(self, *args, **kwargs):
        self.loan = kwargs.pop('loan', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'