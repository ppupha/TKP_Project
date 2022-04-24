from django.urls import path
from . import views

#it is name_space
app_name = 'task'

urlpatterns = [
    path("projects/", views.MyProjects.as_view(), name ="projects"),
    path("project/<int:id>", views.MyProject.as_view(), name ="project"),
    path("del-project/<int:id>", views.Delete_Project, name ="del-project"),
    path("save-task/<int:id>", views.Save_Task, name ="save-task"),
    path("del-task/<int:id>", views.Delete_Task, name ="del-task"),
    path("done-task/<int:id>", views.Done_Task, name ="done-task"),
]
