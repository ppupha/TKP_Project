from django.shortcuts import render, redirect
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, 'user/index.html')

class AuthorsView(View):
    def get(self, request):
        return render(request, 'user/authors.html')