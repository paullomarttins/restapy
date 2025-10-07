from django.urls import path
from .views import GrupoUserUpdate, grupo_update, ListaWorkspace, ListaUserWorkspaceView

urlpatterns = [
    path('api/grupo/', GrupoUserUpdate.as_view(), name='view-grupo'),
    path('api/workspaces/', ListaWorkspace.as_view(), name='lista-workspace'),
    path('api/grupo-update/', grupo_update, name='user-grupo-update'),
    path('api/lista-user/', ListaUserWorkspaceView.as_view(), name='lista-user')
]
