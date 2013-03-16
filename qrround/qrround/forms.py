from django import forms
from qrround.models import Query


class QueryForm(forms.ModelForm):
    CHOICES = (
        ('facebook', 'Facebook',),
        ('google+', 'Google+',),
        ('linkedin', 'LinkedIn',),
        ('linkedin', 'LinkedIn',),
    )
    channel_choice = forms.ChoiceField(
        widget=forms.RadioSelect, choices=CHOICES)
    accept = forms.NullBooleanField(widget=forms.CheckboxInput)

    class Meta:
        model = Query
        fields = ('user', 'text')
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'getqrcode_input',
                'autofocus': 'autofocus',
                'class': 'span5',
                'placeholder': 'Input your data'}),
        }

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['text'].required = True
        self.fields['text'].max_length = 12300
        self.fields['channel_choice'].required = False

    def clean_text(self):
        cleaned_data = super(self.__class__, self).clean()
        if len(cleaned_data.get('text')) > 1000:
            raise forms.ValidationError('Text is too long')
        return cleaned_data

    def clean_accept(self):
        cleaned_data = super(self.__class__, self).clean()
        if not cleaned_data.get('accept'):
            raise forms.ValidationError('You should accept our policy')
        return cleaned_data


class EmptyForm(forms.Form):
    empty = forms.CharField(max_length=100)
