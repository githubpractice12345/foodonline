from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] #ext for extension that takes the extension of the file we upload.Ex: Img.jpg, so index 1 takes 'jpg'.
    print(ext)
    valid_extentions = ['.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extentions:
        raise ValidationError('Unsupported file extensions. Allowed extensions:' +str(valid_extentions)) 