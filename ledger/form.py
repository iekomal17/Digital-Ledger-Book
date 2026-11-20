from django import forms
from .models import Transaction, Contact


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['contact', 'amount', 'transaction_type', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Show only logged-in user's contacts
        self.fields['contact'].queryset = Contact.objects.filter(user=user)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email']
