from django.shortcuts import render, redirect
from home.models import Produto

# Create your views here.

def calcular_desconto(produto):
    try:
        preco_normal = float(produto.precoNormal)
        preco_desconto = float(produto.precoDesconto)
        if preco_normal > 0 and preco_desconto < preco_normal:
            return round(((preco_normal - preco_desconto) / preco_normal) * 100)
        else:
            return 0
    except (ValueError, TypeError):
        return 0

def nomes_bonitos():
    return {
        "processador": "Processador",
        "placa-mae": "Placa-mãe",
        "memoria-ram": "Memória RAM",
        "placa-video": "Placa de Vídeo",
        "hd-ssd": "HD-SSD",
        "fonte": "Fonte",
        "gabinete": "Gabinete",
        "cooler": "Cooler",
        "monitor": "Monitor",
        "teclado": "Teclado",
        "mouse": "Mouse"
    }

def index(request):

    produtos_novos = Produto.objects.all().order_by('-id')[:10]
    produtos_random = Produto.objects.order_by('?')[:10]
    modelos_pc = Produto.objects.filter(tipoDeProduto="PC Gamer").order_by('-id')[:10]

    for produto in produtos_novos:
        produto.desconto = calcular_desconto(produto)
    for produto in produtos_random:
        produto.desconto = calcular_desconto(produto)
    for produto in modelos_pc:
        produto.desconto = calcular_desconto(produto)

    
    ORDEM_PERSONALIZADA = [
        "processador", "placa-mae", "memoria-ram", "placa-video",
        "hd-ssd", "gabinete", "fonte", "cooler", "monitor", "teclado", "mouse"
    ]

    NOMES_BONITOS = nomes_bonitos()

    categorias_distintas = Produto.objects.values_list('tipoDeProduto', flat=True).distinct()
    categorias_existentes = [cat for cat in categorias_distintas if cat]
    
    categorias_data = []
    for categoria in categorias_existentes:
        produto_com_imagem = Produto.objects.filter(
            tipoDeProduto=categoria
        ).exclude(
            imagem__isnull=True
        ).exclude(
            imagem=''
        ).first()
        if produto_com_imagem and produto_com_imagem.imagem:
            img_url = produto_com_imagem.imagem.url
        else:
            img_url = "https://placehold.co/800?text=" + categoria.replace(' ', '+')
        categorias_data.append({
            "slug": categoria,
            "nome": NOMES_BONITOS.get(categoria, categoria.title()),
            "img": img_url
        })
    
    # Ordena conforme sua preferência
    categorias_ordenadas = []
    for categoria_slug in ORDEM_PERSONALIZADA:
        for cat_data in categorias_data:
            if cat_data["slug"] == categoria_slug:
                categorias_ordenadas.append(cat_data)
                break
    for cat_data in categorias_data:
        if cat_data not in categorias_ordenadas:
            categorias_ordenadas.append(cat_data)
    
    context = {
        "produtos_novos": produtos_novos,
        "categorias": categorias_ordenadas,
        "produtos_random": produtos_random,
        "modelos_pc": modelos_pc
    }    
    return render(request, "home/index.html", context)


def detail(request, pk, tipoDeProduto):
    produto_especifico = Produto.objects.get(id=pk)
    produtos_relacionado = Produto.objects.filter(tipoDeProduto=tipoDeProduto).order_by('-id').exclude(id=produto_especifico.id)

    produto_especifico.desconto = calcular_desconto(produto_especifico)
    for produto in produtos_relacionado:
        produto.desconto = calcular_desconto(produto)

    NOMES_BONITOS = nomes_bonitos()
    nome_bonito = NOMES_BONITOS.get(tipoDeProduto, tipoDeProduto.title())

    context = {
        "produto_especifico": produto_especifico,
        "produtos_relacionado": produtos_relacionado,
        "nome_bonito": nome_bonito,
    }
    return render(request, "home/detail.html", context)


def category(request, tipoDeProduto):
    produtos = Produto.objects.filter(tipoDeProduto=tipoDeProduto).order_by('-id')

    NOMES_BONITOS = nomes_bonitos()

    for produto in produtos:
        produto.desconto = calcular_desconto(produto)

    nome_bonito = NOMES_BONITOS.get(tipoDeProduto, tipoDeProduto.title())

    context = {
        "tipo": tipoDeProduto,
        "produtos": produtos,
        "nome_bonito": nome_bonito,
    }
    return render(request, "home/category.html", context)