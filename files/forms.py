from django import forms
from files.models import Department
from users.models import Company
class create_file(forms.Form):
    department_name = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'}))
    document_type = forms.ChoiceField(
        choices=[
            ('contract', 'Contract'),
            ('invoice', 'Invoice'),
            ('report', 'Report'),
        ],
        initial='Select Document Type',
        required=True,
        widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )
    upload_file = forms.FileField()
    
    renewal_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'date', 'style': 'width: 100%; display: block; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )

    expiry_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'date', 'style': 'width: 100%; display: block; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )
    
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.HiddenInput())

    def __init__(self, company, *args, **kwargs):
        super(create_file, self).__init__(*args, **kwargs)
        self.fields['company'].initial = company
        self.fields['department_name'].choices = self.get_department_choices(company)

    def get_department_choices(self, company):
        if company:
            departments = Department.objects.filter(company=company)
            return [(department.department_name, department.department_name) for department in departments]
        return []


class renew_form(forms.Form):
    document_type = forms.ChoiceField(
        choices=[
            ('Select Document Type', '- Select Document Type -'),
            ('contract', 'Contract'),
            ('invoice', 'Invoice'),
            ('report', 'Report'),
        ],
        initial='Select Document Type',
        required=True,
        widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )
    upload_file = forms.FileField()
    renewal_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'date', 'style': 'width: 100%; display: inline-block; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )
    expiry_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'date', 'style': 'width: 100%; display: inline-block; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )

    def __init__(self, company, *args, **kwargs):
        super(renew_form, self).__init__(*args, **kwargs)
        self.fields['company'] = forms.CharField(widget=forms.HiddenInput(), initial=company)
        self.fields['department_name'] = forms.ChoiceField(choices=self.get_department_choices(company), required=True, widget=forms.Select(attrs={'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'}))

    def get_department_choices(self, company):
        if company:
            departments = Department.objects.filter(company=company)
            return [(department.department_name, department.department_name) for department in departments]
        return []


