from django.db import models
from django.contrib.auth.models import User
from home.models import Produto

class MontagemPC(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    modelo = models.CharField(max_length=50, default='customizado')
    processador = models.ForeignKey(Produto, related_name='montagens_processador', on_delete=models.SET_NULL, null=True, blank=True)
    placa_mae = models.ForeignKey(Produto, related_name='montagens_placa_mae', on_delete=models.SET_NULL, null=True, blank=True)
    memoria_ram = models.ForeignKey(Produto, related_name='montagens_memoria_ram', on_delete=models.SET_NULL, null=True, blank=True)
    placa_video = models.ForeignKey(Produto, related_name='montagens_placa_video', on_delete=models.SET_NULL, null=True, blank=True)
    hd_ssd = models.ForeignKey(Produto, related_name='montagens_hd_ssd', on_delete=models.SET_NULL, null=True, blank=True)
    fonte = models.ForeignKey(Produto, related_name='montagens_fonte', on_delete=models.SET_NULL, null=True, blank=True)
    gabinete = models.ForeignKey(Produto, related_name='montagens_gabinete', on_delete=models.SET_NULL, null=True, blank=True)
    cooler = models.ForeignKey(Produto, related_name='montagens_cooler', on_delete=models.SET_NULL, null=True, blank=True)
    monitor = models.ForeignKey(Produto, related_name='montagens_monitor', on_delete=models.SET_NULL, null=True, blank=True)
    teclado = models.ForeignKey(Produto, related_name='montagens_teclado', on_delete=models.SET_NULL, null=True, blank=True)
    mouse = models.ForeignKey(Produto, related_name='montagens_mouse', on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nome = models.CharField(max_length=100, blank=True, null=True)    

    def __str__(self):
        return f"Montagem de {self.usuario.username} em {self.data_criacao:%d/%m/%Y}"

