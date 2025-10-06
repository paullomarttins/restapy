from django.db import models

PERFIL = [
    ('Viewer', 'Viewer'),
    ('Member', 'Member'),
    ('Contributor', 'Contributor'),
    ('Admin', 'Admin')
]

class ListaWorkspaces(models.Model):
    id_ws = models.CharField(primary_key=True, max_length=50, editable=False)
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class GrupoUpdate(models.Model):
    email = models.EmailField()
    perfil = models.CharField(choices=PERFIL, default='Viewer')
    name = models.ManyToManyField(ListaWorkspaces)
    dt_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
