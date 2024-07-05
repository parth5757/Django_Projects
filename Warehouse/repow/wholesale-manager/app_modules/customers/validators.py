import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png' '.svj']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension. File Extention should be only  .pdf, .doc, .docx, .jpg, .jpeg, .png ')