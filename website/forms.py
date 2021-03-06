from django import forms
from django.contrib.auth.models import User
from website.models import UserProfile
from django.contrib.auth.forms import UserCreationForm



class UserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform avalid email address.')
    password = forms.CharField(widget=forms.PasswordInput())

    allowed = ['itbhu.ac.in', 'iitbhu.ac.in']
    def clean_email(self):

        data = self.cleaned_data['email'].split('@')[-1]
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_no',)

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


