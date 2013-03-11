from django import forms


class EmptyForm(forms.Form):
    empty = forms.CharField(max_length=100)
