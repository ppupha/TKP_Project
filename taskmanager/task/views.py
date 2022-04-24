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


class  MyProject(LoginRequiredMixin, APIView):

    # if request.method == "GET"
    def get(self, request, id):
        project = Project.objects.get(id = id)
        tasks = list(project.task_set.all())
        taskforms = []
        modes = []
        for task in tasks:
            data = {'title': task.title,
                    'description': task.description,
                    'deadline': task.deadline,
                    }
            taskform = TaskForm(data)
            taskforms.append(taskform)
            # Get color for task
            if task.done:# task is completed
                modes.append("#28a745")#green
            elif task.deadline - datetime.now(timezone.utc) - timedelta(hours = 3) > timedelta(days = 3): # > 3 days from deadline 
                modes.append("#4d8096")#blue
            elif task.deadline - datetime.now(timezone.utc) - timedelta(hours = 3) > timedelta(0): # > deadline
                modes.append("#FFC107") #yellow
            else: # < 3 days from deadline
                modes.append("#DC3545") #red
        # create notifications
        make_noti(request)
        tsks = Task.objects.filter(project__in = list(request.user.project_set.all()))
        notis = Notification.objects.filter(task__in = list(tsks)).order_by('-id')
        for noti in notis:
            if noti.task.project.id == project.id:
                noti.actived = True
                noti.save()
        notic_count = len(list(Notification.objects.filter(actived = False)))
        
        tasks = [{'id': tasks[i].id, 'taskmodel': tasks[i], 'taskform': taskforms[i], 'mode': modes[i]} for i in range(len(tasks))]
        data = {"project": project, "tasks": tasks, "taskform": TaskForm, 'notis': notis, 'notic_count': notic_count}

        return render(request, "task/project.html", data)
        
    # if method == "POST"
    def post(self, request, id):
        f = TaskForm(request.POST)
        if f.is_valid():
            task = Task()
            task.project = Project.objects.get(id = id)
            task.title = f.cleaned_data['title']
            task.description = f.cleaned_data['description']
            task.deadline = f.cleaned_data['deadline']
            task.save()
            link = "/project/{}".format(id)
            return HttpResponseRedirect(link)
        else:
            link = "/project/{}".format(id)
            return HttpResponseRedirect(link)

@decorators.login_required
def Delete_Task(request, id):
    try:
        if request.method == 'GET':
            task = Task.objects.get(id = id)
            # delete task
            task.delete()
            link = '/project/{}'.format(task.project.id)
            return HttpResponseRedirect(link)
    except:
        return HttpResponse("ERROR: TASK NOT FOUND")

@decorators.login_required
def Save_Task(request, id):
    if request.method == "POST":
        # get data from request
        f = TaskForm(request.POST)
        if f.is_valid():
            task = Task.objects.get(id = id)
            task.title = f.cleaned_data['title']
            task.description = f.cleaned_data['description']
            task.deadline = f.cleaned_data['deadline']
            task.noti = '000'
            task.save()
            link = "/project/{}".format(task.project.id)
            return HttpResponseRedirect(link)
    else:
        return HttpResponse("ERROR: TASK NOT FOUND")

@decorators.login_required
def Done_Task(request, id):
    try:
        if request.method == "GET":
            task = Task.objects.get(id = id)
            # task had been done
            task.done = True
            task.completed_day = datetime.now()
            task.save()
            link = '/project/{}'.format(task.project.id)
            return HttpResponseRedirect(link)
    except:
        return HttpResponse("ERROR: TASK NOT FOUND")