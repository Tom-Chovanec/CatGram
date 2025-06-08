from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3


class CreateUserForm(UserCreationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(action="register"),
        label=""
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(action="login"),
        label=""
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Meno"

    def clean_username(self):
        return self.cleaned_data.get('username')
