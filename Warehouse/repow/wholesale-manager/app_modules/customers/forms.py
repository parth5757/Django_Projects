from django import forms
from app_modules.customers.models import Customer, MultipleContact, Payment, SalesRoute, PriceLevel, PriceLevelProduct
from phonenumber_field.formfields import PhoneNumberField
from app_modules.company.models import Company
from app_modules.users.models import User


'''form for Customer'''
class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'

        
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = self.fields['company'].queryset.exclude(status=Company.IS_INACTIVE)
        
        self.fields['billing_address_line_2'].required = False
        self.fields['shipping_address_line_2'].required = False

        
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        self.fields["customer_type"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["terms"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["sales_rep"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control select2-list"




'''form for Multiple Contact''' 
class MultipleContactForm(forms.ModelForm):

    mobile_no = PhoneNumberField(
        widget=forms.TextInput(attrs={"placeholder": "Mobile No"}), label=("Mobile No"), required=False
    )
    class Meta:
        model = MultipleContact
        fields = [
            "customer_obj",
            "type",
            "contact_person",
            "email",
            "mobile_no",
            "is_default",
        ]

    def __init__(self, *args, **kwargs):
        super(MultipleContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        self.fields['customer_obj'].required = False
        self.fields['is_default'].widget.attrs = {'class': 'mt-2',}
        self.fields["type"].widget.attrs["class"] = "select2-data-array form-control"



'''form for Payment Route'''
class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        if user.role == User.COMPANY_ADMIN:
            self.fields["customer_name"].queryset = Customer.objects.filter(company__id=user.get_company_id)
            

        self.fields['customer_name'].queryset = self.fields['customer_name'].queryset.exclude(status=Customer.INACTIVE)
        

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        self.fields["payment_mode"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["customer_name"].widget.attrs["class"] = "select2-data-array form-control select2-list"


'''form for Sales Route'''
class SalesRouteForm(forms.ModelForm):
     
    class Meta:
        model = SalesRoute
        fields = '__all__'
    
    def __init__(self, user, *args, **kwargs):
        super(SalesRouteForm, self).__init__(*args, **kwargs)

        if user.role == User.COMPANY_ADMIN:
            self.fields["customer"].queryset = Customer.objects.filter(company__id=user.get_company_id)

        self.fields['customer'].queryset = self.fields['customer'].queryset.exclude(status=Customer.INACTIVE)


        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"    
            visible.field.widget.attrs["placeholder"] = visible.field.label
        self.fields["sales_rep"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["customer"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control select2-list"

'''form for Price Level'''
class PriceLevelForm(forms.ModelForm):
     
    class Meta:
        model = PriceLevel
        fields = '__all__'
    
    def __init__(self,  *args, **kwargs):
        super(PriceLevelForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = self.fields['company'].queryset.exclude(status=Company.IS_INACTIVE)

        

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        self.fields["customer_type"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control select2-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control select2-list"


'''form for PriceLevelProduct'''
class PriceLevelProductForm(forms.ModelForm):

    class Meta:
        model = PriceLevelProduct
        fields = '__all__'