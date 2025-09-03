from django.core.management.base import BaseCommand
from home.models import Produto
import random

class Command(BaseCommand):
    help = 'Popula o banco com produtos fictícios'

    def handle(self, *args, **kwargs):
        lojas = ["Kabum", "Terabyte", "Pichau", "Amazon", "Magazine Luiza"]
        tipos = [
            ("processador", "Processador"),
            ("placa-mae", "Placa-mãe"),
            ("memoria-ram", "Memória RAM"),
            ("placa-video", "Placa de Vídeo"),
            ("hd-ssd", "HD/SSD"),
            ("fonte", "Fonte"),
            ("gabinete", "Gabinete"),
            ("cooler", "Cooler"),
            ("monitor", "Monitor"),
            ("teclado", "Teclado"),
            ("mouse", "Mouse"),
        ]
        imagens = {
            "processador": "imagens_produto/processador.png",
            "placa-mae": "imagens_produto/placa-mae.png",
            "memoria-ram": "imagens_produto/memoria-ram.png",
            "placa-video": "imagens_produto/placa-video.png",
            "hd-ssd": "imagens_produto/hd-ssd.png",
            "fonte": "imagens_produto/fonte.png",
            "gabinete": "imagens_produto/gabinete.png",
            "cooler": "imagens_produto/cooler.png",
            "monitor": "imagens_produto/monitor.png",
            "teclado": "imagens_produto/teclado.png",
            "mouse": "imagens_produto/mouse.png",
        }
        nomes_extras = {
            "processador": ["Ryzen 5 5600X", "Intel i5-10400F", "Ryzen 7 5700G", "Intel i7-10700K"],
            "placa-mae": ["ASUS B450M", "Gigabyte H410M", "MSI B550M", "ASRock B460M"],
            "memoria-ram": ["Kingston Fury 8GB", "Corsair Vengeance 16GB", "Crucial Ballistix 8GB", "ADATA XPG 16GB"],
            "placa-video": ["GTX 1650", "RTX 3060", "RX 6600", "GTX 1660 Super"],
            "hd-ssd": ["Kingston SSD 240GB", "Seagate HD 1TB", "WD Blue SSD 480GB", "Crucial SSD 500GB"],
            "fonte": ["Corsair 500W", "PCYES 600W", "EVGA 500W", "Cooler Master 550W"],
            "gabinete": ["Bluecase BG-024", "Redragon Grapple", "PCYES Rhino", "Cooler Master Q300L"],
            "cooler": ["Cooler Master Hyper T20", "Rise Mode Mirage", "DeepCool Gammaxx", "Noctua NH-U12S"],
            "monitor": ["AOC 21.5''", "Samsung 24'' Curvo", "LG UltraGear 27''", "Dell 23.8''"],
            "teclado": ["Redragon Kumara", "Logitech K120", "Corsair K55", "HyperX Alloy"],
            "mouse": ["Logitech G203", "Redragon Cobra", "Razer DeathAdder", "Corsair Harpoon"],
        }
        for i in range(50):
            tipo, tipo_nome = random.choice(tipos)
            nome_produto = f"{random.choice(nomes_extras[tipo])} {random.randint(1000,9999)}"
            loja = random.choice(lojas)
            preco_normal = round(random.uniform(100, 2000), 2)
            desconto = random.choice([0.05, 0.10, 0.13, 0.15, 0.17, 0.20])
            preco_desconto = round(preco_normal * (1 - desconto), 2)
            descricao = f"{tipo_nome} de alta qualidade para seu PC gamer. Aproveite!"
            imagem = imagens[tipo]
            link = f"https://www.{loja.lower().replace(' ', '')}.com.br/produto/{nome_produto.replace(' ', '-').lower()}"
            cupom = random.choice(["", "DESCONTO10", "FRETEGRATIS", "PCGAMER"])
            Produto.objects.create(
                loja=loja,
                nome=nome_produto,
                descricao=descricao,
                precoNormal=preco_normal,
                precoDesconto=preco_desconto,
                tipoDeProduto=tipo,
                cupom=cupom,
                imagem=imagem,
                link=link
            )
        self.stdout.write(self.style.SUCCESS('50 produtos criados com sucesso!'))