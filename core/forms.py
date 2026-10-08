import re

from django import forms

from .models import Enquiry, ExteriorService, InteriorService

OTHER_SERVICE = 'Other'

# Strict rules — keep in sync with the `rules` object in static/js/main.js.
NAME_MIN, NAME_MAX = 3, 50
MESSAGE_MIN, MESSAGE_MAX = 10, 1000
EMAIL_MAX = 254

NAME_RE = re.compile(r"^[A-Za-z]+(?:[ .'][A-Za-z]+)*\.?$")   # letters, single spaces / dots / apostrophes between
MOBILE_RE = re.compile(r'^[6-9]\d{9}$')                       # Indian mobile: 10 digits starting 6-9
PHONE_INPUT_RE = re.compile(r'^(?:\+91|0)?[6-9]\d{9}$')       # what may be typed (spaces removed)
EMAIL_RE = re.compile(
    r'^[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9])?'
    r'@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,24}$'
)
LINK_RE = re.compile(r'(https?://|www\.|<[^>]+>)', re.I)


def service_choices():
    """Dropdown options built from the Interior and Exterior service cards, plus 'Other'."""
    interior = list(InteriorService.objects.filter(is_active=True).values_list('title', flat=True))
    exterior = list(ExteriorService.objects.filter(is_active=True).values_list('title', flat=True))
    choices = []
    if interior:
        choices.append(('Interior Works', [(t, t) for t in interior]))
    if exterior:
        choices.append(('Exterior & Commercial Works', [(t, t) for t in exterior]))
    choices.append((OTHER_SERVICE, OTHER_SERVICE))
    return choices


class EnquiryForm(forms.ModelForm):
    # Honeypot: moved off-screen with CSS, real visitors leave it empty, bots fill it in.
    website = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'tabindex': '-1', 'autocomplete': 'off'}))

    class Meta:
        model = Enquiry
        fields = ('name', 'phone', 'email', 'service', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Name', 'autocomplete': 'name', 'maxlength': NAME_MAX, 'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone', 'autocomplete': 'tel-national', 'inputmode': 'numeric',
                'maxlength': 10, 'pattern': '[6-9][0-9]{9}', 'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email', 'autocomplete': 'email', 'maxlength': EMAIL_MAX, 'required': True,
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Message', 'rows': 5, 'maxlength': MESSAGE_MAX, 'required': True,
            }),
        }
        error_messages = {
            'name': {'required': 'Please enter your name.'},
            'phone': {'required': 'Please enter your phone number.'},
            'email': {'required': 'Please enter your email.', 'invalid': 'Please enter a valid email address.'},
            'message': {'required': 'Please tell us a little about your space.'},
        }

    def __init__(self, *args, service_placeholder='Service Required', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'] = forms.ChoiceField(
            choices=[('', service_placeholder)] + service_choices(),
            error_messages={'required': 'Please choose the service you need.',
                            'invalid_choice': 'Please choose a service from the list.'},
        )

    def clean_name(self):
        name = ' '.join(self.cleaned_data['name'].split())
        if len(name) < NAME_MIN:
            raise forms.ValidationError(f'Name must be at least {NAME_MIN} characters.')
        if len(name) > NAME_MAX:
            raise forms.ValidationError(f'Name must be under {NAME_MAX} characters.')
        if not NAME_RE.match(name):
            raise forms.ValidationError('Name can only contain letters and spaces.')
        if sum(ch.isalpha() for ch in name) < NAME_MIN:
            raise forms.ValidationError('Please enter your full name.')
        return name

    def clean_phone(self):
        raw = re.sub(r'[\s-]', '', self.cleaned_data['phone'])
        if not PHONE_INPUT_RE.match(raw):
            raise forms.ValidationError('Please enter a valid 10-digit mobile number.')
        digits = raw[-10:]
        if not MOBILE_RE.match(digits) or len(set(digits)) == 1:
            raise forms.ValidationError('Please enter a valid 10-digit mobile number.')
        return digits

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if len(email) > EMAIL_MAX or '..' in email or not EMAIL_RE.match(email):
            raise forms.ValidationError('Please enter a valid email address.')
        return email

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < MESSAGE_MIN:
            raise forms.ValidationError(f'Message must be at least {MESSAGE_MIN} characters.')
        if len(message) > MESSAGE_MAX:
            raise forms.ValidationError(f'Message must be under {MESSAGE_MAX} characters.')
        if len(message.split()) < 2:
            raise forms.ValidationError('Please describe your requirement in a few words.')
        if LINK_RE.search(message):
            raise forms.ValidationError('Links and HTML are not allowed in the message.')
        return message

    @property
    def is_spam(self):
        return bool(self.data.get('website'))
