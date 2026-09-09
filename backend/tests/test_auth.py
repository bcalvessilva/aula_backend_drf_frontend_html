import pytest

@pytest.mark.django_db
class TestAutenticacaoJWT:
    def test_login_sucesso(self, api_client, regular_user):
        """Valida se um usuário cadastrado consegue logar e receber o token access e refresh."""
        payload = {
            "username": "cliente",
            "password": "user123"
        }
        response = api_client.post('/api/token/', payload)
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_senha_incorreta(self, api_client, regular_user):
        """Garante que tentativas de login com senhas inválidas sejam rejeitadas com HTTP 401."""
        payload = {
            "username": "cliente",
            "password": "senha_errada"
        }
        response = api_client.post('/api/token/', payload)
        assert response.status_code == 401
        assert response.data['detail'] == "No active account found with the given credentials"

    def test_login_usuario_inexistente(self, api_client):
        """Garante que usuários não cadastrados recebam bloqueio HTTP 401."""
        payload = {
            "username": "fantasma",
            "password": "qualquersenha"
        }
        response = api_client.post('/api/token/', payload)
        assert response.status_code == 401
