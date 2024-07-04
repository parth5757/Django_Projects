from django import forms
from .models import *
# # from simplemathcaptcha.fields import MathCaptchaField

class StudentRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'nameid'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'id':'emailid'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'id':'passwordid'}),
        }
    # captcha = MathCaptchaField()
        
class TeacherRegistation(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'id':'nameid'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'id':'emailid'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'id':'passwordid'}),
        }


# class StudentRegistration(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password']
#         widgets = {
#             'name': forms.TextInput(attrs={'class':'form-control', 'id':'nameid'}),
#             'email': forms.EmailInput(attrs={'class':'form-control', 'id':'emailid'}),
#             'password': forms.PasswordInput(attrs={'class':'form-control', 'id':'passwordid'}),
#         }

# class TeacherRegistration(forms.ModelForm):
#     class Meta:
#         model = Teacher
#         fields = ['name', 'email', 'password']
#         widgets = {
#             'name': forms.TextInput(attrs={'class':'form-control', 'id':'nameid'}),
#             'email': forms.EmailInput(attrs={'class':'form-control', 'id':'emailid'}),
#             'password': forms.PasswordInput(attrs={'class':'form-control', 'id':'passwordid'}),
#         }
