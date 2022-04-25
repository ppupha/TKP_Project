from django.shortcuts import render, redirect
from django.views import View
from myuser.forms import UserInfoForm, UserForm
from task.views import make_noti
from task.models import Task, Notification
from django.contrib.auth.decorators import login_required



class IndexView(View):
    def get(self, request):
        return render(request, 'user/index.html')

class AuthorsView(View):
    def get(self, request):
        return render(request, 'user/authors.html')


@login_required(login_url='/login/')
def user_profile(request):
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