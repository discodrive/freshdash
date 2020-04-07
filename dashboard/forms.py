from django import forms
from dashboard.models import Client, ClientOwner

class LocationFilterForm(forms.ModelForm):
    location = forms.CharField(
        required=False,
        widget=forms.Select(
            choices=[('UK', 'UK'), ('North America', 'North America')],
            attrs={
                'name': 'location',
                'onchange': 'this.form.submit()',
            },
        )
    )

    class Meta:
        model = Client
        fields = ('location',)

class OwnerFilterForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        empty_label='-- Owner --',
        required=False,
        queryset=ClientOwner.objects.all(),
        widget=forms.Select(
            attrs={
                'name': 'owner',
                'onchange': 'this.form.submit()',
            },
        )
    )

    class  Meta:
        model = Client
        fields = ('owner',)
