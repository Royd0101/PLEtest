from django import forms
from .models import Receipt,Person_Receipt

class receipt_form(forms.ModelForm):
    fined = forms.DecimalField(
        label="Please enter amount",
        widget=forms.NumberInput(attrs={
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
        })
    )

    receipt = forms.FileInput()

    invoice_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'date', 'style': 'width: 100%; display: inline-block; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )

    class Meta:
        model = Receipt
        fields = ['fined', 'receipt', 'file', 'invoice_date']
        widgets = {
            'receipt': forms.ClearableFileInput(attrs={'multiple': True}),
            'file': forms.HiddenInput(),
        }
        labels = {
            'receipt': 'Penalty Receipt',
        }
    

class person_receipt_form(forms.ModelForm):
    fined = forms.DecimalField(
        label="Please enter amount",
        widget=forms.NumberInput(attrs={
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
        })
    )
    receipt = forms.FileInput()


    
    invoice_date = forms.DateField(
        required=True,
        widget=forms.TextInput(attrs={'type': 'date', 'style': 'width: 100%; display: inline-block; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'})
    )

    class Meta:
        model = Person_Receipt
        fields = ['fined', 'receipt', 'person_document', 'invoice_date']
        widgets = {
            'receipt': forms.ClearableFileInput(attrs={'multiple': True}),
            'person_document': forms.HiddenInput(),
        }
        labels = {
            'receipt': 'Penalty Receipt',
        }