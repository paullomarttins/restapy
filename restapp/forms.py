from django import forms
from contrib.config import lista_workspace

WORKSPACES = lista_workspace()

class GrupoFormUpdate(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'label': 'E-mail', 'placeholder': 'nome@exemplo.com'}))
    perfil = forms.ChoiceField(
        choices = [
            ('Viewer', 'Viewer'),
            ('Member', 'Member'),
            ('Contributor', 'Contributor'),
            ('Admin', 'Admin')
        ],
        widget=forms.Select(attrs={'class': 'form-select', 'label': 'Perfil'})
    )
    # workspace = forms.CharField(widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    workspace = forms.MultipleChoiceField(
        choices = WORKSPACES,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
