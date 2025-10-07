from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.contrib import messages

from contrib.config import adiciona_user_workspace, lista_workspace, lista_user_workspace
from .forms import GrupoFormUpdate
from .models import ListaWorkspaces, ListaUserWorkspace

class GrupoUserUpdate(TemplateView):
    template_name = 'grupos_user.html'
    form_class = GrupoFormUpdate

def grupo_update(request):
    # lista_workspace() # incluir no crontab
    # instance = GrupoUpdate.objects.all()

    if request.method == 'POST':
        form = GrupoFormUpdate(request.POST)
        if form.is_valid():
            grupo_instance = form.save()

            email = form.cleaned_data['email']
            perfil = form.cleaned_data['perfil']
            workspaces = form.cleaned_data['name']

            grupo_instance.name.set(workspaces)

            for workspace in workspaces:
                status_code, response = adiciona_user_workspace(email, perfil, workspace.id_ws)

            if status_code in {200, 201}:
                messages.success(request, 'Grupo atualizado com sucesso!')
            else:
                messages.error(request, 'Erro ao atualizar grupo!')

            form = GrupoFormUpdate()
            return render(request, 'grupos_user.html', {'response': response, 'form': form})
    else:
        form = GrupoFormUpdate()

    return render(request, 'grupos_user.html', {'form': form})

class ListaWorkspace(ListView):
    model = ListaWorkspaces
    paginate_by = 15
    template_name = 'workspaces_list.html'

class ListaUserWorkspaceView(ListView):
    # lista_user_workspace()
    model = ListaUserWorkspace
    paginate_by = 15
    template_name = 'usuarios_list.html'
