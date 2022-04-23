from django.shortcuts import render
from django.views import View
from myuser.forms import UserForm
from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site





# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class SignupView(View):
    """
    Load signup page
    If success == 1 then return successful registration message
    else return registration form
    """
    def get(self, request):
        user_form = UserForm()
        return render(request, 'signup.html', {'user_form': user_form, 'success': 0})

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
            html_content = get_template('registrations/acc_active_email.html').render({
                'user': user,
                'domain': current_site.domain,
                # encode a bytestring version of user's primary key
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # make a token that can be used once to active user
                'token': account_activation_token.make_token(user),
            })
            '''
            email = EmailMultiAlternatives(
                mail_subject, '', to=[to_email]
            )
            # attach a HTML formatted email
            email.attach_alternative(html_content, 'text/html')
            email.send()
            '''
            return render(request, 'signup.html', {'user_form': user_form, 'success': 1,})

        return render(request, 'signup.html', {'user_form': user_form, 'success': 0, })
