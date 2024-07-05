from atexit import register
from typing import Any, Dict
from django.db import models
from django.forms import all_valid
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, View, DeleteView
from app_modules.customers.models import Customer, MultipleContact, Payment, SalesRoute, PriceLevel, PriceLevelProduct
from django.urls import reverse_lazy, reverse
from app_modules.customers.forms import CustomerForm, MultipleContactForm, PaymentForm, SalesRouteForm, PriceLevelForm
from extra_views import CreateWithInlinesView, InlineFormSetFactory, NamedFormsetsMixin, UpdateWithInlinesView
from django_datatables_too.mixins import DataTableMixin
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from app_modules.company.models import Company
from app_modules.users.models import User
from django.contrib.messages.views import SuccessMessageMixin
from utils.helpers import get_geo_code_from_address
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from app_modules.product.models import Product


# Create your views here.

'''views for Customer'''
class CustomerListView(LoginRequiredMixin, ListView):
    template_name = "customer/customer_list.html"
    model = Customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.filter(status='active')
        context["status_choices"] = Customer.STATUS_CHOICES
        return context
    

class CustomerDataTablesAjaxPagination(LoginRequiredMixin, DataTableMixin,View):
    model= Customer
    
    def get_queryset(self):  # sourcery skip: extract-duplicate-method
        company_obj = self.request.user.company
        if company_obj is not None:
            return Customer.objects.filter(company__company_name=company_obj)

        #----- dropdown filteration -----
        company = self.request.GET.get("company")
        status_choice = self.request.GET.get("status")
        qs = Customer.objects.all()
        if company:
            company_users = Customer.objects.filter(company__company_name=company)
            qs = qs.filter(id__in=company_users)
            if status_choice:
                status_customer = Customer.objects.filter(status=status_choice)
                qs = qs.filter(id__in=status_customer)
                return qs
            return qs
        if status_choice:
            status_customer = Customer.objects.filter(status=status_choice)
            qs = qs.filter(id__in=status_customer)
            return qs
        # ---end---

        return Customer.objects.all().order_by("id")
    
    def _get_status(self,obj):
        t = get_template("customer/customer_status.html")
        return t.render(
            {"customer": obj, "request": self.request}
        )

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        update_url = reverse("customer:customer_update", kwargs={"pk": obj.id})
        delete_url = reverse("customer:customer_delete")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.customer_name}" data-url="{delete_url}" data-id="{obj.id}" title="Delete" id="delete_btn"  class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'


    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(customer_name__icontains=self.search) |
                Q(customer_type__icontains=self.search)
            )
        return qs
    
    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'customer_name': o.customer_name,
                'customer_type': o.customer_type.title(),
                'company': str(o.company), 
                'status': self._get_status(o),
                'tax_id': o.tax_id,
                'terms': o.terms.title(),
                'store_open_time': o.store_open_time,
                'store_close_time': o.store_close_time,
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)
    
    
class MultipleContactInline(InlineFormSetFactory):
    model = MultipleContact
    form_class = MultipleContactForm
    factory_kwargs = {"extra": 1, "min_num": 0, "validate_min": False}

