from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from app_modules.company.models import Company
from allauth.account.forms import LoginForm
from allauth.account.adapter import get_adapter
from allauth.account import app_settings

User = get_user_model()

class UserCreateForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)

    # password = forms.CharField(widget=forms.PasswordInput, label=("Password"), required=True, validators=[validate_password])
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={"placeholder": "Phone"}), label=("Phone"), required=False
    )

    class Meta:
        model = User
        fields = ("email", "full_name", "phone", "role", "company")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserCreateForm, self).__init__(*args, **kwargs)

        if self.user.role == User.COMPANY_ADMIN:
            self.fields["role"].choices = [
                (User.COMPANY_ADMIN, "Company Admin"),
                (User.SALES_REPRESENTATIVE, "Sales Representative"),
                (User.DRIVER, "Driver"),
            ]

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label

        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control company-list"
        self.fields["role"].widget.attrs["class"] = "select2-data-array form-control user-role"
        self.fields["phone"].widget.attrs["type"] = "tel"

    def clean_company(self):
        company = self.cleaned_data["company"]
        role = self.cleaned_data["role"]
        if role in [User.COMPANY_ADMIN, User.SALES_REPRESENTATIVE, User.DRIVER] and (self.user.role in [User.SUPER_ADMIN]):
            if not company:
                raise ValidationError("This field is required.")
        return company


class UserUpdateForm(forms.ModelForm):
    
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)
    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={"placeholder": "Phone"}), label=("Phone"), required=False
    )

    class Meta:
        model = User
        fields = ("email", "full_name", "phone", "role", "company")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.role in [User.COMPANY_ADMIN, User.SALES_REPRESENTATIVE, User.DRIVER]:
            self.fields['company'].initial = self.instance.company_users.first().company

        if self.user.role == User.COMPANY_ADMIN:
            self.fields["role"].choices = [
                (User.COMPANY_ADMIN, "Company Admin"),
                (User.SALES_REPRESENTATIVE, "Sales Representative"),
                (User.DRIVER, "Driver"),
            ]

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label

        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control company-list"
        self.fields["role"].widget.attrs["class"] = "select2-data-array form-control user-role"


    def clean_company(self):
        company = self.cleaned_data["company"]
        role = self.cleaned_data["role"]
        if role in [User.COMPANY_ADMIN, User.SALES_REPRESENTATIVE, User.DRIVER] and (self.user.role in [User.SUPER_ADMIN]):
            if not company:
                raise ValidationError("This field is required.")
        return company


class CustomLoginForm(LoginForm):
    def clean(self):
        super(LoginForm, self).clean()
        if self._errors:
            return
        credentials = self.user_credentials()
        user_obj = User.objects.filter(email = self.cleaned_data["login"]).first()
        if user_obj:
            if user_obj.role not in [User.SUPER_ADMIN, User.COMPANY_ADMIN]:
                raise forms.ValidationError("You can't access this site")
        user = get_adapter(self.request).authenticate(self.request, **credentials)
        if user:
            self.user = user
        else:
            auth_method = app_settings.AUTHENTICATION_METHOD
            if auth_method == app_settings.AuthenticationMethod.USERNAME_EMAIL:
                login = self.cleaned_data["login"]
                if self._is_login_email(login):
                    auth_method = app_settings.AuthenticationMethod.EMAIL
                else:
                    auth_method = app_settings.AuthenticationMethod.USERNAME
            raise forms.ValidationError(
                self.error_messages["%s_password_mismatch" % auth_method]
            )
        return self.cleaned_data
    
class ProfileManageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("email", "full_name", "phone", "role")

    def __init__(self, *args, **kwargs):
        super(ProfileManageForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        self.fields["role"].disabled = True
        self.fields["email"].widget.attrs["readonly"] = True