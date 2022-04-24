from django.shortcuts import render, get_object_or_404, redirect
from models import Project, Task, Notification
from django.views.generic import DetailView, ListView, DeleteView
from django.views import View
from forms import ProjectForm, TaskForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, decorators
from datetime import timedelta, datetime, timezone
from rest_framework.views import APIView


class MyProjects(LoginRequiredMixin, APIView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    # if request.method == "GẺT"
    def get(self, request, str = 'id'):
        projects = request.user.project_set.all().order_by(str)
        # get all notification of user
        make_noti(request)
        tasks = Task.objects.filter(project__in = list(projects))
        notis = Notification.objects.filter(task__in = list(tasks)).order_by('-id')
        notic_count = len(list(Notification.objects.filter(actived = False)))
        data = {"projects": projects, "projectform": ProjectForm, "notis": notis, "notic_count": notic_count}
        return render(request, "task/projects.html", data)

    # if request.method == "POST"
    def post(self, request):
        f = ProjectForm(request.POST)
        if f.is_valid():

            # create new Project with infor from form
            project = Project()
            project.user = request.user
            project.title = f.cleaned_data['title']
            project.save()
            link = "/projects/"
            return HttpResponseRedirect(link)
        else:
            # if form not valid, return to home page
            link = "/projects/"
            return HttpResponseRedirect(link)


@decorators.login_required
def Delete_Project(request, id):
    try:
        # get project need delete
        project = Project.objects.get(id =id)
        if request.method == 'GET':
            project.delete()
            return HttpResponseRedirect("/projects/")
    except:
       return HttpResponse("ERROR: PROJECT NOT FOUND")


