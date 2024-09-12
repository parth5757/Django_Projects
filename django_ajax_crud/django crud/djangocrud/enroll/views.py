from django.shortcuts import render
from .forms import StudentRegistration
from .models import User, Teacher
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from .forms import StudentRegistration, TeacherRegistation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login, logout

# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.decorators.csrf import csrf_exempt

def error(request,undefined_route):
    return render(request, 'enroll/404.html')

class RegisterTeacher(CreateView):
    model = Teacher
    forms = TeacherRegistation()
    template_name = "enroll/register.html"
    fields = ["name", "email", "password"]
    success_url = reverse_lazy('user-login')

    def form_valid(self, form):
        form.instance.password = set_password(form.cleaned_data['password'])
        form.save()
        return super().form_valid(form)

@login_required
def home(request,):
    form = StudentRegistration()
    stud = User.objects.all()
    return render(request, 'enroll/home.html',{'form':form, 'stu' :stud})

# @csrf_exempt # it make you application as less secure
def save_data(request):
    if request.method == "POST":
        form = StudentRegistration(request.POST)
        if form.is_valid():
            sid = request.POST['stuid']
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            if (sid == ''):
                usr = User.objects.create_user(name= name, email= email, password = password)
            else:
                usr = User.objects.create_user(id=sid, name= name, email= email, password = password)
            usr.save()
            stud = User.objects.values()
            # print(stud)
            student_data = list(stud)
            return JsonResponse({'status': 'save', 'student_data': student_data})
        else:
            return JsonResponse({'status':0})

def delete_data(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        print(id)
        pi = User.objects.get(pk=id)
        pi.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})
    
def edit_data(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        print(id)
        student = User.objects.get(pk=id)
        student_data = {"id": student.id, "name": student.name, "email": student.email, "password": student.password}
        return JsonResponse(student_data)
    

# 