class CustomerCreateView(SuccessMessageMixin,LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    template_name = "customer/customer_form.html" 
    model = Customer
    form_class = CustomerForm


    inlines = [MultipleContactInline]    
    inlines_names = ["multiplecontacts"]
    
    def form_valid(self, form):  # sourcery skip: use-named-expression
        instance = form.save(commit=False)
        instance.save()
        if self.request.user.role == User.COMPANY_ADMIN:
            instance.company = self.request.user.company_users.first().company
            instance.save()

        billing_address1 = form.cleaned_data["billing_address_line_1"]
        billing_address2 = form.cleaned_data["billing_address_line_2"]
        shipping_address1 = form.cleaned_data["shipping_address_line_1"]
        shipping_address2 = form.cleaned_data["shipping_address_line_2"]

        billing_city = form.cleaned_data["billing_city"]
        billing_state = form.cleaned_data["billing_state"]
        billing_country = form.cleaned_data["billing_country"]
        
        shipping_city = form.cleaned_data["shipping_city"]
        shipping_state = form.cleaned_data["shipping_state"]
        shipping_country = form.cleaned_data["shipping_country"]
        
        billing_location = get_geo_code_from_address(billing_address1, billing_city, billing_state, billing_country)
        if billing_location:
            instance.billing_latitude = billing_location.latitude
            instance.billing_longitude = billing_location.longitude
            instance.save()
            
        shipping_location = get_geo_code_from_address(shipping_address1, shipping_city, shipping_state, shipping_country)
        if shipping_location:
            instance.shipping_latitude = shipping_location.latitude
            instance.shipping_longitude = shipping_location.longitude
            instance.save()

        messages.add_message(self.request, messages.SUCCESS, "Customer Created Successfully.")
        return HttpResponseRedirect(reverse("customer:customer_list"))
    
            
    success_url = reverse_lazy('customer:customer_list')


class CustomerUpdateView(SuccessMessageMixin, LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    template_name = "customer/customer_form.html"
    model = Customer
    form_class = CustomerForm

    inlines = [MultipleContactInline]    
    inlines_names = ["multiplecontacts"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = Company.objects.filter(status='active')

        return context


    def form_valid(self, form):  # sourcery skip: use-named-expression
        instance = form.save(commit=False)
        instance.save()
        if self.request.user.role == User.COMPANY_ADMIN:
            instance.company = self.request.user.company_users.first().company
            instance.save()

        billing_address1 = form.cleaned_data["billing_address_line_1"]
        billing_address2 = form.cleaned_data["billing_address_line_2"]
        shipping_address1 = form.cleaned_data["shipping_address_line_1"]
        shipping_address2 = form.cleaned_data["shipping_address_line_2"]

        billing_city = form.cleaned_data["billing_city"]
        billing_state = form.cleaned_data["billing_state"]
        billing_country = form.cleaned_data["billing_country"]
        
        shipping_city = form.cleaned_data["shipping_city"]
        shipping_state = form.cleaned_data["shipping_state"]
        shipping_country = form.cleaned_data["shipping_country"]
        
        billing_location = get_geo_code_from_address(billing_address1, billing_city, billing_state, billing_country)
        if billing_location:
            instance.billing_latitude = billing_location.latitude
            instance.billing_longitude = billing_location.longitude
            instance.save()
            
        shipping_location = get_geo_code_from_address(shipping_address1, shipping_city, shipping_state, shipping_country)
        if shipping_location:
            instance.shipping_latitude = shipping_location.latitude
            instance.shipping_longitude = shipping_location.longitude
            instance.save()

        messages.add_message(self.request, messages.SUCCESS, "Customer Updated Successfully.")
        return HttpResponseRedirect(reverse("customer:customer_list"))
            
    success_url = reverse_lazy('customer:customer_list')

class CustomerDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        customer_id = self.request.POST.get("id")
        Customer.objects.filter(id=customer_id).delete()
        return JsonResponse({"message": "Customer Deleted Successfully."})


'''views for payment'''

class PaymentListView(LoginRequiredMixin, ListView):
     template_name = "customer/payment_list.html"
     model = Payment

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customers"] = Customer.objects.filter(status='active')
        return context


class PaymentDataTablesAjaxPagination(LoginRequiredMixin, DataTableMixin,View):
    model= Payment
    
    def get_queryset(self):
        """Get queryset."""
        #----- dropdown filteration -----
        customer = self.request.GET.get("customer")
        start_date = self.request.GET.get("from_date")
        end_date = self.request.GET.get("to_date")
        qs = Payment.objects.all()
        if customer:
            customer_users = Payment.objects.filter(customer_name__customer_name=customer)
            qs = qs.filter(id__in=customer_users)
            return qs
        if end_date:
            result_payment = Payment.objects.filter(receive_date__range = [start_date, end_date])
            qs = qs.filter(id__in=result_payment)
            return qs
        # ---end---
        return Payment.objects.all().order_by("id")
    

    def _get_actions(self, obj):
        """Get action buttons w/links."""
        update_url = reverse("customer:payment_update", kwargs={"pk": obj.id})
        delete_url = reverse("customer:payment_delete")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.customer_name}" data-url="{delete_url}" data-id="{obj.id}" title="Delete" id="delete_btn" class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3 "></i></label></center>'


    def filter_queryset(self, qs):
        # sourcery skip: assign-if-exp, reintroduce-else
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(reference_id__icontains=self.search)
            )
        return qs
    
    def prepare_results(self, qs):
        return [
            {
                'id': o.id,
                'receive_date': o.receive_date,
                'entry_date': o.entry_date,
                'customer_name': str(o.customer_name),
                'receive_amount': o.receive_amount,
                'payment_mode': o.payment_mode.title(),
                'check_no': o.check_no,
                'reference_id': o.reference_id,
                'remark': o.remark,
                'actions': self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)
    

class PaymentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "customer/payment_form.html"
    form_class = PaymentForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    success_message = "Payment Created Successfully"

    success_url = reverse_lazy('customer:payment_list')

class PaymentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "customer/payment_form.html"
    model = Payment
    form_class =PaymentForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    success_message = "Payment Updated Successfully"

    success_url = reverse_lazy('customer:payment_list')

class PaymentDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        payment_id = self.request.POST.get("id")
        Payment.objects.filter(id=payment_id).delete()
        return JsonResponse({"message": "Payment Deleted Successfully."})
    

'''views for Sales Route'''

class SalesRouteListView(LoginRequiredMixin, ListView):
    template_name = "customer/sales_route_list.html"
    model = SalesRoute
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sales_rep"] = User.objects.all()
        context["status_choices"] = SalesRoute.STATUS_CHOICES
        return context


class SalesRouteDataTablesAjaxPagination(LoginRequiredMixin, DataTableMixin, View):
    model = SalesRoute

    def get_queryset(self):  # sourcery skip: extract-duplicate-method
    #----- dropdown filteration -----
        sales_rep = self.request.GET.get("sales_rep")
        status_choice = self.request.GET.get("status")
        qs = SalesRoute.objects.all()
        if sales_rep:
            sales_rep_users = SalesRoute.objects.filter(sales_rep__username=sales_rep)
            qs = qs.filter(id__in=sales_rep_users)
            if status_choice:
                status_salesroute = SalesRoute.objects.filter(status=status_choice)
                qs = qs.filter(id__in=status_salesroute)
                return qs
            return qs
        if status_choice:
            status_salesroute = SalesRoute.objects.filter(status=status_choice)
            qs = qs.filter(id__in=status_salesroute)
            return qs
        return qs.order_by("id")
        # ---end---
    
    def _get_actions(self, obj):
        update_url = reverse("customer:sales_route_update", kwargs={"pk":obj.id})
        delete_url = reverse("customer:sales_route_delete")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.route_name}" data-url="{delete_url}" data-url="{delete_url}" data-id="{obj.id}" title="Delete" id="delete_btn"  class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'
    
    def filter_queryset(self, qs):
        # sourcery skip: assign-if-exp, reintroduce-else
        if self.search:
            return qs.filter(
                Q(route_name__icontains=self.search) 
            )
        return qs
    
    def _get_status(self,obj):
        t = get_template("customer/customer_status.html")
        return t.render(
            {"customer": obj, "request": self.request}
        )
    
    def prepare_results(self, qs):
        return [
            {
                'id' : o.id,
                'route_name' : o.route_name,
                'sales_rep' : str(o.sales_rep),
                'status' : self._get_status(o),
                'actions' : self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)    
    

class SalesRouteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "customer/sales_route_form.html"
    form_class = SalesRouteForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs
    
    success_message = "Sales Route Created Successfully"
    
    success_url = reverse_lazy('customer:sales_route_list')


class SalesRouteUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "customer/sales_route_form.html"
    model = SalesRoute
    form_class = SalesRouteForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["user"] = self.request.user
        return form_kwargs

    success_message = "Sales Route Updated Successfully"

    success_url = reverse_lazy('customer:sales_route_list')

class SalesRouteDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        sales_route_id = self.request.POST.get("id")
        SalesRoute.objects.filter(id=sales_route_id).delete()
        return JsonResponse({"message": "Sales Route Deleted Successfully."})
    

'''views for Price Level'''

class PricelevelListView(LoginRequiredMixin, ListView):
    template_name = "customer/price_level_list.html"
    model = PriceLevel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customer_type"] = PriceLevel.TYPE_CHOICES
        context["status_choices"] = PriceLevel.STATUS_CHOICES
        context["company"] = Company.objects.all()
        return context

class PricelevelDataTablesAjaxPagination(LoginRequiredMixin, DataTableMixin, View):
    model = PriceLevel

    def get_queryset(self):  # sourcery skip: extract-duplicate-method
        #----- dropdown filteration -----
        customer_type = self.request.GET.get("customer_type")
        status_choice = self.request.GET.get("status")
        company_choice = self.request.GET.get("company")
        qs = PriceLevel.objects.all()
        if customer_type:
            customer_type_pricelevel = PriceLevel.objects.filter(customer_type=customer_type)
            qs = qs.filter(id__in=customer_type_pricelevel)
            if status_choice:
                status_pricelevel = PriceLevel.objects.filter(status=status_choice)
                qs = qs.filter(id__in=status_pricelevel)
                return qs
            return qs
        if status_choice:
            status_pricelevel = PriceLevel.objects.filter(status=status_choice)
            qs = qs.filter(id__in=status_pricelevel)
            return qs
        if company_choice:
            company_pricelevel = PriceLevel.objects.filter(company__company_name=company_choice)
            qs = qs.filter(id__in=company_pricelevel)
            return qs
        return qs.order_by("id")
        # ---end---
    
    def _get_actions(self, obj):
        update_url = reverse("customer:price_level_update", kwargs={"pk":obj.id})
        delete_url = reverse("customer:price_level_delete")
        return f'<center><a href="{update_url}" title="Edit"><i class="ft-edit font-medium-3 mr-2"></i></a> <label data-title="{obj.price_level}" data-url="{delete_url}" data-url="{delete_url}" data-id="{obj.id}" title="Delete" id="delete_btn"  class="danger p-0 ajax-delete-btn"><i class="ft-trash font-medium-3"></i></label></center>'
    
    def filter_queryset(self, qs):
        # sourcery skip: assign-if-exp, reintroduce-else
        if self.search:
            return qs.filter(
                Q(price_level__icontains=self.search) 
            )
        return qs
    
    def _get_status(self,obj):
        t = get_template("customer/customer_status.html")
        return t.render(
            {"customer": obj, "request": self.request}
        )
    
    
    def prepare_results(self, qs):
        return [
            {
                'id' : o.id,
                'price_level' : o.price_level,
                'customer_type' : o.customer_type.title(),
                'company' : str(o.company),
                'status' : self._get_status(o),
                'actions' : self._get_actions(o),
            }
            for o in qs
        ]

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)    
   
class PricelevelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "customer/price_level_form.html"
    form_class = PriceLevelForm

    success_message = "Price Level Created Successfully"
    

    # def form_valid(self, form):  # sourcery skip: use-named-expression
    #     instance = form.save(commit=False)
    #     if self.request.user.role == User.COMPANY_ADMIN:
    #         company = self.request.user.company_users.first().company
    #         PriceLevel.objects.create(
    #             company = company,
    #             user = instance
    #         )
    #     else:
    #         company_id = form.data.get("company")
    #         if company_id:
    #             company = Company.objects.get(id=company_id)
    #             PriceLevel.objects.create(
    #                 company = company,
    #                 customer_type = instance.customer_type,
    #                 price_level = instance,
    #                 status = instance.status,
    #             )
    #     messages.add_message(self.request, messages.SUCCESS, "Price Level Created Successfully.")
    #     return HttpResponseRedirect(reverse("customer:price_level_list"))

    success_url = reverse_lazy('customer:price_level_list')

class PricelevelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "customer/price_level_form.html"
    model = PriceLevel
    form_class = PriceLevelForm

    success_message = "Price Level Updated Successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.all()
        return context

    success_url = reverse_lazy('customer:price_level_list')

class PricelevelDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        price_level_id = self.request.POST.get("id")
        PriceLevel.objects.filter(id=price_level_id).delete()
        return JsonResponse({"message": "Price Level Deleted Successfully."})
    

'''views for custom price of product'''
class PricelevelProductDataTablesAjaxPagination(LoginRequiredMixin, DataTableMixin, View):
    model = PriceLevelProduct

    def get_queryset(self):
        qs = PriceLevelProduct.objects.all()
        price_level = self.request.GET.get("price_level")
        if price_level:
            qs = qs.filter(price_level__id=price_level)
        return qs
    
    def _get_input(self, obj):
        t = get_template("customer/custom_input.html")
        return t.render(
            {"price_level_product": obj}
        )
    
    def _get_actions(self, obj):
        save_url = reverse("customer:price_level_product_update")
        return f'<button data-url="{save_url}" data-id="{obj.id}" class="btn btn-primary submit-customer-price" >Save</button>'
 

    def filter_queryset(self, qs):
        # sourcery skip: assign-if-exp, reintroduce-else
        if self.search:
            return qs.filter(
                Q(unit_type__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        data=[]
        for o in qs:
                data.append(
                    {
                        'id' : o.id,
                        'product' : str(o.product),
                        'unit_type' : o.unit_type,
                        'min_price' : o.product.wholesale_min_price,
                        'base_price': o.product.wholesale_base_price,
                        'custom_price' : self._get_input(o),
                        'action' : self._get_actions(o),
                    }
                )        
        return data
    
    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        return JsonResponse(context_data)
    

class PricelevelProductUpdateDataTablesAjaxPagination(LoginRequiredMixin, View):
    def post(self, request):

        custom_price = self.request.POST.get("custom_price")
        price_level_product_id = self.request.POST.get("id")
        
        if price_level_product_id:
            object = PriceLevelProduct.objects.get(id=price_level_product_id)
            object.custom_price = custom_price
            object.save()
            return JsonResponse({"message": "Custom Price Updated Successfully."})