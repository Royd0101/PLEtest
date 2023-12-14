from django import forms
from django.db import transaction
from .models import Company ,User

#create user form
class create_user_form(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'width: 100%; padding: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'width: 100%; padding: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'style': 'width: 100%; padding: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
    }))
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        empty_label="Select a Company",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'style': 'width: 100%; padding: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
    }))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'style': 'width: 100%; padding: 4px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
    }))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be 8 characters or longer.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please try again.")

        return cleaned_data


class update_user_form(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;',
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;',
        })
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;',
        })
    )
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        empty_label="Select a Company",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;',
        })
    )
    password = forms.CharField(
        required=False,
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;',
        })
    )

    @transaction.atomic
    def save(self, user, commit=True):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        company = self.cleaned_data['company']
        company_name = Company.objects.get(company_name=company)
        user.company = company_name

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user

class update_company_form(forms.ModelForm):
    
    company_name = forms.CharField(
        widget=forms.TextInput(
      attrs={
        'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
    }))
    
    class Meta:
        model = Company
        fields = ['company_name']


class company_form(forms.ModelForm):
    
    company_name = forms.CharField(
        widget=forms.TextInput(
      attrs={
        'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
    }))
    
    class Meta:
        model = Company
        fields = ['company_name']
