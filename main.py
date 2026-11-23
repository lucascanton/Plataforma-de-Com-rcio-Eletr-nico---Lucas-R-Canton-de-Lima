from collections import deque
import os

ARQUIVO = "dados_sistema.txt"

def ler(mensagem):
    return input(mensagem).strip() # LÊ A MENSAGEM SE ESPAÇO

def formatar_preco(valor): # transforma o número em dinheiro, ex: 50.5 vira R$ 50,50
    return "R$ " +f"{valor:.2f}".replace(".", ",")

#criação das estruturas vazias
arvore = {} # Usada para criar as categorias
catalogo = [] #Lista, ca produto vai ter codigo, nome, preço, estoque e categoria
pilha = [] #Para o carrinho de compras, quarda o códgigo do produto para ref
fila = deque() #Para o pagamento (pedido(id), cliente, valor, codigo dos produtos)
historico = [] #lista para ver o historico de pedidos aprovados

#---------------------------------------------------------------------------------------#

# funções arvore

def pedir_caminho(mensagem):
    texto = ler(mensagem)
    if texto.strip() == "":
        return []
    return [parte.strip() for parte in texto.split(">")]
    #Tira os espaços e quebra o texto no divisor ">" para gerar os caminhos

def navegar(caminho):
    no = arvore
    for nome in caminho:
        if nome not in no:
            return None
        no = no[nome]
    return no
    # não entendi

def inserir_no():
    caminhoPai = pedir_caminho("Pai (vazio para criar um categoria)") # vazio = raiz
    pai = navegar(caminhoPai)
    if pai is None: # verifica se existe pela navegação
        print("Esse pai não existe")
        return
    nome = ler("Nome no novo nó: ")
    pai[nome] = {} # adiciona o novo nó (sub-categoria)
    print ("No inserido")

def exibir_arvore(no, nivel):
    for nome in no:
        print("    " * nivel +  " - " + nome)
        exibir_arvore(no[nome], nivel + 1)
        #função recursiva -> lista os nós da arvore descendo os niveis até não ter filhos

def renomear_no():
    caminho = pedir_caminho("Caminho do nó a renomear: ") # antes tava sem a mensagem
    if len(caminho) == 0 or navegar(caminho) is None:
        print("Nó não encontrado.")
        return
    pai = navegar(caminho[:-1]) # pega o caminho pai (para acessar os nós que dele)
    novo = ler("Novo nome: ") # pega o nome do novo nó
    pai[novo] = pai.pop(caminho[-1]) #cria esse novo nó pegando o conteudo do antigo que foi apagado
    print("Nó renomeado.")

def remover_no():
    caminho = pedir_caminho("Caminho do nó a remover: ")
    if len(caminho) == 0 or navegar(caminho) is None:
        print("Nó não encontrado.")
        return
    pai = navegar(caminho[:-1])
    del pai[caminho[-1]]  # apaga o nó e tudo que está dentro dele
    print("Nó removido.")

def menu_departamentos():  # menu de navegação
    while True:
        print("\n--- DEPARTAMENTOS (Árvore) ---")
        print("1-Inserir  2-Exibir  3-Renomear  4-Remover  0-Voltar")
        op = ler("Opção: ")
        if op == "1":
            inserir_no()
        elif op == "2":
            if len(arvore) == 0:
                print("Árvore vazia.")
            exibir_arvore(arvore, 0)
        elif op == "3":
            renomear_no()
        elif op == "4":
            remover_no()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

#---------------------------------------------------------------------------#
#funções lista

def buscar_produto(codigo):
    # percorre a lista e devolve o produto com esse código (ou None). Usada por carrinho e pagamentos.
    for produto in catalogo:
        if produto[0] == codigo:
            return produto
    return None


def cadastrar_produto():
    codigo = ler("Código: ")
    if buscar_produto(codigo) is not None:
        print("Já existe produto com esse código.")
        return
    # o produto só pode ser cadastrado em uma categoria que existe na ÁRVORE
    categoria = pedir_caminho("Categoria (ex: Eletronicos > Celulares): ")
    if len(categoria) == 0 or navegar(categoria) is None:
        print("Categoria não existe. Cadastre antes no menu Departamentos.")
        return
    nome = ler("Nome: ")
    preco = float(ler("Preço: ").replace(",", "."))
    estoque = int(ler("Estoque: "))
    catalogo.append([codigo, nome, preco, estoque, " > ".join(categoria)])  # insere no fim da lista
    print("Produto cadastrado.")


def mostrar_produto(p):
    print(p[0], "-", p[1], "-", formatar_preco(p[2]), "- estoque:", p[3], "-", p[4])


def listar_produtos():
    if len(catalogo) == 0:
        print("Catálogo vazio.")
    for p in catalogo:
        mostrar_produto(p)


