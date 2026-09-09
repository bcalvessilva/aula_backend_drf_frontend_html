# Projeto: E-commerce com Django REST Framework + Frontend HTML/JS

Este projeto foi desenvolvido como uma aplicação de e-commerce simples, com uma API REST em Django e uma interface em HTML, CSS e JavaScript consumindo essa API. A arquitetura foi pensada para separar claramente:

- camada de negócio e regras de validação no backend
- camada de interação e experiência do usuário no frontend
- regras gerais e consulta de comportamento no README raiz do projeto

## Visão geral

O sistema expõe um catálogo de produtos, permite autenticação de usuários via JWT, mantém um carrinho no navegador e executa o checkout com validação do estoque e do total da compra.

A ideia central do projeto é demonstrar como o frontend e o backend podem trabalhar juntos, mantendo a regra de negócio em um local de autoridade e deixando a camada de apresentação responsável apenas pela experiência visual e interação.

## O que foi desenvolvido

### Backend
- API REST com Django REST Framework
- Modelagem de produtos com imagem, preço, estoque e categoria
- Endpoints para autenticação JWT
- Endpoints para listagem/gerenciamento de produtos
- Checkout com validação de estoque, ID de produto e total da compra
- Permissões por grupo para operações administrativas
- Validação de imagens e preço no serializer
- Testes de API cobrindo regras críticas

### Frontend
- Vitrine de produtos em HTML
- Carrinho de compras em JavaScript com armazenamento em localStorage
- Login com diálogo modal
- Visualização do status do usuário
- Cálculo de subtotal, total e economia promocional
- Envio do checkout para a API autentica

## Regras do projeto

As regras devem ser interpretadas em camadas:

1. Regras de negócio e validação crítica: ficam no backend.
2. Regras de experiência e interface: ficam no frontend.
3. O README raiz explica o contexto geral e orienta para a regra específica de cada camada.

### Regra de autoridade

A regra principal é que o backend é a fonte de verdade da aplicação. Mesmo que o frontend valide alguns pontos no navegador, o servidor é quem decide se a operação pode prosseguir.

Isso vale para:
- preço válido
- imagem válida
- estoque suficiente
- produto existente
- autorização para ações administrativas
- cálculo final do checkout

## Backend

A pasta [backend](backend) contém toda a lógica da API, modelos, serializadores, permissões, rotas e testes.

A estrutura principal inclui:
- [backend/products](backend/products): modelos, serializers, permissões, views e rotas
- [backend/setupecommerce](backend/setupecommerce): settings do Django
- [backend/tests](backend/tests): testes de validação e checkout

Para consultar a documentação técnica do backend, acesse:
- [backend/README.md](backend/README.md)

## Frontend

A pasta [frontend](frontend) contém a interface web da aplicação. Ela consome a API Django e oferece a experiência do usuário.

A estrutura principal inclui:
- [frontend/index.html](frontend/index.html): página principal
- [frontend/style.css](frontend/style.css): estilos
- [frontend/app.js](frontend/app.js): lógica de autenticação, carrinho e checkout

Para consultar a documentação técnica do frontend, acesse:
- [frontend/README.md](frontend/README.md)

## Como consultar a regra específica em cada camada

### Se a dúvida for sobre regra de negócio
Consulte o backend:
- [backend/README.md](backend/README.md)
- [backend/products/views.py](backend/products/views.py)
- [backend/products/serializers.py](backend/products/serializers.py)
- [backend/products/permissions.py](backend/products/permissions.py)

### Se a dúvida for sobre comportamento da interface
Consulte o frontend:
- [frontend/README.md](frontend/README.md)
- [frontend/app.js](frontend/app.js)
- [frontend/index.html](frontend/index.html)

### Se a dúvida for sobre o projeto como um todo
Use este README raiz como guia de visão geral e referências.

## Fluxo principal do projeto

1. O usuário acessa a vitrine no frontend.
2. O frontend busca os produtos na API do backend.
3. O usuário escolhe itens para o carrinho.
4. O frontend valida limite de estoque localmente.
5. Ao finalizar a compra, o usuário pode ser solicitado a autenticar.
6. O backend recebe os itens do carrinho e valida:
   - existência do produto
   - quantidade disponível
   - autorização do usuário
   - valor total da compra
7. O estoque é atualizado somente após a validação final.

## Observações finais

Este projeto foi estruturado para fins de estudo e demonstração prática de integração entre backend e frontend. Como regra de organização, a parte técnica detalhada permanece nos READMEs de cada pasta, enquanto este README raiz funciona como mapa geral do projeto, explicando objetivos, regras e a forma correta de consultar a regra específica em cada camada.
