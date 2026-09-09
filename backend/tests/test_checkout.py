import pytest

@pytest.mark.django_db
class TestCheckoutIntegrado:

    def test_checkout_sucesso_reduz_estoque(self, regular_client, sample_product):
        """Fluxo completo de compra bem-sucedida: calcula o total e decrementa o estoque de produtos."""
        payload = {
            "items": [
                {
                    "product_id": sample_product.id,
                    "quantity": 3
                }
            ]
        }
        # Executa requisição POST protegida
        response = regular_client.post('/api/checkout/', payload, format='json')
        
        assert response.status_code == 200
        assert response.data['mensagem'] == "Checkout finalizado com sucesso!"
        # Preço unitário (5000.00) * 3 = 15000.00
        assert response.data['total_da_compra'] == 15000.00
        
        # Atualiza a model vinda do banco e verifica se o estoque foi para 7 (tínhamos 10)
        sample_product.refresh_from_db()
        assert sample_product.stock == 7

    def test_checkout_bloqueado_estoque_insuficiente(self, regular_client, sample_product):
        """Valida se a compra é barrada caso o usuário tente comprar mais unidades do que o estoque disponível."""
        payload = {
            "items": [
                {
                    "product_id": sample_product.id,
                    "quantity": 11 # Temos apenas 10 no estoque
                }
            ]
        }
        response = regular_client.post('/api/checkout/', payload, format='json')
        
        assert response.status_code == 400
        assert "Estoque insuficiente" in response.data['detail']
        
        # Garante que o estoque original não foi alterado devido ao erro de validação
        sample_product.refresh_from_db()
        assert sample_product.stock == 10

    def test_checkout_produto_inexistente(self, regular_client):
        """Valida se a API retorna HTTP 400 amigável informando que o ID do produto é inválido."""
        payload = {
            "items": [
                {
                    "product_id": 9999, # ID não existente no banco
                    "quantity": 1
                }
            ]
        }
        response = regular_client.post('/api/checkout/', payload, format='json')
        assert response.status_code == 400
        assert "não existe no catálogo" in response.data['detail']

