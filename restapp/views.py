from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib import messages

import requests
from contrib.config import adiciona_user_workspace
from .forms import GrupoFormUpdate

# Token de acesso API
# access_token = obter_token()

class GrupoUserUpdate(TemplateView):
    template_name = 'grupos_user.html'
    form_class = GrupoFormUpdate

def grupo_update(request):
    form = GrupoFormUpdate(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            perfil = form.cleaned_data['perfil']
            workspace = form.cleaned_data['workspace']

            status_code, response = adiciona_user_workspace(email, perfil, workspace)
            form = GrupoFormUpdate()

            if status_code == 200 or status_code == 201:
                messages.success(request, 'Grupo atualizado com sucesso!')
                return render(request, 'grupos_user.html', {'response': response, 'form': form})
            else:
                messages.error(request, 'Erro ao atualizar grupo!')
                return render(request, 'grupos_user.html', {'response': response, 'form': form})
    else:
        form = GrupoFormUpdate()

    return render(request, 'grupos_user.html', {'form': form})
