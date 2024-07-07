from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, ListView, TemplateView, View
from django.views.generic.edit import UpdateView, DeleteView, FormView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import Task
class BaseView(LoginRequiredMixin):
    '''Base view here'''
    login_url = '/login/'

class ErrorView(View):
    def get(self, request, undefined_route):
        return render(request, 'common/error.html')

class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

class RegisterUser(CreateView):
        '''Create at User Registration'''
        model = User #model name
        template_name = 'register.html'
        fields = ["username", "email", "password"] #field that want to send from user
        success_url = reverse_lazy('login')
        
        '''check form is valid or not if valid than execute'''
        def form_valid(self, form):
            form.instance.password = make_password(form.cleaned_data['password'])
            form.save()
            return super().form_valid(form)
        
        # to check error
        # def form_invalid(self, form):
        #     for error in form.errors:
        #         print("==> error:", error)
        #     return super().form_invalid(form)


class AddTask(BaseView, CreateView):
     model = Task
     template_name = "add_task.html"
     fields = ["task"]