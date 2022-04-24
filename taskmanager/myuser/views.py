from django.shortcuts import render, redirect
from django.views import View
from myuser.forms import UserForm
from django.template.loader import get_template

from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.decorators import login_required

from .tokens import account_activation_token

# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

@login_required
def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('user:index')

class SignupView(View):
    """
    Load signup page
    If success == 1 then return successful registration message
    else return registration form
    """
    def get(self, request):
        user_form = UserForm()
        return render(request, 'myuser/signup.html', {'user_form': user_form, 'success': 0})

    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():

            user = user_form.save(commit=False)
            user.is_active = True
            user.save()

            # format activation email
            current_site = get_current_site(request)
            mail_subject = 'Active your account.'
            to_email = user_form.cleaned_data.get('email')
            from_email = "nguyennsangqh@gmail.com"
            html_content = get_template('registrations/acc_active_email.html').render({
                'user': user,
                'domain': current_site.domain,
                # encode a bytestring version of user's primary key
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # make a token that can be used once to active user
                'token': account_activation_token.make_token(user),
            })

            email = EmailMultiAlternatives(
                mail_subject, '', to=[to_email]
            )
            # attach a HTML formatted email
            email.attach_alternative(html_content, 'text/html')
            email.send()

            return render(request, 'myuser/signup.html', {'user_form': user_form, 'success': 1,})

        return render(request, 'myuser/signup.html', {'user_form': user_form, 'success': 0, })

class LoginClass(View):
    """
    Load login page
    If user is authenticated then redirect to task:projects page
    else return the corresponding errors
    - Password is not correct
    - Account is inactive
    - Username does not exist
    """
    def get(self, request):
        return render(request, 'myuser/login.html', {'mode': 0})

    def post(self, request):
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        # return a user if both username and password are valid

        user = authenticate(username=user_name, password=pass_word)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('user:index')
        else:
            user = User.objects.filter(username=user_name)
            return render(request, 'myuser/login.html', {'user': user, 'mode': 1})


class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            # Decode a base64 encoded string. The received data is a user's primary key
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        # if user exists and check_token is correct then account is successful activated
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registrations/acc_active_invalid.html')

class PasswordChangeView_(auth_views.PasswordChangeView):
    success_url = reverse_lazy('myuser:password_change_done')
    template_name = 'registrations/password_change_form.html'

class PasswordChageDoneView_(auth_views.PasswordChangeDoneView):
    template_name = 'registrations/password_change_done.html'

class PasswordResetView_(auth_views.PasswordResetView):
    subject_template_name = 'registrations/password_reset_subject.txt'
    template_name = 'registrations/password_reset_form.html'
    success_url = reverse_lazy('myuser:password_reset_done')
    email_template_name = 'registrations/password_reset_email.html'
    html_email_template_name = email_template_name

class PasswordResetDoneView_(auth_views.PasswordResetDoneView):
    template_name = 'registrations/password_reset_done.html'

class PasswordResetConfirmView_(auth_views.PasswordResetConfirmView):
    template_name = 'registrations/password_reset_confirm.html'
    success_url = reverse_lazy('myuser:password_reset_complete')

class PasswordResetCompleteView_(auth_views.PasswordResetCompleteView):
    template_name = 'registrations/password_reset_complete.html'
