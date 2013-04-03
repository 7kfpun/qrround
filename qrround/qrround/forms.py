from captcha.fields import ReCaptchaField
from django import forms
from django.utils import six  # Python 3 compatibility
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from random import choice
mark_safe_lazy = lazy(mark_safe, six.text_type)

from .channels import channels
from .models import (
    Query,
    UserClient,
)

BACKDOOR_KEY = 'kkk'


class LoginForm(forms.Form):
    name = forms.CharField(
        label=u'Your name',
        max_length=100,
        widget=forms.TextInput,
        help_text=_('Your name'),
        required=True,
    )

    password = forms.CharField(
        label=u'Your password',
        max_length=100,
        widget=forms.TextInput,
        help_text=_('Your password'),
        required=True,
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_('Name'),
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': _('Your name is...')}),
        required=True,
    )

    email = forms.EmailField(
        label=_('E-mail'),
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': _('Your E-mail is...')}),
        required=True,
    )

    topic = forms.CharField(
        label=_('Topic'),
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': _('Your topic is...')}),
        required=True,
    )

    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea(attrs={
            'placeholder': _('And leave your message here...')}),
        required=True,
    )

    captcha = ReCaptchaField(attrs={'theme': 'clean'})


class QueryForm(forms.ModelForm):
    backdoor = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('Still in Beta now.')}),
        required=False,
    )

    CHANNEL_CHOICES = (
        ('0', '<< Empty >>',),
    )
    channel_choice = forms.MultipleChoiceField(
        label=_('Channel choice'),
        widget=forms.CheckboxSelectMultiple,
        choices=CHANNEL_CHOICES,
        required=True,
    )

    ERROR_CORRECT = (
        ('ERROR_CORRECT_L', mark_safe_lazy(_('Low (7 &#37; of codewords can be restored)'))),  # noqa
        ('ERROR_CORRECT_M', mark_safe_lazy(_('Medium (15 &#37; of codewords can be restored)'))),  # noqa
        ('ERROR_CORRECT_Q', mark_safe_lazy(_('Quartile (25 &#37; of codewords can be restored)'))),  # noqa
        ('ERROR_CORRECT_H', mark_safe_lazy(_('High (30 &#37; of codewords can be restored)'))),  # noqa
    )
    error_correct_choice = forms.ChoiceField(
        label=_('Error correct choice'),
        widget=forms.RadioSelect, choices=ERROR_CORRECT, required=True)

    accept = forms.NullBooleanField(
        label=_('I have read and accept'),
        widget=forms.CheckboxInput,
        help_text=_('Privacy Policy and Terms of Service'),  # noqa
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

    auto_post_facebook = forms.NullBooleanField(
        label=_('Auto facebook post'),
        widget=forms.CheckboxInput,
        initial=True,
        help_text=_('Auto post the code to your Facebook wall (only when you have a Facebook account)'),  # noqa
    )

    STYLE_CHOICES = (
        ('0', '0',),
        ('1', '1',),
        ('2', '2',),
        ('3', '3',),
    )
    style = forms.ChoiceField(
        label=_('Auto post'),
        widget=forms.RadioSelect,
        choices=STYLE_CHOICES,
        required=True,
        initial='0',
        help_text=_('Set your style here...(more to come)'),
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

        self.fields['channel_choice'].choices = (
            (
                client,
                mark_safe_lazy(
                    _(' <img src="%(profile_picture_url)s" height="50" width="50" /> %(username)s from %(channel)s') % {  # noqa
                        'profile_picture_url': UserClient.objects.get(client=client).profile_picture_url,  # noqa
                        'username': UserClient.objects.get(client=client).username,  # noqa
                        'channel': channel.capitalize(),
                    }
                )
            )
            for channel in channels if channel in session
            for client in session[channel]
        )
        if self.fields['channel_choice'].choices:
            self.fields['text'].initial = UserClient.objects.get(
                client=choice(self.fields['channel_choice'].choices)[0]).url  # noqa

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
            raise forms.ValidationError(_('You should accept our Privacy Policy and Terms of Service'))  # noqa
        return cleaned_data

    def clean_backdoor(self):
        cleaned_data = super(self.__class__, self).clean()
        if cleaned_data.get('backdoor') != BACKDOOR_KEY:
            raise forms.ValidationError(
                _('Sorry, our service is not available now'))
        return cleaned_data
