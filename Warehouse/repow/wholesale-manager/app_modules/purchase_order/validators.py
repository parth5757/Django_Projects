import os
from django.core.exceptions import ValidationError


def validate_invoice_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.zip']
    if ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Zip file is not allowed')