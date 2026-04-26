from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
# Create your models here.
class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name  = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
    
class Loan(models.Model):
    DIRECTION_CHOICES = [
        ('lent', 'I lent money'),
        ('borrow', 'I borrowed money'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('overdue', 'Overdue'),
        ('paid', 'Paid Off'),
    ]
    DURATION_CHOICES = [
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='loans')
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    status  = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    principal = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5,decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True)
    duration  = models.PositiveIntegerField(null=True, blank=True)
    duration_type = models.CharField(choices=DURATION_CHOICES, max_length=10, null=True, blank=True)
    description = models.TextField(blank=True)
    loan_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def amount_paid(self):
        return sum(p.amount for p in self.payments.all())
    
    def total_owed(self):
        interest = self.principal * self.interest_rate / 100
        return self.principal + interest
    
    def balance(self):
        return self.total_owed() - self.amount_paid()
    
    def save(self, *args, **kwargs):
        # Calculate due date from duration
        if self.duration and self.duration_type and self.loan_date:
            if self.duration_type == 'days':
                self.due_date = self.loan_date + relativedelta(days=self.duration)
            elif self.duration_type == 'weeks':
                self.due_date = self.loan_date + relativedelta(weeks=self.duration)
            elif self.duration_type == 'months':
                self.due_date = self.loan_date + relativedelta(months=self.duration)
        
        # Auto detect overdue
        if self.due_date and self.status != 'paid':
            if self.due_date < timezone.now().date():
                self.status = 'overdue'
            else:
                self.status = 'active'
    
        super().save(*args, **kwargs)
    
    def is_overdue(self):
        if self.due_date and self.status != 'paid':
            return self.due_date < timezone.now().date()
        return False
    
    def __str__(self):
        return f"{self.direction} - {self.contact.name} - {self.principal}"
    

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check if loan is fully paid after saving this payment
        loan = self.loan
        if loan.balance() <= 0:
            loan.status = 'paid'
            loan.save()
            
    def __str__(self):
        return f"Payment of {self.amount} on {self.date}"