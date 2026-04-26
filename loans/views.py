from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Contact, Loan, Payment
from .forms import ContactForm, LoanForm, PaymentForm
from django.db.models import Sum

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid:
            user = form.save()
            return HttpResponse('User Created Successfully!')
    else:
        form = RegisterUser(request.POST)

    return render(request, 'loans/register.html', {'form' : form})

# --------------------------------------------------------------------------------
# CLASS-BASED VIEWS
# region Contact Views
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'loans/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'loans/contact_detail.html'
    context_object_name = 'contact'

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)
    
class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'loans/contact_form.html'
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'loans/contact_form.html'
    success_url = reverse_lazy('contact_list')

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)
    
class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'loans/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)
# endregion

# region Loan Views
class LoanListView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = 'loans/loan_list.html'
    context_object_name = 'loans'

    def get_queryset(self):
        return Loan.objects.filter(owner=self.request.user).exclude(status='paid')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paid_loans'] = Loan.objects.filter(owner=self.request.user, status='paid')
        return context

class LoanDetailView(LoginRequiredMixin, DetailView):
    model = Loan
    template_name = 'loans/loan_detail.html'
    context_object_name = 'loan'

    def get_queryset(self):
        return Loan.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payments'] = self.object.payments.all()
        return context
    
class LoanCreateView(LoginRequiredMixin, CreateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loans/loan_form.html'
    success_url = reverse_lazy('loan_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class LoanUpdateView(LoginRequiredMixin, UpdateView):
    model = Loan
    form_class = LoanForm
    template_name = 'loans/loan_form.html'
    success_url = reverse_lazy('loan_list')

    def get_queryset(self):
        return Loan.objects.filter(owner=self.request.user)

class LoanDeleteView(LoginRequiredMixin, DeleteView):
    model = Loan
    template_name = 'loans/loan_confirm_delete.html'
    success_url = reverse_lazy('loan_list')

    def get_queryset(self):
        return Loan.objects.filter(owner=self.request.user)
# endregion

# region Payment Views
class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'loans/payment_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.loan = get_object_or_404(Loan, pk=self.kwargs['pk'], owner=self.request.user)
        kwargs['loan'] = self.loan
        return kwargs
    
    def form_valid(self, form):
        loan = get_object_or_404(Loan, pk=self.kwargs['pk'], owner=self.request.user)
        form.instance.loan = loan
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('loan_detail', kwargs={'pk':self.kwargs['pk']})

class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'loans/payment_form.html'
    
    def get_queryset(self):
        return Payment.objects.filter(loan__owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('loan_detail', kwargs={'pk':self.object.loan.pk})
    
class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'loans/payment_confirm_delete.html'

    def get_queryset(self):
        return Payment.objects.filter(loan__owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('loan_detail', kwargs={'pk':self.object.loan.pk})

# endregion

@login_required
def dashboard(request):
    loans = Loan.objects.filter(owner=request.user)
    
    total_lent = loans.filter(direction='lent').aggregate(Sum('principal'))['principal__sum'] or 0
    total_borrowed = loans.filter(direction='borrow').aggregate(Sum('principal'))['principal__sum'] or 0
    active_loans = loans.filter(status='active').count()
    overdue_loans = [loan for loan in loans if loan.is_overdue()]

    context = {
        'total_lent': total_lent,
        'total_borrow': total_borrowed,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
        'recent_loans': loans.order_by('-created_at')[:5]
    }
    return render(request, 'loans/dashboard.html', context)
# ------------------------------------------------------------------------
''' FUNCTION-BASED VIEWS
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contact, Loan, Payment
from .forms import ContactForm, LoanForm, PaymentForm

@login_required
def contact_list(request):
    contacts = Contact.objects.filter(owner=request.user)
    return render(request, 'loans/contact_list.html', {'contacts':contacts})

@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid:
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'loan/contact_form.html', {'form':form})

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    loans = contact.loans.all()
    return render(request, 'loans/contact_detail.html', {'contact': contact, 'loans': loans})

@login_required
def update_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid:
            form.save()
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'loans/contact_form.html', {'form':form})

@login_required
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)
    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')
    return render(request, 'loans/contact_delete.html', {'contact':contact})
        '''