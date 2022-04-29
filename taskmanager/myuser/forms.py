from django import forms
from .models import UserInfo
from django.contrib.auth.models import User


class UserForm(forms.Form):
    '''

    User Form

    '''
    username = forms.CharField(label='Username', min_length=6, max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm'}))

    def clean_username(self):
        '''

        Check if username is exist

        :return: username if check ok,
                 else raise error
        '''
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        '''

        Check if email is exist

        :return: email if check ok,
                 else raise error
        '''
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        #if r.count():
         #   raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        '''

        Check Password
        Compare password with second password

        :return: passwork if check ok
                 else raise error
        '''
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Those passwords didn't match. Try again.")

        return password2

    def save(self, commit=True):
        '''

        Save user to DB

        :return: user object
        '''
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class UserInfoForm(forms.ModelForm):

    '''

    Form for UserInfor Object

    '''
    class Meta:
        model = UserInfo
        fields = ('user_fullname', 'user_description', 'user_avatar')
        widgets = {
            'user_fullname' : forms.TextInput(attrs={'class': 'form-control'}),
            'user_description' : forms.Textarea(attrs={'class': 'form-control', 'rows':'5'}),
            'user_avatar' : forms.FileInput(),
        }
