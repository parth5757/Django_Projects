from django import forms
from django.contrib.auth import get_user_model
from app_modules.vendors.models import Vendor
from phonenumber_field.formfields import PhoneNumberField
from django.forms.widgets import HiddenInput
User = get_user_model()

class VendorCreateForm(forms.ModelForm):

    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={"placeholder": "Phone"}), label=("Phone"), required=False
    )

    class Meta:
        model = Vendor
        fields = ("email", "phone", "first_name", "last_name", "company", "website", "office_number_1", "office_number_2", "address_line_1", "address_line_2", "city", "state", "zip_code", "country", "status")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(VendorCreateForm, self).__init__(*args, **kwargs)

        if self.user.role in [User.COMPANY_ADMIN]:
            self.fields['company'].initial = self.user.company_users.first().company

        self.fields['company'].required = True
        self.fields['address_line_1'].required = True
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['zip_code'].required = True
        self.fields['country'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label
        
        # self.fields["status"].widget.attrs.update({'class' : "mt-1"})

        self.fields["phone"].widget.attrs["type"] = "tel"

        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control company-list"
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control vendor-status"


class VendorUpdateForm(forms.ModelForm):

    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={"placeholder": "Phone"}), label=("Phone"), required=False
    )

    class Meta:
        model = Vendor
        fields = ("email", "phone", "first_name", "last_name", "company", "website", "office_number_1", "office_number_2", "address_line_1", "address_line_2", "city", "state", "zip_code", "country", "status")

    def __init__(self, *args, **kwargs):
        super(VendorUpdateForm, self).__init__(*args, **kwargs)

        self.fields['company'].required = True
        self.fields['address_line_1'].required = True

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = visible.field.label

        self.fields["phone"].widget.attrs["type"] = "tel"
        
        self.fields["status"].widget.attrs["class"] = "select2-data-array form-control vendor-status"
        self.fields["company"].widget.attrs["class"] = "select2-data-array form-control company-list"