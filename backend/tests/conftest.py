import shutil
from io import BytesIO
from pathlib import Path

import pytest
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from PIL import Image

from products.models import Product


@pytest.fixture(autouse=True)
def isolated_media_root(settings, tmp_path):
    """Garante que os uploads de imagens fiquem em um diretório temporário e sejam removidos ao final do teste."""
    media_root = tmp_path / "media"
    media_root.mkdir(parents=True, exist_ok=True)
    settings.MEDIA_ROOT = str(media_root)
    yield
    if media_root.exists():
        shutil.rmtree(media_root, ignore_errors=True)

@pytest.fixture
def api_client():
    """Retorna uma instância limpa do cliente de teste do Django REST Framework."""
    return APIClient()

@pytest.fixture
def db_setup(db):
    """Garante acesso ao banco de dados e cria os grupos necessários."""
    Group.objects.get_or_create(name='Gerentes')

@pytest.fixture
def regular_user(db_setup):
    """Cria e retorna um usuário comum (cliente) no banco de dados."""
    return User.objects.create_user(username="cliente", password="user123", email="cliente@email.com")

@pytest.fixture
def gerente_user(db_setup):
    """Cria um usuário e o adiciona ao grupo de Gerentes."""
    user = User.objects.create_user(username="gerente", password="manager123", email="gerente@email.com")
    grupo_gerentes = Group.objects.get(name='Gerentes')
    user.groups.add(grupo_gerentes)
    return user

@pytest.fixture
def gerente_client(api_client, gerente_user):
    """Retorna o APIClient já autenticado com o Token JWT do usuário Gerente."""
    response = api_client.post('/api/token/', {"username": "gerente", "password": "manager123"})
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture
def regular_client(api_client, regular_user):
    """Retorna o APIClient já autenticado com o Token JWT do usuário comum."""
    response = api_client.post('/api/token/', {"username": "cliente", "password": "user123"})
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture
def sample_image():
    """Gera uma imagem válida em memória de 10x10 pixels (JPEG)."""
    file_io = BytesIO()
    image = Image.new('RGB', (10, 10), 'white')
    image.save(file_io, 'JPEG')
    file_io.seek(0)
    return SimpleUploadedFile("produto.jpg", file_io.read(), content_type="image/jpeg")

@pytest.fixture
def large_image():
    """Gera uma imagem válida com tamanho superior a 2MB para testar a regra de limite."""
    image = Image.effect_noise((5000, 5000), 100)
    file_io = BytesIO()
    image.save(file_io, 'JPEG', quality=95)
    file_io.seek(0)
    return SimpleUploadedFile("imagem_gigante.jpg", file_io.read(), content_type="image/jpeg")

@pytest.fixture
def invalid_extension_file():
    """Retorna um arquivo binário com extensão inválida (GIF)."""
    file_io = BytesIO()
    image = Image.new('RGB', (5, 5), 'blue')
    image.save(file_io, 'GIF')
    file_io.seek(0)
    return SimpleUploadedFile("foto_invalida.gif", file_io.read(), content_type="image/gif")

@pytest.fixture
def sample_product(db_setup):
    """Cria um produto no banco de dados com estoque controlado."""
    return Product.objects.create(
        name="Notebook Gamer",
        description="Core i7 16GB",
        price=5000.00,
        stock=10,
        category="Informática"
    )
