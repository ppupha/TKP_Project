from django.shortcuts import render, redirect
# from user.forms import UserInfoForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
#from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
#from task.views import make_noti
#from task.models import Task, Project, Notification
from rest_framework.views import APIView

#МЕРЕДОВА
class IndexView(APIView):
    def get(self, request):
        return render(request, 'user/index.html')
