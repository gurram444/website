from django.contrib import admin
from .models import Client,New_Portfolio
# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ['username','email','mobile_phone','password']
    class Meta:
        model = Client
admin.site.register(Client,ClientAdmin)
admin.site.register(New_Portfolio)