import pytest

@pytest.mark.django_db
class TestPermissoesECommerce:

    def test_leitura_catalogo_publica(self, api_client, sample_product):
        """Garante que qualquer pessoa (anônima) possa ver a lista de produtos."""
        response = api_client.get('/api/products/')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == "Notebook Gamer"

    def test_escrita_catalogo_anotimo_negada(self, api_client):
        """Garante que um usuário não autenticado receba bloqueio HTTP 401 ao tentar criar produto."""
        payload = {
            "name": "Mouse Gamer",
            "price": "150.00",
            "stock": 5
        }
        response = api_client.post('/api/products/', payload)
        assert response.status_code == 401

    def test_escrita_catalogo_cliente_comum_negada(self, regular_client):
        """Garante que um usuário autenticado, mas que não pertence ao grupo 'Gerentes' receba HTTP 403."""
        payload = {
            "name": "Teclado RGB",
            "price": "300.00",
            "stock": 4
        }
        response = regular_client.post('/api/products/', payload)
        assert response.status_code == 403

    def test_escrita_catalogo_gerente_permitida(self, gerente_client, sample_image):
        """Garante que usuários pertencentes ao grupo 'Gerentes' consigam criar produtos com sucesso (HTTP 201)."""
        payload = {
            "name": "Headset Gamer",
            "description": "Som surround 7.1",
            "price": "450.00",
            "stock": 12,
            "category": "Periféricos",
            "image": sample_image
        }
        # Enviamos os dados codificados como form-data por conta da imagem
        response = gerente_client.post('/api/products/', payload, format='multipart')
        assert response.status_code == 201
        assert response.data['name'] == "Headset Gamer"
        assert 'image' in response.data
        assert response.data['image'] is not None

    def test_atualizacao_catalogo_cliente_comum_negada(self, regular_client, sample_product):
        """Garante que um usuário comum receba HTTP 403 ao tentar atualizar um produto."""
        payload = {
            "name": "Notebook Gamer Atualizado",
            "price": "6000.00",
            "stock": 8
        }
        response = regular_client.put(f'/api/products/{sample_product.id}/', payload)
        assert response.status_code == 403

    def test_remocao_catalogo_cliente_comum_negada(self, regular_client, sample_product):
        """Garante que um usuário comum receba HTTP 403 ao tentar remover um produto."""
        response = regular_client.delete(f'/api/products/{sample_product.id}/')
        assert response.status_code == 403

    def test_atualizacao_catalogo_gerente_permitida(self, gerente_client, sample_product):
        """Garante que um gerente consiga atualizar um produto com sucesso."""
        payload = {
            "name": "Notebook Gamer Atualizado",
            "price": "6500.00",
            "stock": 9
        }
        response = gerente_client.patch(f'/api/products/{sample_product.id}/', payload)
        assert response.status_code == 200
        assert response.data['name'] == "Notebook Gamer Atualizado"
        assert response.data['price'] == "6500.00"

    def test_remocao_catalogo_gerente_permitida(self, gerente_client, sample_product):
        """Garante que um gerente consiga remover um produto com sucesso."""
        response = gerente_client.delete(f'/api/products/{sample_product.id}/')
        assert response.status_code == 204