def atualizar_produto():
    produto = buscar_produto(ler("Código do produto a atualizar: "))
    if produto is None:
        print("Produto não encontrado.")
        return
    produto[1] = ler("Novo nome: ")
    produto[2] = float(ler("Novo preço: ").replace(",", "."))
    produto[3] = int(ler("Novo estoque: "))
    print("Produto atualizado.")


def remover_produto():
    codigo = ler("Código do produto a remover: ")
    produto = buscar_produto(codigo)
    if produto is None:
        print("Produto não encontrado.")
        return
    if codigo in pilha:
        print("Produto está no carrinho. Desfaça a ação antes de remover.")
        return
    catalogo.remove(produto)
    print("Produto removido.")


def menu_catalogo(): # menu lista
    while True:
        print("\n--- CATÁLOGO (Lista) ---")
        print("1-Cadastrar  2-Listar  3-Atualizar  4-Remover  0-Voltar")
        op = ler("Opção: ")
        if op == "1":
            cadastrar_produto()
        elif op == "2":
            listar_produtos()
        elif op == "3":
            atualizar_produto()
        elif op == "4":
            remover_produto()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

# ----------------------------------------------------------------
# função pilhas
def adicionar_ao_carrinho():
    listar_produtos()
    codigo = ler("Código do produto a adicionar: ")
    produto = buscar_produto(codigo)  # consulta o CATÁLOGO
    if produto is None:
        print("Produto não encontrado.")
        return
    if pilha.count(codigo) >= produto[3]:  # quantas vezes já está no carrinho x estoque
        print("Estoque insuficiente.")
        return
    pilha.append(codigo)  # entra no TOPO (fim da lista)
    print(produto[1], "adicionado ao carrinho.")


def calcular_total():
    total = 0
    for codigo in pilha:
        produto = buscar_produto(codigo)
        if produto is not None:
            total = total + produto[2]
    return round(total, 2)


def listar_carrinho():
    if len(pilha) == 0:
        print("Carrinho vazio.")
    for codigo in reversed(pilha):  # mostra do topo para a base
        produto = buscar_produto(codigo)
        if produto is not None:
            print(produto[1], "-", formatar_preco(produto[2]))
    print("Total:", formatar_preco(calcular_total()))


def trocar_topo():
    if len(pilha) == 0:
        print("Carrinho vazio.")
        return
    novo = ler("Código do novo produto para o topo: ")
    produto = buscar_produto(novo)
    if produto is None:
        print("Produto não encontrado.")
        return
    pilha[-1] = novo  # [-1] é o topo
    print("Topo trocado por", produto[1])


def desfazer_acao():
    if len(pilha) == 0:
        print("Carrinho vazio.")
        return
    codigo = pilha.pop()  # sai do TOPO (último que entrou)
    print("Desfeito:", buscar_produto(codigo)[1], "saiu do carrinho.")


def finalizar_compra():
    # transforma o carrinho (PILHA) em um pagamento na FILA
    if len(pilha) == 0:
        print("Carrinho vazio.")
        return
    pedido = ler("Número do pedido: ")
    cliente = ler("Nome do cliente: ")
    valor = calcular_total()
    itens = list(pilha)  # cópia dos códigos (para não perder ao limpar o carrinho)
    fila.append([pedido, cliente, valor, itens])  # entra no FIM da fila
    pilha.clear()  # carrinho esvaziado
    print("Compra finalizada. Pagamento do pedido", pedido, "aguardando aprovação.")


def menu_carrinho():
    while True:
        print("\n--- CARRINHO (Pilha) ---")
        print("1-Adicionar produto  2-Ver carrinho  3-Trocar o topo  4-Desfazer última ação  5-Finalizar compra  0-Voltar")
        op = ler("Opção: ")
        if op == "1":
            adicionar_ao_carrinho()
        elif op == "2":
            listar_carrinho()
        elif op == "3":
            trocar_topo()
        elif op == "4":
            desfazer_acao()
        elif op == "5":
            finalizar_compra()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

# ----------------------------------------------------------------
# funções filas
def listar_fila():
    if len(fila) == 0:
        print("Fila vazia.")
    posicao = 1
    for p in fila:
        print(str(posicao) + "º - Pedido", p[0], "-", p[1], "-", formatar_preco(p[2]), "-", len(p[3]), "item(ns)")
        posicao = posicao + 1


def listar_historico():
    if len(historico) == 0:
        print("Nenhum pedido aprovado ainda.")
    for p in historico:
        print("Pedido", p[0], "-", p[1], "-", formatar_preco(p[2]), "-", len(p[3]), "item(ns)")


def corrigir_cliente_do_primeiro():
    if len(fila) == 0:
        print("Fila vazia.")
        return
    fila[0][1] = ler("Novo nome do cliente do primeiro pagamento: ")  # só mexe no da frente
    print("Pagamento atualizado.")


