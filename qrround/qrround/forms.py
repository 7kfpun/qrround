from django import forms
from qrround.models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('user', 'text')


class EmptyForm(forms.Form):
    empty = forms.CharField(max_length=100)
