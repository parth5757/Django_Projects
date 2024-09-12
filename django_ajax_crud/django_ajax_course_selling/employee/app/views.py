from django.shortcuts import render
from .models import OfficeForm, EmployeeForm


def home(request):
    officeForm = OfficeForm()
    employeeForm = EmployeeForm()
    context = {
        "officeForm": officeForm,
        "employeeForm": employeeForm
    }
    return render(request, 'index.html', context)