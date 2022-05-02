from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Notification
from django.views.generic import DetailView, ListView, DeleteView
from django.views import View
from .forms import ProjectForm, TaskForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, decorators
from datetime import timedelta, datetime, timezone
from rest_framework.views import APIView
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site




def send_mail_notif(task, msg, domain):
    mail_subject = "Task Notif"
    project = task.project
    user = project.user
    to_email = user.email
    html_content = get_template('task/email_notif.html').render({
        'username': user.username,
        'msg': msg,
        'task': task,
        'project': project,
        'domain': domain,
    })

    email = EmailMultiAlternatives(
        mail_subject, '', to=[to_email]
    )
    # attach a HTML formatted email
    email.attach_alternative(html_content, 'text/html')
    email.send()

def update_notif(domain = '', user = None):
    if (user == None):
        projects = project.objects.all()
    else:
        projects = user.project_set.all()

    for project in projects:
        # get all task of a projects
        tasks = project.task_set.all()
        for task in tasks:
            if not task.done:
                count += 1
                # create a new Model
                noti = Notification()
                noti.task = task
                # if closed to deadline 5 day
                if (task.deadline - datetime.now(timezone.utc) - timedelta(hours=3) < timedelta(0)) and (
                        task.noti[0] == '0'):
                    noti.content = 'The deadline is already over'
                    noti.save()
                    task.noti = '1{}{}'.format(task.noti[1], task.noti[2])
                    send_mail_notif(domain=domain, msg=noti.content, task = task)
                # if out ò deadline
                elif (timedelta(0) < task.deadline - datetime.now(timezone.utc) - timedelta(hours=3) < timedelta(
                        days=5)) and (task.noti[1] == '0'):

                    noti.content = '5 day left '
                    noti.save()
                    task.noti = task.noti[0] + '1' + task.noti[2]
                    send_mail_notif(domain=domain, msg=noti.content, task = task)
                task.save()
    return count


def make_noti(request):
    '''
    Create notifications for all projects
    :param request: get request from user
    :return: number of notifications
    '''
    count = 0
    current_site = get_current_site(request)
    domain = current_site.domain
    # get all projects of a users
    projects = request.user.project_set.all()
    for project in projects:
        # get all task of a projects
        tasks = project.task_set.all()
        for task in tasks:
            if not task.done:
                count += 1
                # create a new Model
                noti = Notification()
                noti.task = task
                # if closed to deadline 5 day
                if (task.deadline - datetime.now(timezone.utc) - timedelta(hours=3) < timedelta(0)) and (
                        task.noti[0] == '0'):
                    noti.content = 'The deadline is already over'
                    noti.save()
                    task.noti = '1{}{}'.format(task.noti[1], task.noti[2])
                    send_mail_notif(domain=domain, msg=noti.content, task = task)
                # if out ò deadline
                elif (timedelta(0) < task.deadline - datetime.now(timezone.utc) - timedelta(hours=3) < timedelta(
                        days=5)) and (task.noti[1] == '0'):

                    noti.content = '5 day left '
                    noti.save()
                    task.noti = task.noti[0] + '1' + task.noti[2]
                    send_mail_notif(domain=domain, msg=noti.content, task = task)
                task.save()
    return count


class MyProjects(LoginRequiredMixin, APIView):
    '''

    Infor about MyProjects Objects (Cout From TZ)

    '''

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    # if request.method == "GẺT"
    def get(self, request, str='id'):
        '''

        GET Method for model MyProjects
        Show all Projects of a user

        :param request: GET request from user
        :param str: sorting order
        :return: sorted list of all Projects,
        '''
        projects = request.user.project_set.all().order_by(str)
        # get all notification of user
        make_noti(request)
        tasks = Task.objects.filter(project__in=list(projects))
        notis = Notification.objects.filter(task__in=list(tasks)).order_by('-id')
        notic_count = len(list(Notification.objects.filter(actived=False)))
        data = {"projects": projects, "projectform": ProjectForm, "notis": notis, "notic_count": notic_count}
        return render(request, "task/projects.html", data)

    # if request.method == "POST"
    def post(self, request):
        '''

        POST method for model MyProjects
        Create a new project

        :param request: POST request from user
        :return: a Project Object is created if form data is valid and then redirect to main page
        '''
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
    '''

    Delete a Project by Id

    :param request:
    :param id: project id
    :return: if projects with id is exist, then delete it and redirect to main page,
             else raise error
    '''
    try:
        # get project need delete
        project = Project.objects.get(id=id)
        if request.method == 'GET':
            project.delete()
            return HttpResponseRedirect("/projects/")
    except:
        return HttpResponse("ERROR: PROJECT NOT FOUND")


