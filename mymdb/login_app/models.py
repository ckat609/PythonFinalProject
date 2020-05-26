from django.db import models
import re
from datetime import datetime, date


def years_ago(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29  # can be removed
        return from_date.replace(month=2, day=28,
                                 year=from_date.year-years)


class UserManager(models.Manager):
    def basic_validator(self, postData,):
        age = 13
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if(postData['email_exists'] == True):
            errors['email_exists'] = "Invalid email address: that email address is already in our records."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address: that is an invalid email address."
        if(len(postData['first_name']) < 2):
            errors['first_name'] = "Invalid first name: the first name must be at least two characters long."
        if(len(postData['last_name']) < 2):
            errors['last_name'] = "Invalid last name: the first name must be at least two characters long."
        if(postData['password'] != postData['password_confirm']):
            errors['password'] = "Invalid password: passwords don't match"
        if(len(postData['password']) < 8):
            errors['pw_length'] = "Invalid password: the password must be at least 8 characters long."
        if(not postData['birthday']):
            errors['birthday'] = "Birthday error: the birthday field can't be left empty."
        if(postData['birthday'] >= datetime.now().strftime("%Y-%m-%d")):
            errors['birthday'] = "Birthday error: the birthday can't be set in the future."
        if(datetime.strptime(postData['birthday'], "%Y-%m-%d").date() >= years_ago(age, date.today())):
            errors['birthday'] = f"Age restriction: the user must be at least {age} years old."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
