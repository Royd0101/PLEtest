from django import forms
from .models import Receipt

class receipt_form(forms.ModelForm):
    fined = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'style': 'width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;'
        })
    )

    class Meta:
        model = Receipt
        fields = ['fined', 'receipt','file']
        widgets = {
            'receipt': forms.ClearableFileInput(attrs={'multiple': True}),
            'file': forms.HiddenInput(), 
        }