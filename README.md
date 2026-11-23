# Plataforma de Comércio Eletrônico (Tema 2)

Projeto final da disciplina **Teoria das Estruturas de Dados**.
Aluno: Lucas Roberto Canton de Lima (RA 252-000863)

Sistema em Python, executado no terminal, que aplica **Árvore, Lista, Pilha e Fila** de forma integrada no núcleo de uma loja virtual, com persistência em arquivo texto.

## Como executar

Requisito: Python 3 (somente bibliotecas nativas).

```bash
python main.py
```

(em alguns sistemas, `python3 main.py`)

O sistema inicia **vazio**. A opção **5 - Salvar dados** grava o estado em `dados_sistema.txt` e a opção **6 - Carregar dados** reconstrói as estruturas a partir dele. Não digite o caractere `|` nos textos, pois ele é o separador do arquivo.

## Como as estruturas se conversam

```
Árvore (departamentos) -> define a categoria de cada produto
Lista (catálogo)       -> produtos disponíveis para compra
Pilha (carrinho)       -> produtos que o cliente adiciona; a última ação pode ser desfeita
Fila (pagamentos)      -> compras finalizadas, aprovadas na ordem de chegada; a aprovação baixa o estoque
Lista (histórico)      -> pedidos já aprovados, que saem da fila mas continuam registrados
```

Fluxo de uso:
1. **Departamentos**: criar a hierarquia (ex.: `Eletronicos > Celulares`).
2. **Catálogo**: cadastrar produtos em uma categoria que exista na árvore.
3. **Carrinho**: adicionar produtos do catálogo (respeitando o estoque), desfazer a última ação e **finalizar a compra**, que transforma o carrinho em um pagamento na fila.
4. **Pagamentos**: aprovar o primeiro da fila, o que baixa o estoque dos produtos no catálogo e move o pedido para o histórico de pedidos aprovados.

## Menu

| Opção | Módulo | Estrutura | Operações |
|---|---|---|---|
| 1 | Departamentos | Árvore | inserir, exibir, renomear, remover |
| 2 | Catálogo | Lista | cadastrar, listar, atualizar, remover |
| 3 | Carrinho | Pilha | adicionar produto, ver carrinho, trocar o topo, desfazer última ação, finalizar compra |
| 4 | Pagamentos | Fila (+ Lista de histórico) | listar fila, corrigir cliente do primeiro, aprovar o primeiro, ver pedidos aprovados |
| 5 | Salvar dados | - | grava tudo em `dados_sistema.txt` |
| 6 | Carregar dados | - | reconstrói as estruturas a partir do arquivo |

## Justificativa técnica das estruturas

**Árvore (dicionários aninhados) - departamentos e categorias.** Departamentos, categorias e subcategorias formam uma hierarquia (pai > filhos). Como o Python não possui árvore nativa, cada nó é uma chave de um dicionário cujo valor é outro dicionário com seus filhos, por exemplo `{"Eletronicos": {"Celulares": {}}}`. Cada produto do catálogo só pode ser cadastrado em uma categoria que exista na árvore.

**Lista (`list`) - catálogo de produtos.** O catálogo é um conjunto de produtos ativos que cresce, diminui e é consultado a qualquer momento. A lista permite inserir no fim e buscar, alterar ou remover qualquer produto, sem restrição de ordem de acesso.

**Pilha (`list`) - carrinho de compras.** Para desfazer modificações no carrinho, a primeira ação a ser desfeita é sempre a mais recente (LIFO). Com `append` (empilhar) e `pop` (desempilhar), o fim da lista funciona como o topo. Cada elemento da pilha é o código de um produto do catálogo. Seguindo a regra da pilha, só o topo pode ser trocado ou removido.

**Fila (`collections.deque`) - aprovação de pagamentos.** Os pagamentos devem ser aprovados na ordem em que chegam (FIFO), para que nenhum cliente seja ultrapassado. O `deque` insere no fim com `append` e remove do início com `popleft` de forma eficiente. Seguindo a regra da fila, só o pagamento da frente pode ser alterado ou aprovado. Como a fila só guarda pedidos pendentes, os pedidos aprovados são movidos para uma lista de histórico (`list`), para que continuem registrados e sejam salvos no arquivo.

## Formato do arquivo `dados_sistema.txt`

Cada linha começa com o identificador da estrutura, seguido dos campos separados por `|`. Cada campo vem com o seu nome (`nome=valor`), para o arquivo ser legível:

```
ARVORE|Departamento|Categoria|Subcategoria
LISTA|codigo=P1|nome=Camisa|preco=50.0|estoque=3|categoria=Moda
PILHA|codigo=P1
FILA|pedido=PED2|cliente=Leo|valor=50.0|itens=P1,P2
HISTORICO|pedido=PED1|cliente=Bia|valor=60.5|itens=P1,P2
```

- A pilha é gravada da base para o topo e a fila do início para o fim, para que a ordem seja restaurada ao carregar.
- Na árvore, cada linha é o caminho da raiz até uma folha; ao carregar, os níveis são recriados a partir desses caminhos.
- `FILA` guarda os pedidos pendentes e `HISTORICO` os pedidos já aprovados.