def aprovar_pagamento():
    if len(fila) == 0:
        print("Fila vazia.")
        return
    p = fila.popleft()  # sai do INÍCIO da fila (primeiro que entrou)
    historico.append(p)  # guarda o pedido aprovado no histórico
    for codigo in p[3]:  # baixa o estoque no CATÁLOGO
        produto = buscar_produto(codigo)
        if produto is not None and produto[3] > 0:
            produto[3] = produto[3] - 1
    print("Pedido", p[0], "aprovado. Estoque atualizado.")


def menu_pagamentos():
    while True:
        print("\n--- PAGAMENTOS (Fila) ---")
        print("1-Listar fila  2-Corrigir cliente do primeiro  3-Aprovar o primeiro  4-Ver pedidos aprovados  0-Voltar")
        print("(os pagamentos entram na fila ao finalizar a compra no Carrinho)")
        op = ler("Opção: ")
        if op == "1":
            listar_fila()
        elif op == "2":
            corrigir_cliente_do_primeiro()
        elif op == "3":
            aprovar_pagamento()
        elif op == "4":
            listar_historico()
        elif op == "0":
            break
        else:
            print("Opção inválida.")

# ------------------------------------------------------------------
#peristencia
def listar_caminhos(no, prefixo):
    # devolve o caminho da raiz até cada folha, ex: [["Eletronicos", "Celulares"]]
    caminhos = []
    for nome in no:
        novo = prefixo + [nome]
        if len(no[nome]) == 0:  # sem filhos = folha
            caminhos.append(novo)
        else:
            caminhos = caminhos + listar_caminhos(no[nome], novo)
    return caminhos


def texto_pedido(p):
    # monta o trecho rotulado de um pedido (usado para FILA e HISTORICO)
    return ("pedido=" + p[0] + "|cliente=" + p[1] + "|valor=" + str(p[2]) +
            "|itens=" + ",".join(p[3]))


def pegar(campo):
    # "preco=50.0" -> "50.0" (pega o que vem depois do primeiro =)
    return campo.split("=", 1)[1]


def ler_pedido(campos):
    # reconstrói um pedido a partir dos campos da linha
    return [pegar(campos[1]), pegar(campos[2]), float(pegar(campos[3])), pegar(campos[4]).split(",")]


def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as arq:
        for caminho in listar_caminhos(arvore, []):
            arq.write("ARVORE|" + "|".join(caminho) + "\n")
        for p in catalogo:
            arq.write("LISTA|codigo=" + p[0] + "|nome=" + p[1] + "|preco=" + str(p[2]) +
                      "|estoque=" + str(p[3]) + "|categoria=" + p[4] + "\n")
        for codigo in pilha:  # da base para o topo
            arq.write("PILHA|codigo=" + codigo + "\n")
        for p in fila:  # do início para o fim
            arq.write("FILA|" + texto_pedido(p) + "\n")
        for p in historico:
            arq.write("HISTORICO|" + texto_pedido(p) + "\n")
    print("Dados salvos.")


def carregar_dados():
    if not os.path.exists(ARQUIVO):
        print("Arquivo não encontrado. Salve os dados primeiro.")
        return
    # esvazia a memória antes de reconstruir
    arvore.clear()
    catalogo.clear()
    pilha.clear()
    fila.clear()
    historico.clear()
    with open(ARQUIVO, "r", encoding="utf-8") as arq:
        for linha in arq:
            campos = linha.strip().split("|")  # separa a linha em pedaços
            tipo = campos[0]  # primeiro pedaço = identificador da estrutura
            if tipo == "ARVORE":
                no = arvore
                for nome in campos[1:]:  # cada pedaço é um nível da árvore
                    if nome not in no:
                        no[nome] = {}
                    no = no[nome]
            elif tipo == "LISTA":
                catalogo.append([pegar(campos[1]), pegar(campos[2]), float(pegar(campos[3])),
                                 int(pegar(campos[4])), pegar(campos[5])])
            elif tipo == "PILHA":
                pilha.append(pegar(campos[1]))
            elif tipo == "FILA":
                fila.append(ler_pedido(campos))
            elif tipo == "HISTORICO":
                historico.append(ler_pedido(campos))
    print("Dados carregados.")

# ---------------- MENU PRINCIPAL ----------------
def menu_principal():
    while True:
        print("\n===== E-COMMERCE =====")
        print("1-Categorias (Árvore)")
        print("2-Catálogo (Lista)")
        print("3-Carrinho (Pilha)")
        print("4-Pagamentos (Fila)")
        print("5-Salvar dados")
        print("6-Carregar dados")
        print("0-Sair")
        op = ler("Opção: ")
        if op == "1":
            menu_departamentos()
        elif op == "2":
            menu_catalogo()
        elif op == "3":
            menu_carrinho()
        elif op == "4":
            menu_pagamentos()
        elif op == "5":
            salvar_dados()
        elif op == "6":
            carregar_dados()
        elif op == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")


menu_principal()




