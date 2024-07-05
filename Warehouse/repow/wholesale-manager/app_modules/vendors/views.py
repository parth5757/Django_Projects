from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, TemplateView, View
from django.urls import reverse_lazy, reverse
from app_modules.company.models import Company
from app_modules.vendors.forms import VendorCreateForm, VendorUpdateForm
from app_modules.vendors.models import Vendor
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django_datatables_too.mixins import DataTableMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


User = get_user_model()

# Create your views here.
class VendorListView(LoginRequiredMixin, ListView):
    template_name = "vendors/vendor_list.html"
    model = Vendor
    context_object_name = "vendor_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.all()
        return context


class VendorCreateView(LoginRequiredMixin, CreateView):
    template_name = "vendors/vendor_create.html"
    model = Vendor
    form_class = VendorCreateForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()

        messages.add_message(self.request, messages.SUCCESS, "Vendor Created Successfully.")
        return HttpResponseRedirect(reverse("vendors:vendor_list"))
    

class VendorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "vendors/vendor_update.html"
    model = Vendor
    form_class = VendorUpdateForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()

        messages.add_message(self.request, messages.SUCCESS, "Vendor Updated Successfully.")
        return HttpResponseRedirect(reverse("vendors:vendor_list"))
    

class VendorDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        vendor_id = self.request.POST.get("id")
        Vendor.objects.filter(id=vendor_id).delete()
        return JsonResponse({"message": "Vendor Deleted Successfully."})


class VendorDataTablesAjaxPagination(DataTableMixin,View):
    model= Vendor
    
    def get_queryset(self):
        """Get queryset."""
        qs = Vendor.objects.all()
        if self.request.user.role == User.COMPANY_ADMIN:
            company = self.request.user.company_users.first().company
            qs = qs.filter(company=company)

        company = self.request.GET.get("company")
        if company:
            qs = qs.filter(company__id=company)
        return qs.order_by("id")

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        # update_url = reverse("users: user_update", kwargs={"pk": obj.id})
        update_url = reverse("vendors:vendor_update", kwargs={"pk": obj.id})
        delete_url = reverse("vendors:vendor_delete")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label style="cursor: pointer;" data-title="{obj.first_name} {obj.last_name}" data-url="{delete_url}" data-id="{obj.id}" title="Delete" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'


    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(first_name__icontains=self.search) |
                Q(last_name=self.search) |
                Q(email__icontains=self.search)
            )
        return qs
    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'email': o.email,
                'first_name': o.first_name,
                'last_name': o.last_name,
                'phone': o.phone,
                'company': o.company.company_name,
                'city': o.city,
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)