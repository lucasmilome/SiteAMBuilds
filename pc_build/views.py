from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from home.models import Produto
from .models import MontagemPC

# Create your views here.
def pc_build(request):
    return render(request, "pc_build/index.html")

def pecas(request):
    produtos = Produto.objects.all()
    for produto in produtos:
        produto.desconto = calcular_desconto(produto)

    modelo = request.GET.get('modelo', 'customizado')
    context = {
        'processadores': Produto.objects.filter(tipoDeProduto="processador"),
        'placas_mae': Produto.objects.filter(tipoDeProduto="placa-mae"),
        'memoria_ram': Produto.objects.filter(tipoDeProduto="memoria-ram"),
        'armazenamento': Produto.objects.filter(tipoDeProduto="hd-ssd"),
        'placas_de_video': Produto.objects.filter(tipoDeProduto="placa-video"),
        'fontes_de_alimentacao': Produto.objects.filter(tipoDeProduto="fonte"),
        'gabinetes': Produto.objects.filter(tipoDeProduto="gabinete"),
        'coolers': Produto.objects.filter(tipoDeProduto="cooler"),
        'monitores': Produto.objects.filter(tipoDeProduto="monitor"),
        'teclados': Produto.objects.filter(tipoDeProduto="teclado"),
        'mouses': Produto.objects.filter(tipoDeProduto="mouse"),
        'modelo': modelo,
    }

    return render(request, 'pc_build/pecas.html', context)

@login_required
def salvar_montagem(request):
    if request.method == 'POST':
        usuario = request.user
        modelo = request.POST.get('modelo', 'customizado')
        total_str = request.POST.get('total', '0')
        try:
            total = float(total_str.replace(',', '.')) if total_str else 0
        except ValueError:
            total = 0

        def get_produto(produto_id):
            try:
                return Produto.objects.get(id=int(produto_id))
            except (TypeError, ValueError, Produto.DoesNotExist):
                return None

        # IDs das peças vindos do form
        processador = get_produto(request.POST.get('processador'))
        placa_mae = get_produto(request.POST.get('placa_mae'))
        memoria_ram = get_produto(request.POST.get('memoria_ram'))
        placa_video = get_produto(request.POST.get('placa_video'))
        hd_ssd = get_produto(request.POST.get('hd_ssd'))
        fonte = get_produto(request.POST.get('fonte'))
        gabinete = get_produto(request.POST.get('gabinete'))
        cooler = get_produto(request.POST.get('cooler'))
        monitor = get_produto(request.POST.get('monitor'))
        teclado = get_produto(request.POST.get('teclado'))
        mouse = get_produto(request.POST.get('mouse'))

        montagem = MontagemPC.objects.create(
            usuario=request.user,
            processador=processador,
            placa_mae=placa_mae,
            memoria_ram=memoria_ram,
            placa_video=placa_video,
            hd_ssd=hd_ssd,
            fonte=fonte,
            gabinete=gabinete,
            cooler=cooler,
            monitor=monitor,
            teclado=teclado,
            mouse=mouse,
        )

        # Redirecione para a página de sucesso ou lista de montagens
        return redirect('meus_pcs')  # ou 'meus_pcs'

    # Se não for POST, redirecione ou mostre erro
    return redirect('index')

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

def meus_pcs(request):
    montagens = MontagemPC.objects.filter(usuario=request.user).order_by('-data_criacao')
    return render(request, 'pc_build/meus_pcs.html', {'montagens': montagens})

@login_required
def montagem_detalhes(request, montagem_id):
    montagem = get_object_or_404(MontagemPC, id=montagem_id)
    pecas = []
    campos = [
        ("processador", "Processador"),
        ("placa_mae", "Placa-mãe"),
        ("memoria_ram", "Memória RAM"),
        ("placa_video", "Placa de Vídeo"),
        ("hd_ssd", "HD/SSD"),
        ("fonte", "Fonte"),
        ("gabinete", "Gabinete"),
        ("cooler", "Cooler"),
        ("monitor", "Monitor"),
        ("teclado", "Teclado"),
        ("mouse", "Mouse"),
    ]
    total = 0
    for campo, label in campos:
        produto = getattr(montagem, campo, None)
        if produto:
            quantidade = 1
            if campo == "memoria_ram" and hasattr(montagem, "quantidade_memoria_ram"):
                quantidade = montagem.quantidade_memoria_ram
            preco = produto.precoDesconto * quantidade
            total += preco
            pecas.append({
                "nome": produto.nome,
                "imagem": produto.imagem.url if produto.imagem else "",
                "preco": preco,
                "quantidade": quantidade,
                "url": getattr(produto, "url", "#"),
                "label": label,
            })
    return render(request, "pc_build/montagem_detalhes.html", {
        "montagem": montagem,
        "pecas": pecas,
        "total": total,
    })