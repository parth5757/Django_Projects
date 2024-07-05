import random
import string
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView, View, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from app_modules.company.models import Company, CompanyUsers
from app_modules.users.forms import UserCreateForm, UserUpdateForm, ProfileManageForm
from django_datatables_too.mixins import DataTableMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from app_modules.users.tasks import send_email_notifications


User = get_user_model()

# Create your views here.
class UserListView(LoginRequiredMixin, ListView):
    template_name = "users/user_list.html"
    model = User
    context_object_name = "user_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.all()
        return context
    


class UserCreateView(LoginRequiredMixin, CreateView):
    template_name = "users/user_create.html"
    model = User
    form_class = UserCreateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    # def get_form(self, form_class=None):
    #     form = super(UserCreateView, self).get_form(form_class)
    #     for visible in form.visible_fields():
    #         visible.field.widget.attrs.update({'class': 'form-control'})
    #     return form
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.username = form.cleaned_data["email"].split("@")[0]
        instance.save()
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        instance.set_password(password)
        instance.save()

        target_link = self.request.build_absolute_uri(reverse('account_login'))
        context = {
            "email" : instance.email,
            "password" : password,
            "target_link" : target_link,
        }
        send_email_notifications.delay(
            subject = "Welcome to US Safety!",
            template="users/user_email.html",
            context = context,
            to_emails = [instance.email],
        )

        if self.request.user.role == User.COMPANY_ADMIN:
            company = self.request.user.company_users.first().company
            CompanyUsers.objects.create(
                company = company,
                user = instance
            )
        else:
            company_id = form.data.get("company")
            if company_id:
                company = Company.objects.get(id=company_id)
                CompanyUsers.objects.create(
                    company = company,
                    user = instance
                )

        messages.add_message(self.request, messages.SUCCESS, "User Created Successfully.")
        return HttpResponseRedirect(reverse("users:user_list"))

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/user_update.html"
    model = User
    form_class = UserUpdateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()

        company_id = form.data.get("company")
        if company_id:
            company = Company.objects.get(id=company_id)
            if 'company' in form.changed_data:
                company_user = CompanyUsers.objects.filter(user=instance).first()
                if company_user:
                    company_user.company = company
                    company_user.save()
                else:
                    CompanyUsers.objects.create(
                        company = company,
                        user = instance
                    )
        else:
            CompanyUsers.objects.filter(user=instance).delete()

        messages.add_message(self.request, messages.SUCCESS, "User Updated Successfully.")
        return HttpResponseRedirect(reverse("users:user_list"))


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse("users:user_list"))


class UserDataTablesAjaxPagination(DataTableMixin,View):
    model= User
    
    def get_queryset(self):
        """Get queryset."""
        qs = User.objects.all()
        if self.request.user.role == User.COMPANY_ADMIN:
            company = list(self.request.user.company_users.all().values_list("company_id", flat=True))
            company_users = list(CompanyUsers.objects.filter(company__id__in=company).values_list("user__id", flat=True))
            qs = qs.filter(id__in=company_users)

        role = self.request.GET.get("role")
        if role:
            qs = qs.filter(role=role)

        company = self.request.GET.get("company")
        if company:
            company_users = list(CompanyUsers.objects.filter(company__id=company).values_list("user_id", flat=True))
            qs = qs.filter(id__in=company_users)
        return qs.order_by("id")

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        # update_url = reverse("users: user_update", kwargs={"pk": obj.id})
        update_url = reverse("users:user_update", kwargs={"pk": obj.id})
        delete_url = reverse("users:user_delete")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.full_name}" style="cursor: pointer;" data-url="{delete_url}" data-id="{obj.id}" title="Delete" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'


    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query

        if self.search:
            return qs.filter(
                Q(full_name__icontains=self.search) |
                Q(email__icontains=self.search)
            )
        return qs
    def prepare_results(self, qs):
        # if self.request.user.role == User.COMPANY_ADMIN:
        #     return [
        #         {
        #             'id': o.id,
        #             'email': o.email,
        #             'full_name': o.full_name,
        #             'phone': o.phone,
        #             'role': o.role.title(),
        #             'actions': self._get_actions(o),
        #         }
        #         for o in qs
        #     ]
        # else:
        return [
            {
                'id': o.id,
                'email': o.email,
                'full_name': o.full_name,
                'phone': o.phone,
                'role': o.role,
                'company': o.company,
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)


class UserDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        user_id = self.request.POST.get("id")
        User.objects.filter(id=user_id).delete()
        return JsonResponse({"message": "User Deleted Successfully."})



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "users/profile_manage.html"
    model = User
    form_class = ProfileManageForm

    success_url = reverse_lazy("users:user_list")