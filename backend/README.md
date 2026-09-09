# Backend - Django REST Framework

Este diretório concentra a API do projeto, a regra de negócio, as validações críticas e o armazenamento de dados. Ele é a camada de autoridade da aplicação: todas as decisões de negócio relevantes devem ser validadas aqui antes de qualquer alteração persistente.

## Visão geral

O backend foi desenvolvido em Django com Django REST Framework e expõe uma API para gerenciar produtos, autenticar usuários e processar o checkout do carrinho de compras. A aplicação foi pensada para ser consumida por um frontend estático em HTML, CSS e JavaScript.

A regra geral do projeto é simples:

- o frontend cuida da experiência do usuário
- o backend cuida da regra de negócio e da integridade dos dados
- o README raiz explica o contexto geral do projeto e aponta para a regra específica de cada camada

## Objetivo da API

A API fornece:

- autenticação via JWT
- listagem e gerenciamento de produtos
- controle de acesso para operações de escrita
- validação de dados de produto
- processamento seguro de checkout com decremento de estoque

## Stack tecnológica

- Python
- Django
- Django REST Framework
- DRF Spectacular
- SimpleJWT
- SQLite (configuração padrão do projeto)

## Estrutura principal

- `setupecommerce/`: configuração do projeto Django
- `products/`: modelos, serializers, permissões, views, URLs e regras de negócio
- `tests/`: testes automatizados para validação e checkout
- `media/`: arquivos de mídia carregados pelos produtos

## Modelos principais

### Product

O modelo `Product` representa um item do catálogo com os seguintes campos:

- `name`: nome do produto
- `description`: descrição
- `price`: preço do produto
- `stock`: quantidade disponível em estoque
- `category`: categoria do produto
- `image`: imagem do produto com upload para `products/`

## Regras de negócio e validação

### 1. Preço do produto
No serializer, o valor do produto deve ser maior que zero.

Regra aplicada:
- `price > 0`
- caso contrário, retorna erro `400 Bad Request`

Mensagem:
- "O preço do produto deve ser maior que R$ 0,00."

### 2. Imagem do produto
A imagem deve obedecer a regras de segurança e qualidade:

- tamanho máximo: 2MB
- extensões permitidas: `.jpg`, `.jpeg`, `.png`
- qualquer outro formato ou arquivo excedente deve ser bloqueado

Se a validação falhar, a API responde com erro de serialização e não persiste o produto.

### 3. Estoque
O estoque é parte central da operação.

No checkout:
- cada item deve ter `quantity >= 1`
- o produto precisa existir no catálogo
- a quantidade solicitada não pode ser maior que o estoque disponível

Se qualquer condição falhar, o backend responde com `400 Bad Request` e não atualiza o estoque.

### 4. Permissões
As regras de acesso foram separadas em permissões:

- leitura pública: usuários autenticados ou anônimos podem consultar os produtos
- escrita restrita: todas as operações de escrita exigem grupo `Gerentes` ou usuário admin/funcionário
  - criação de produto
  - atualização de produto
  - atualização parcial de produto
  - exclusão de produto
  - qualquer ação que altere o estado persistido do sistema

A permissão fica em `products/permissions.py`.

### 5. Checkout
O endpoint de checkout tem responsabilidade crítica:

- recebe a lista de itens do carrinho
- valida cada produto e quantidade
- calcula o total da compra
- reduz o estoque apenas quando todas as validações passarem

Essa abordagem evita inconsistências e garante integridade transacional da operação.

## Endpoints principais

### Autenticação

- `POST /api/token/` -> gera tokens JWT
- `POST /api/token/refresh/` -> atualiza token JWT

### Produtos

- `GET /api/products/` -> lista produtos
- `POST /api/products/` -> cria produto (somente gerentes/admin)
- `GET /api/products/<id>/` -> detalhe do produto
- `PUT /api/products/<id>/` -> atualização completa (somente gerentes/admin)
- `PATCH /api/products/<id>/` -> atualização parcial (somente gerentes/admin)
- `DELETE /api/products/<id>/` -> exclusão (somente gerentes/admin)

### Checkout

- `POST /api/checkout/` -> finaliza compra

Payload esperado:

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

Resposta de sucesso:

```json
{
  "mensagem": "Checkout finalizado com sucesso!",
  "usuario": "admin",
  "total_da_compra": 150.0
}
```

## Arquivos-chave

- `products/models.py`: modelo `Product`
- `products/serializers.py`: validações e estrutura do payload
- `products/views.py`: endpoints e regra de checkout
- `products/permissions.py`: regras de acesso
- `products/urls.py`: mapeamento das rotas da API
- `tests/test_checkout.py`: validação de fluxo de compra
- `tests/test_validation.py`: validações de preço e imagem

## Testes

Os testes automatizados cobrem os comportamentos mais sensíveis do backend:

- preço inválido
- imagem grande ou com extensão inválida
- checkout com sucesso
- estoque insuficiente
- produto inexistente

Para executar os testes:

```powershell
cd backend
python -m pytest
```

## Setup rápido

```powershell
# criar o ambiente virtual
python -m venv .venv

# ativar o ambiente
.\.venv\Scripts\Activate.ps1

# instalar dependências
python -m pip install --upgrade pip
pip install -r requirements.txt

# aplicar migrations
python manage.py migrate

# opcional: criar superusuário
python manage.py createsuperuser

# iniciar servidor
python manage.py runserver
```

> Se estiver usando CMD, utilize `\.venv\Scripts\activate` em vez do PowerShell.

## Observação importante

A regra técnica detalhada do backend está neste README e nos arquivos da pasta `products`. O README raiz do projeto continua sendo a referência de visão geral e de navegação entre as camadas.

Para consultar a parte visual e de interação com o usuário, veja o frontend em `../frontend/README.md`.

