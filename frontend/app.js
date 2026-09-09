// ==========================================================================
// APP.JS - LÓGICA CONSOLIDADA DO FRONTEND (AULA 27)
// ==========================================================================

const API_BASE_URL = 'http://127.0.0.1:8000';

// Estado global mantido no navegador
let carrinho = JSON.parse(localStorage.getItem('computer_carrinho')) || [];
let produtosCache = [];
let tokenAcesso = localStorage.getItem('computer_jwt_token') || null;
let usuarioLogado = localStorage.getItem('computer_username') || null;
let loginPendendeAposAutenticacao = null;

// Inicialização da aplicação ao carregar o DOM
window.addEventListener('DOMContentLoaded', () => {
    atualizarPainelAuthVisual();
    carregarVitrine();
    atualizarCarrinhoVisual();
    fecharModalLogin();
});

// --------------------------------------------------------------------------
// 1. AUTENTICAÇÃO AUTOMÁTICA JWT (LOGIN & LOGOUT)
// --------------------------------------------------------------------------

function abrirModalLogin(acaoPosterior = null) {
    loginPendendeAposAutenticacao = acaoPosterior;

    const modal = document.getElementById('auth-modal');
    if (!modal) return;

    modal.classList.remove('hidden');
    document.getElementById('auth-username').focus();
}

function fecharModalLogin() {
    const modal = document.getElementById('auth-modal');
    if (!modal) return;

    modal.classList.add('hidden');
    document.getElementById('auth-username').value = '';
    document.getElementById('auth-password').value = '';
}

