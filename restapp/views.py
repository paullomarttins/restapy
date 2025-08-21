from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from decouple import config
import requests
import json
from contrib.config import obter_token
from .forms import GrupoFormUpdate
from this import s

# Token de acesso API
access_token = config('SECRET_KEY') # obter_token()

class GrupoUserUpdate(TemplateView):
    template_name = 'grupos_user.html'
    form_class = GrupoFormUpdate

def lista_workspace(request):
    url = 'https://api.powerbi.com/v1.0/myorg/groups'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    relatorios = response.json().get('value', [])

    context = {
        'relatorios': relatorios
    }

    return render(request, 'grupos_user.html', context)

def grupo_update(request):
    form = GrupoFormUpdate(request.POST)
    if request.method == 'POST':
        # form = GrupoFormUpdate()
        if form.is_valid():
            email = form.cleaned_data['email']
            perfil = form.cleaned_data['perfil']
            workspace = form.cleaned_data['workspace']

            status, response = adiciona_user_workspace(email, perfil, workspace)
            form = GrupoFormUpdate()
            if status == 200 or status == 201:
                messages.success(request, 'Grupo atualizado com sucesso!')
                return render(request, 'grupos_user.html', {'response': response, 'form': form})
            else:
                messages.error(request, 'Erro ao atualizar grupo!')
                return render(request, 'grupos_user.html', {'response': response, 'form': form})
    else:
        form = GrupoFormUpdate()

    return render(request, 'grupos_user.html', {'form': form})

def adiciona_user_workspace(email, perfil, workspace):
    url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace}/users'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'identifier': email,
        'groupUserAccessRight': perfil,
        'principalType': 'User'
    }

    try:
        response = requests.put(url, json=params, headers=headers)
        response.raise_for_status()
        return response.status_code, response
    except requests.exceptions.RequestException as e:
        return f'Erro de requisição: {e}'
