# Frontend

Este diretório contém a camada de apresentação do projeto: a vitrine de produtos, o carrinho de compras, autenticação e o fluxo de checkout no navegador.

## Objetivo da camada

A interface foi construída para consumir a API do backend em Django REST Framework e entregar uma experiência de e-commerce em uma única página com HTML, CSS e JavaScript vanilla.

## O que foi implementado

- Vitrine de produtos carregada via fetch da API
- Carrinho persistido em localStorage
- Login JWT via modal
- Logout do usuário
- Validação de estoque no frontend antes de incluir itens no carrinho
- Cálculo de total do carrinho e da economia promocional
- Fluxo de checkout que exige autenticação e envia os itens para o backend

## Regras aplicadas no frontend

### 1. Autenticação
- O login é realizado no endpoint `/api/token/`.
- O token JWT é salvo no browser via `localStorage`.
- A tela atualiza o estado visual conforme o usuário está autenticado ou não.
- Se o usuário tentar finalizar a compra sem login, o sistema abre o modal de autenticação e depois continua o checkout.

### 2. Carrinho
- O carrinho é mantido no navegador em `localStorage`.
- Cada item guarda o identificador, nome, preço, promo e quantidade.
- A quantidade máxima de um produto não pode exceder o estoque disponível do backend.

### 3. Promoção e cálculo
- O frontend usa `promo_price` quando disponível e mostra o preço promocional na vitrine.
- O total do carrinho considera o preço final aplicável em cada item.
- A economia é exibida na interface quando houver desconto.

### 4. Checkout
- O botão de finalizar compra dispara a requisição para `/api/checkout/`.
- O payload enviado ao backend contém apenas os itens do carrinho e as quantidades.
- O frontend não deve “confundir” a regra de negócio com a regra de validação: ele apenas orienta a interação; o backend é a fonte final de verdade.

## Arquivos principais

- `index.html`: estrutura da interface com header, vitrine, carrinho e modal de login
- `style.css`: layout visual da loja
- `app.js`: lógica de autenticação, carregamento de produtos, carrinho e checkout

## Como consultar a regra específica

Para entender a regra de negócio completa de cada comportamento, consulte:

- Backend: [../backend/README.md](../backend/README.md)
- Frontend: este arquivo
- Regras gerais do projeto: [../README.md](../README.md)

> A regra técnica detalhada fica na camada correspondente. O README raiz explica o contexto e a orientação geral.
