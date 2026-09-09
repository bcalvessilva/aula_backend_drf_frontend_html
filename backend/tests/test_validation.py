import pytest

@pytest.mark.django_db
class TestValidacoesSerializer:

    def test_preco_invalido_rejeitado(self, gerente_client):
        """Garante que a tentativa de cadastrar produtos com preços negativos ou zerados retorne HTTP 400."""
        payload = {
            "name": "Cabo HDMI",
            "price": "-5.00",
            "stock": 20
        }
        response = gerente_client.post('/api/products/', payload)
        assert response.status_code == 400
        assert 'price' in response.data
        # Mensagem definida no método validate_price do serializer
        assert response.data['price'][0] == "O preço do produto deve ser maior que R$ 0,00."

    def test_imagem_gigante_rejeitada(self, gerente_client, large_image):
        """Garante que arquivos de imagens maiores que 2MB sejam rejeitados pelo serializer."""
        payload = {
            "name": "Monitor UltraWide 34",
            "price": "2500.00",
            "stock": 5,
            "image": large_image
        }
        response = gerente_client.post('/api/products/', payload, format='multipart')
        assert response.status_code == 400
        assert 'image' in response.data
        assert response.data['image'][0] == "O tamanho da imagem não pode ultrapassar 2MB."

    def test_extensao_invalida_rejeitada(self, gerente_client, invalid_extension_file):
        """Garante que o backend rejeite formatos de imagem inseguros (como .gif) nas operações de upload."""
        payload = {
            "name": "Mouse Pad XL",
            "price": "80.00",
            "stock": 10,
            "image": invalid_extension_file
        }
        response = gerente_client.post('/api/products/', payload, format='multipart')
        assert response.status_code == 400
        assert 'image' in response.data
        assert "Extensão inválida" in response.data['image'][0]

