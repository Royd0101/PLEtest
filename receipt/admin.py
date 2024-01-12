from django.contrib import admin

from .models import Receipt,Person_Receipt
# Register your models here.
@admin.register(Receipt)
class Receipt_Admin(admin.ModelAdmin):
    search_fields = ('id',)  # Note the comma after 'id'
    list_display = ('id', 'fined', 'receipt')

@admin.register(Person_Receipt)
class Person_Receipt(admin.ModelAdmin):
    search_fields = ('id',)  # Note the comma after 'id'
    list_display = ('id', 'fined', 'receipt','person_document')