class MyProject(LoginRequiredMixin, APIView):
    '''

        Infor about Object PRoject

    '''
    # if request.method == "GET"
    def get(self, request, id):
        '''

        Get Method
        Show all Task in Projects

        :param request: GET request from user
        :param id: id of Project
        :return: tasks and these notifications
        '''
        project = Project.objects.get(id=id)
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
            if task.done:  # task is completed
                modes.append("#28a745")  # green
            elif task.deadline - datetime.now(timezone.utc) - timedelta(hours=3) > timedelta(
                    days=3):  # > 3 days from deadline
                modes.append("#4d8096")  # blue
            elif task.deadline - datetime.now(timezone.utc) - timedelta(hours=3) > timedelta(0):  # > deadline
                modes.append("#FFC107")  # yellow
            else:  # < 3 days from deadline
                modes.append("#DC3545")  # red
        # create notifications
        make_noti(request)
        tsks = Task.objects.filter(project__in=list(request.user.project_set.all()))
        notis = Notification.objects.filter(task__in=list(tsks)).order_by('-id')
        for noti in notis:
            if noti.task.project.id == project.id:
                noti.actived = True
                noti.save()
        notic_count = len(list(Notification.objects.filter(actived=False)))

        tasks = [{'id': tasks[i].id, 'taskmodel': tasks[i], 'taskform': taskforms[i], 'mode': modes[i]} for i in
                 range(len(tasks))]
        data = {"project": project, "tasks": tasks, "taskform": TaskForm, 'notis': notis, 'notic_count': notic_count}

        return render(request, "task/project.html", data)

    # if method == "POST"
    def post(self, request, id):
        '''

        POST method
        Create a new Task into this project

        :param request: POST request from user
        :param id: id of project
        :return: New Task is create if form data is Valid, then redirect bach to Project Page
        '''
        f = TaskForm(request.POST)
        if f.is_valid():
            task = Task()
            task.project = Project.objects.get(id=id)
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
    '''

      Delete a Task from Project

    :param request: request from user
    :param id: Task id
    :return: if Task is exist, delete it and redirect to project page,
             else raise error
    '''
    try:
        if request.method == 'GET':
            task = Task.objects.get(id=id)
            # delete task
            task.delete()
            link = '/project/{}'.format(task.project.id)
            return HttpResponseRedirect(link)
    except:
        return HttpResponse("ERROR: TASK NOT FOUND")


@decorators.login_required
def Save_Task(request, id):
    '''

     POST Method for model Task
     Update Information for Task

    :param request: POST request from user
    :param id: Task id
    :return: if task is exit, update task information with valid data,
             if task didnt found, raise error
    '''
    if request.method == "POST":
        # get data from request
        f = TaskForm(request.POST)
        if f.is_valid():
            task = Task.objects.get(id=id)
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
    '''

    Make Task as Done

    :param request: request from user
    :param id: Task id
    :return: make task as done and direct back to project page
    '''
    try:
        if request.method == "GET":
            task = Task.objects.get(id=id)
            # task had been done
            task.done = True
            task.completed_day = datetime.now()
            task.save()
            link = '/project/{}'.format(task.project.id)
            return HttpResponseRedirect(link)
    except:
        return HttpResponse("ERROR: TASK NOT FOUND")