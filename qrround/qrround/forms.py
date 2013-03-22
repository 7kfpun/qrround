from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .channels import channels
from .models import Query
from captcha.fields import ReCaptchaField

BACKDOOR_KEY = 'kkk'


class ContactForm(forms.Form):
    name = forms.CharField(
        label=u'Your name',
        max_length=100,
        widget=forms.TextInput,
        help_text=_('Your name'),
        required=True,
    )

    email = forms.EmailField(
        label=u'Your E-mail',
        max_length=200,
        widget=forms.TextInput,
        help_text=_('Your E-mail'),
        required=True,
    )

    message = forms.CharField(
        label=u'Your message',
        widget=forms.Textarea,
        help_text=_('Leave your message here...'),
        required=True,
    )

    captcha = ReCaptchaField(attrs={'theme': 'clean'})


class QueryForm(forms.ModelForm):
    CHANNEL_CHOICES = (
        ('', '<< Empty >>',),
    )
    channel_choice = forms.MultipleChoiceField(
        label=_('Channel choice'),
        widget=forms.CheckboxSelectMultiple,
        choices=CHANNEL_CHOICES,
        required=True,
    )

    ERROR_CORRECT = (
        ('ERROR_CORRECT_L',
            _('Low 7 %(PERCENT_SIGN)s of codewords can be restored)')
            % {'PERCENT_SIGN': '%'}),
        ('ERROR_CORRECT_M',
            _('Medium 15 %(PERCENT_SIGN)s of codewords can be restored)')
            % {'PERCENT_SIGN': '%'}),
        ('ERROR_CORRECT_Q',
            _('Quartile 25 %(PERCENT_SIGN)s of codewords can be restored)')
            % {'PERCENT_SIGN': '%'}),
        ('ERROR_CORRECT_H',
            _('High 30 %(PERCENT_SIGN)s of codewords can be restored)')
            % {'PERCENT_SIGN': '%'}),
    )
    error_correct_choice = forms.ChoiceField(
        label=_('Error correct choice'),
        widget=forms.RadioSelect, choices=ERROR_CORRECT, required=True)

    accept = forms.NullBooleanField(
        label=_('Accept'),
        widget=forms.CheckboxInput,
        help_text=mark_safe(_('I have read and accept <a id="policy_modal_link" type="button">Privacy Policy and Terms of Service</a>')),  # noqa
    )
    auto_post = forms.NullBooleanField(
        label=_('Auto post'),
        widget=forms.CheckboxInput,
        help_text=_('Post the code to your wall/stream/board'),
        initial=True
    )

    color = forms.CharField(
        label=_('Color'),
        widget=forms.TextInput(attrs={
            'class': 'span2',
            'value': 'rgb(0, 0, 0)',
            'readonly': '',
        }),
        help_text=_('Darker is better...'),
    )

    backdoor = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Still in Beta now.')}),
        required=False,
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

    def clean_backdoor(self):
        cleaned_data = super(self.__class__, self).clean()
        if cleaned_data.get('backdoor') != BACKDOOR_KEY:
            raise forms.ValidationError(
                _('Sorry, our service is not available now'))
        return cleaned_data
