from django.contrib import admin
from .models import User, Company
# Register your models here.
@admin.register(User)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('id', 'first_name',)
    list_display = ('id', 'first_name','last_name','email','company')


@admin.register(Company)
class Company_Admin(admin.ModelAdmin):
    search_fields = ('id', 'company_name',)
    list_display = ('id','company_name')