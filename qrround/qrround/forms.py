from django import forms
from django.utils.safestring import mark_safe
from qrround.models import Query
from qrround.channels import channels
from django.utils.translation import ugettext_lazy as _


class QueryForm(forms.ModelForm):
    CHANNEL_CHOICES = (
        ('', '<< Empty >>',),
    )
    channel_choice = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CHANNEL_CHOICES,
        required=True,
    )

    ERROR_CORRECT = (
        ('ERROR_CORRECT_L',
            _('Low 7 percent of codewords can be restored)')),
        ('ERROR_CORRECT_M',
            _('Medium 15 percent of codewords can be restored)')),
        ('ERROR_CORRECT_Q',
            _('Quartile 25 percent of codewords can be restored)')),
        ('ERROR_CORRECT_H',
            _('High 30 percent of codewords can be restored)')),
    )
    error_correct_choice = forms.ChoiceField(
        widget=forms.RadioSelect, choices=ERROR_CORRECT, required=True)

    accept = forms.NullBooleanField(
        widget=forms.CheckboxInput,
        help_text=mark_safe(_('I have read and accept <a id="policy_modal_link" type="button">Privacy Policy and Terms of Service</a>')),  # noqa
    )
    auto_post = forms.NullBooleanField(
        widget=forms.CheckboxInput,
        help_text=_('Post the code to your wall/stream/board'),
        initial=True
    )

    class Meta:
        model = Query
        fields = ('user', 'text')
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'getqrcode_input',
                'autofocus': 'autofocus',
                'class': 'span5',
                'placeholder': _('Input your data')}),
        }

    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session', [])
        super(self.__class__, self).__init__(*args, **kwargs)

        self.fields['text'].required = True
        self.fields['text'].max_length = 2000
        self.fields['error_correct_choice'].initial = 'ERROR_CORRECT_M'

        self.fields['channel_choice'].choices = [
            (client, channel) for channel in channels if channel in session
            for client in session[channel]
        ]
        self.fields['channel_choice'].initial = (
            choice[0] for choice in self.fields['channel_choice'].choices)

    def clean_text(self):
        cleaned_data = super(self.__class__, self).clean()
        if len(cleaned_data.get('text')) > 1000:
            raise forms.ValidationError(_('Text is too long'))
        return cleaned_data

    def clean_accept(self):
        cleaned_data = super(self.__class__, self).clean()
        if not cleaned_data.get('accept'):
            raise forms.ValidationError(_('You should accept our policy'))
        return cleaned_data


class EmptyForm(forms.Form):
    empty = forms.CharField(max_length=100)
