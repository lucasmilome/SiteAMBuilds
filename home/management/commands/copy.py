from django.core.management.base import BaseCommand
from home.models import Produto 

class Command(BaseCommand):
    help = 'Popula o banco com produtos fictícios'

    def handle(self, *args, **kwargs):
        produtos = Produto.objects.all()  # Altere o slice para quantos quiser copiar

        for produto in produtos:
            produto.pk = None  # Remove o ID para criar novo
            produto.nome = produto.nome
            produto.save()