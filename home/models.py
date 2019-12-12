# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User,AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date
from .validations import validate_file_extension
import datetime, os

from django.core.files.storage import FileSystemStorage

# Create your models here.

PREFIX_CHOICES = (
    ('MR', 'MR'),
    ('MRS', 'MRS'),
    ('MS', 'MS'),
    ('MX', 'MX')
)

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

EXPERIENCE_CHOICES = [(i, str(i)) for i in range(51)]

BUDGET_CHOICES = [(i, str(i)) for i in range(101)]

QUALIFICATION_CHOICES = (
    ('UG', 'UNDER GRADUATE'),
    ('GRADUATE', 'GRADUATE'),
    ('PG', 'POST GRADUATE'),
    ('PhD', 'PhD'),
)

GENDER_CHOICES = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
)


def change_file_path(instance, filename):
    ''' This function generates a random string of length 16 which will be a combination of (4 digits + 4
    characters(lowercase) + 4 digits + 4 characters(uppercase)) seperated 4 characters by hyphen(-) '''

    import random
    import string

    # random_str length will be 16 which will be combination of (4 digits + 4 characters + 4 digits + 4 characters)

    filetype = filename.split(".")[-1].lower()
    filename = filename + "." + filetype
    path = "MyANSRSource/uploads/" + str(datetime.datetime.now().year) + "/" + str(
        datetime.datetime.now().month) + "/" + str(datetime.datetime.now().day) + "/"
    os_path = os.path.join(path, filename)
    return os_path


def content_file_name(instance, filename):
    ''' This function generates a random string of length 16 which will be a combination of (4 digits + 4
    characters(lowercase) + 4 digits + 4 characters(uppercase)) seperated 4 characters by hyphen(-) '''

    import random
    import string

    # random_str length will be 16 which will be combination of (4 digits + 4 characters + 4 digits + 4 characters)

    filetype = filename.split(".")[-1].lower()
    filename = filename
    path = "uploads/" + str(instance.user)
    os_path = os.path.join(path, filename)
    return os_path


class Customer(models.Model):
    phone_number = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    con_password=models.CharField(max_length=20)

    def __str__(self):
        return self.id


class Client(AbstractUser):
    mobile_phone = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
    USERNAME_FIELD = 'mobile_phone'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=50)

    def __str__(self):
        return self.name


class Sub_category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class child_sub_category(models.Model):
    name = models.CharField(verbose_name="Name", max_length=30)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Design(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    design_type = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    design_name = models.CharField(verbose_name="Design project Name", max_length=30)
    design_images = models.FileField(upload_to='media/', blank=True, null=True, verbose_name="Design Images")
    design_number = models.CharField(verbose_name="Design Number", max_length=50)

    def __str__(self):
        return self.design_name


class Project(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    project_type = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    project_name = models.CharField(verbose_name="Project Name", max_length=30)
    project_images = models.FileField(upload_to='media/', blank=True, null=True, verbose_name="Project Images")
    project_number = models.CharField(verbose_name="project Number", max_length=50)

    def __str__(self):
        return self.project_name


class New_Portfolio(models.Model):
    user = models.OneToOneField(Client,on_delete=models.CASCADE)
    experience = models.CharField(verbose_name="Experience", max_length=10, choices=EXPERIENCE_CHOICES, blank=False,
                                  null=False)
    qualification = models.CharField(verbose_name="Qualification", max_length=20, choices=QUALIFICATION_CHOICES,
                                     blank=False, null=False)
    budget = models.CharField(verbose_name="Budget", max_length=20, choices=BUDGET_CHOICES)
    prefix = models.CharField(verbose_name="Prefix", max_length=3, choices=PREFIX_CHOICES)
    gender = models.CharField(verbose_name="Gender", max_length=10, choices=GENDER_CHOICES)
    mobile_phone = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
    secondary_phone = models.CharField(verbose_name="Secondary phone", max_length=10, unique=True, blank=False,
                                       null=True)
    tel_phone = models.CharField(verbose_name="Tele phone", max_length=10, unique=True, blank=False,
                                 null=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    about_me = models.CharField(verbose_name="About me ", blank=True, max_length=250)
    profile_pic = models.ImageField(upload_to='media/')
    location = models.CharField(verbose_name="location", max_length=30)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    child_sub_category=models.ForeignKey(child_sub_category,on_delete=models.CASCADE)


    # @receiver(post_save, sender=Client)
    # def create_client_profile(sender, instance, created, **kwargs):
    #     if created:
    #         New_Portfolio.objects.create(user=instance)
    #
    #
    # @receiver(post_save, sender=Client)
    # def save_client_profile(sender, instance, **kwargs):
    #     instance.New_Portfolio.save()


class WalkinCustomer(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Name", max_length=30)
    email = models.EmailField(verbose_name="email", max_length=70, blank=True)
    mobile_phone = models.CharField(verbose_name="Mobile phone", max_length=10, unique=True, blank=False, null=True)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)


class Appointment(models.Model):
    user = models.ForeignKey(Client, related_name="client_appointment", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="customer_appointment", on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Status', default=False)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)


class DeisgnUploads(models.Model):
    user = models.ForeignKey(Client, related_name="client_designs", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="customer_designs", on_delete=models.CASCADE)
    design_type = models.ForeignKey(child_sub_category, on_delete=models.CASCADE)
    design_name = models.CharField(verbose_name="Design project Name", max_length=30)
    design_images = models.FileField(upload_to='media/')
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)


class InvoicesProposalsUploads(models.Model):
    user = models.ForeignKey(Client, related_name="client_invoice_and_proposals", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="customer_invoice_and_proposals", on_delete=models.CASCADE)
    invoices = models.FileField(upload_to=change_file_path, validators=[validate_file_extension],
                                verbose_name="Invoices")
    proposals = models.FileField(upload_to=change_file_path, validators=[validate_file_extension],
                                 verbose_name="Proposals")
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)


class AppointmentScheduler(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    slots_booked = models.ForeignKey(Appointment, on_delete=models.CASCADE)


class FeedBack(models.Model):
    user = models.ForeignKey(Client, related_name="client_feedback", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="Customer_feedback", on_delete=models.CASCADE)
    feedback = models.CharField(verbose_name="Feedback", max_length=250)
    date_time = models.DateTimeField(verbose_name="Actual BRS Start Date", auto_now_add = True)

    def __str__(self):
        return self.feedback


class Rating(models.Model):
    user = models.ForeignKey(Client, related_name="client_rating", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name="Customer_rating", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=True, choices=RATING_CHOICES, blank=False, default=0)
    date_time = models.DateField(verbose_name="Actual BRS Start Date",auto_now_add =True)

    def __str__(self):
        return self.rating


class Parameters(models.Model):
    user = models.ForeignKey(Client, related_name="client", on_delete=models.CASCADE)
    clicks = models.CharField(verbose_name="clicks", max_length=10)
    date_time = models.DateField(verbose_name="Actual BRS Start Date", blank=True, null=True)


class Questions(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    question_title = models.TextField(max_length=200)
    question_description=models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_title


class Answers(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    answer = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer