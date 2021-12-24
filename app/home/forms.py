from django import forms


class InstanceForm(forms.Form):
    token = forms.CharField(min_length=36, max_length=36)
    location = forms.CharField(max_length=8)
