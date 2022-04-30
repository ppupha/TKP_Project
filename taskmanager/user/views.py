from django.shortcuts import render, redirect
from django.views import View
from myuser.forms import UserInfoForm, UserForm
from task.views import make_noti
from task.models import Task, Notification
from django.contrib.auth.decorators import login_required



class IndexView(View):
    '''

        Home Page

    '''
    def get(self, request):
        '''

        :param request: GET request
        :return: html for homepage
        '''
        return render(request, 'user/index.html')

class AuthorsView(View):
    '''

    Author Page

    '''
    def get(self, request):
        '''

        :param request: GET request
        :return: html for author page
        '''
        return render(request, 'user/authors.html')

class HelpView(View):
    '''

    Help Page

    '''
    def get(self, request):
        '''

        :param request: GET request
        :return: html for help page
        '''
        return render(request, 'user/help.html')
        
@login_required(login_url='/login/')
def user_profile(request):
    '''

    User Profile Page

    :param request: request form user (it can be GET or POST)
    :return: > if request method is GET, show user profile
             > if request method is POST, update information for user if form data is valid
             - And then back to profile page
    '''
    # Add notification to navbar
    make_noti(request)
    projects = request.user.project_set.all()
    tasks = Task.objects.filter(project__in = list(projects))
    notis = Notification.objects.filter(task__in = list(tasks)).order_by('-id')
    notic_count = len(list(Notification.objects.filter(actived = False)))
    
    # Form edit profile
    form = UserInfoForm(instance=request.user.Info)
    
    data = {"notis": notis, 'form': form, "notic_count": notic_count}
    
    if request.method == "POST":
        form = UserInfoForm(request.POST, request.FILES, instance=request.user.Info)
        if form.is_valid():
            custom_form = form.save(False)
            custom_form.user = request.user
            custom_form.save()
            return redirect('user:user_profile')
        
    return render(request, 'user/user_profile.html', data)