async function realizarLogin() {
    const usernameInput = document.getElementById('auth-username').value.trim();
    const passwordInput = document.getElementById('auth-password').value.trim();

    if (!usernameInput || !passwordInput) {
        alert('Por favor, preencha o usuário e a senha!');
        return;
    }

    try {
        const resposta = await fetch(`${API_BASE_URL}/api/token/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: usernameInput,
                password: passwordInput
            })
        });

        const dados = await resposta.json();

        if (resposta.ok && dados.access) {
            tokenAcesso = dados.access;
            usuarioLogado = usernameInput;

            localStorage.setItem('computer_jwt_token', tokenAcesso);
            localStorage.setItem('computer_username', usuarioLogado);

            document.getElementById('auth-password').value = '';
            atualizarPainelAuthVisual();
            fecharModalLogin();

            if (loginPendendeAposAutenticacao === 'checkout') {
                loginPendendeAposAutenticacao = null;
                finalizarCompra();
                return;
            }

            loginPendendeAposAutenticacao = null;
            alert(`Bem-vindo(a), ${usuarioLogado}! Autenticação realizada com sucesso.`);
        } else {
            alert(`Erro no login: ${dados.detail || 'Credenciais inválidas.'}`);
        }
    } catch (erro) {
        alert(`Erro ao conectar com o servidor de autenticação: ${erro.message}`);
    }
}

function realizarLogout() {
    tokenAcesso = null;
    usuarioLogado = null;
    loginPendendeAposAutenticacao = null;
    localStorage.removeItem('computer_jwt_token');
    localStorage.removeItem('computer_username');
    atualizarPainelAuthVisual();
    alert('Sessão encerrada com sucesso.');
}

function atualizarPainelAuthVisual() {
    const userDisplay = document.getElementById('user-display');
    const loggedUsernameText = document.getElementById('logged-username-text');
    const loginButton = document.getElementById('btn-login-header');
    const userMenu = document.getElementById('user-menu');

    if (tokenAcesso && usuarioLogado) {
        loginButton.style.display = 'none';
        userMenu.style.display = 'flex';
        loggedUsernameText.innerText = usuarioLogado;
        userDisplay.innerHTML = `Status: <strong>Logado (${usuarioLogado})</strong>`;
    } else {
        loginButton.style.display = 'inline-flex';
        userMenu.style.display = 'none';
        userDisplay.innerHTML = `Status: <strong>Não autenticado</strong>`;
    }
}

// --------------------------------------------------------------------------
// 2. CARREGAMENTO DA VITRINE DE PRODUTOS (FETCH REST)
// --------------------------------------------------------------------------

async function carregarVitrine() {
    const container = document.getElementById('grid-produtos');
    container.innerHTML = '<p>Carregando catálogo do servidor...</p>';

    try {
        const resposta = await fetch(`${API_BASE_URL}/api/products/`);

        if (!resposta.ok) throw new Error('Erro ao buscar a lista de produtos.');

        produtosCache = await resposta.json();
        container.innerHTML = '';

        if (produtosCache.length === 0) {
            container.innerHTML = '<p>Nenhum produto cadastrado no catálogo.</p>';
            return;
        }

        produtosCache.forEach(produto => {
            // Resolve URLs relativas e absolutas das imagens físicas de mídia
            let imagemUrl = 'https://via.placeholder.com/150';
            if (produto.image) {
                imagemUrl = produto.image.startsWith('http')
                    ? produto.image
                    : `${API_BASE_URL}${produto.image}`;
            }

            const precoEfetivo = parseFloat(produto.promo_price || produto.price);

            const card = document.createElement('div');
            card.className = 'card-produto';
            card.innerHTML = `
                <div>
                    <img src="${imagemUrl}" alt="${produto.name}" onerror="this.src='https://via.placeholder.com/150'">
                    <h3>${produto.name}</h3>
                    <p class="preco">R$ ${precoEfetivo.toFixed(2)}</p>
                    <p class="estoque">Estoque: ${produto.stock} unid.</p>
                </div>
                <button onclick="adicionarAoCarrinho(${produto.id})">Adicionar ao Carrinho</button>
            `;
            container.appendChild(card);
        });

    } catch (erro) {
        container.innerHTML = `<p style="color: red;">Erro ao carregar vitrine: ${erro.message}</p>`;
    }
}

// --------------------------------------------------------------------------
// 3. GERENCIAMENTO DE ESTADO E LOCALSTORAGE DO CARRINHO
// --------------------------------------------------------------------------

function adicionarAoCarrinho(produtoId) {
    const produtoBD = produtosCache.find(p => p.id === produtoId);
    if (!produtoBD) return;

    const itemExistente = carrinho.find(item => item.id === produtoId);
    const quantidadeAtual = itemExistente ? itemExistente.quantity : 0;

    // Validação local de estoque
    if (quantidadeAtual + 1 > produtoBD.stock) {
        alert(`Estoque máximo atingido para ${produtoBD.name} (${produtoBD.stock} disponíveis).`);
        return;
    }

    if (itemExistente) {
        itemExistente.quantity += 1;
    } else {
        carrinho.push({
            id: produtoBD.id,
            name: produtoBD.name,
            price: parseFloat(produtoBD.price),
            promo_price: produtoBD.promo_price ? parseFloat(produtoBD.promo_price) : null,
            quantity: 1
        });
    }

    salvarNoLocalStorage();
    atualizarCarrinhoVisual();
}

function alterarQuantidade(produtoId, delta) {
    const item = carrinho.find(i => i.id === produtoId);
    if (!item) return;

    const produtoBD = produtosCache.find(p => p.id === produtoId);

    if (delta > 0 && produtoBD && (item.quantity + delta > produtoBD.stock)) {
        alert(`Limite de estoque atingido (${produtoBD.stock} unidades).`);
        return;
    }

    item.quantity += delta;

    if (item.quantity <= 0) {
        carrinho = carrinho.filter(i => i.id !== produtoId);
    }

    salvarNoLocalStorage();
    atualizarCarrinhoVisual();
}

function salvarNoLocalStorage() {
    localStorage.setItem('computer_carrinho', JSON.stringify(carrinho));
}

function atualizarCarrinhoVisual() {
    const listaContainer = document.getElementById('lista-carrinho');
    const contadorElemento = document.getElementById('contador-carrinho');
    const totalElemento = document.getElementById('valor-total');
    const economiaElemento = document.getElementById('economia-box');

    listaContainer.innerHTML = '';

    let totalGeral = 0;
    let totalEconomia = 0;
    let totalItens = 0;

    if (carrinho.length === 0) {
        listaContainer.innerHTML = '<p style="color: #666; font-size: 0.9rem;">Seu carrinho está vazio.</p>';
    } else {
        carrinho.forEach(item => {
            const precoEfetivo = item.promo_price ? item.promo_price : item.price;
            const subtotal = precoEfetivo * item.quantity;

            totalGeral += subtotal;
            totalItens += item.quantity;

            if (item.promo_price && item.promo_price < item.price) {
                totalEconomia += (item.price - item.promo_price) * item.quantity;
            }

            const divItem = document.createElement('div');
            divItem.className = 'item-carrinho';
            divItem.innerHTML = `
                <div class="item-carrinho-info">
                    <strong>${item.name}</strong>
                    <small>R$ ${precoEfetivo.toFixed(2)} x ${item.quantity}</small>
                </div>
                <div class="controles-qtd">
                    <button onclick="alterarQuantidade(${item.id}, -1)">-</button>
                    <button onclick="alterarQuantidade(${item.id}, 1)">+</button>
                </div>
            `;
            listaContainer.appendChild(divItem);
        });
    }

    contadorElemento.innerText = `${totalItens} ${totalItens === 1 ? 'item' : 'itens'}`;
    totalElemento.innerText = totalGeral.toFixed(2);

    if (totalEconomia > 0) {
        economiaElemento.innerText = `Você está economizando R$ ${totalEconomia.toFixed(2)} nesta compra!`;
    } else {
        economiaElemento.innerText = '';
    }
}

// --------------------------------------------------------------------------
// 4. CHECKOUT COM ENVIO DO BEARER TOKEN AUTOMÁTICO
// --------------------------------------------------------------------------

async function finalizarCompra() {
    if (carrinho.length === 0) {
        alert('Seu carrinho está vazio!');
        return;
    }

    if (!tokenAcesso) {
        abrirModalLogin('checkout');
        return;
    }

    const payload = {
        items: carrinho.map(item => ({
            product_id: parseInt(item.id, 10),
            quantity: parseInt(item.quantity, 10)
        }))
    };

    try {
        const resposta = await fetch(`${API_BASE_URL}/api/checkout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${tokenAcesso}`
            },
            body: JSON.stringify(payload)
        });

        const dados = await resposta.json();

        if (resposta.ok) {
            alert(`✅ ${dados.mensagem || 'Compra realizada com sucesso!'}
Total da compra: R$ ${dados.total_da_compra.toFixed(2)}`);

            // Limpa o carrinho após compra bem-sucedida
            carrinho = [];
            localStorage.removeItem('computer_carrinho');
            atualizarCarrinhoVisual();
            carregarVitrine(); // Atualiza estoque na vitrine
        } else if (resposta.status === 401) {
            alert('Sua sessão expirou ou o token é inválido. Por favor, faça login novamente.');
            realizarLogout();
        } else {
            alert(`Erro no checkout: ${dados.detail || JSON.stringify(dados)}`);
        }
    } catch (erro) {
        alert(`Erro ao conectar com o servidor: ${erro.message}`);
    }
}