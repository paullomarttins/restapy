from django import forms
from restapp.models import GrupoUpdate

class GrupoFormUpdate(forms.ModelForm):
    class Meta:
        model = GrupoUpdate
        fields = ['email','perfil','name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nome@exemplo.com'}),
            'perfil': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.Select(attrs={'class': 'form-select'})
        }
