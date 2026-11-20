from django import forms
from .models import Group, BillSpliting
from ledger.models import Contact

# ---------------- CREATE GROUP FORM ----------------

from django import forms
from .models import Group
from ledger.models import Contact


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['members'].queryset = Contact.objects.filter(user=user)


# ---------------- BILL SPLIT FORM ----------------

class BillSplitForm(forms.ModelForm):
    class Meta:
        model = BillSpliting
        fields = ['bill_name', 'total_amount', 'paid_by']

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)

        super().__init__(*args, **kwargs)

        if group:
            self.fields['paid_by'].queryset = group.members.all()