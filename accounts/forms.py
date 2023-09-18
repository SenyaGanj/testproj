from django.contrib.auth import get_user_model
from django.forms import Form, ModelForm, CharField, EmailField, PasswordInput, EmailInput, ValidationError

User = get_user_model()


class RegisterForm(ModelForm):
    password = CharField(label='Password', widget=PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = CharField(label='Repeat password', widget=PasswordInput(attrs={'class': 'form-control'}))
    email = EmailField(label='Email', widget=EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise ValidationError('Password mismatch.')
        return cd['confirm_password']


class LoginForm(Form):
    email = EmailField(label='Email', widget=EmailInput(attrs={'class': 'form-control'}))
    password = CharField(label='Password', widget=PasswordInput(attrs={'class': 'form-control'}))
