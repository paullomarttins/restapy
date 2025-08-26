from django.urls import path
from .views import GrupoUserUpdate, grupo_update

urlpatterns = [
    path('api/grupo/', GrupoUserUpdate.as_view(), name='view-grupo'),
    # path('api/', lista_workspace, name='lista-workspace'),
    path('api/grupo-update/', grupo_update, name='user-grupo-update'),
]
