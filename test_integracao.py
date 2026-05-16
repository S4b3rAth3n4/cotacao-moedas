"""
Testes de integração para o Conversor de Moedas.
Valida a comunicação com a AwesomeAPI e o fluxo de dados.
"""

import pytest
import requests
from unittest.mock import patch, MagicMock
from main import buscar_cotacao, converter


# ─── Testes de Integração (comunicação real com a API) ────────────────────────

class TestIntegracaoAPI:
    """Testa a comunicação real com a AwesomeAPI."""

    def test_busca_cotacao_usd_retorna_dados(self):
        """Verifica se a API retorna dados válidos para USD-BRL."""
        dados = buscar_cotacao("USD")

        assert dados is not None
        assert "bid" in dados, "Resposta não contém o campo 'bid' (preço de compra)"
        assert "ask" in dados, "Resposta não contém o campo 'ask' (preço de venda)"
        assert "create_date" in dados, "Resposta não contém o campo 'create_date'"

    def test_cotacao_usd_e_numero_valido(self):
        """Verifica se o valor retornado para USD pode ser convertido para float."""
        dados = buscar_cotacao("USD")
        cotacao = float(dados["bid"])

        assert cotacao > 0, "A cotação do USD deve ser maior que zero"

    def test_busca_cotacao_eur_retorna_dados(self):
        """Verifica se a API retorna dados válidos para EUR-BRL."""
        dados = buscar_cotacao("EUR")

        assert dados is not None
        assert "bid" in dados

    def test_moeda_invalida_levanta_excecao(self):
        """Verifica se uma moeda inexistente causa erro HTTP da API."""
        with pytest.raises(requests.exceptions.HTTPError):
            buscar_cotacao("XXX")


# ─── Testes com Mock (sem chamar a API de verdade) ────────────────────────────

class TestMockAPI:
    """Testa o fluxo com respostas simuladas (mock) da API."""

    @patch("main.requests.get")
    def test_buscar_cotacao_retorna_chave_correta(self, mock_get):
        """Simula resposta da API e verifica se a função extrai a chave certa."""
        resposta_simulada = {
            "USDBRL": {
                "bid": "5.2345",
                "ask": "5.2400",
                "create_date": "2025-01-01 10:00:00"
            }
        }
        mock_response = MagicMock()
        mock_response.json.return_value = resposta_simulada
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        resultado = buscar_cotacao("USD")

        assert resultado["bid"] == "5.2345"
        assert resultado["create_date"] == "2025-01-01 10:00:00"

    @patch("main.requests.get")
    def test_erro_de_conexao_levanta_excecao(self, mock_get):
        """Simula falha de rede e verifica se a exceção é propagada."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Sem internet")

        with pytest.raises(requests.exceptions.ConnectionError):
            buscar_cotacao("USD")

    @patch("main.requests.get")
    def test_timeout_levanta_excecao(self, mock_get):
        """Simula timeout e verifica se a exceção é propagada."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")

        with pytest.raises(requests.exceptions.Timeout):
            buscar_cotacao("USD")


# ─── Testes Unitários da função converter ─────────────────────────────────────

class TestConversor:
    """Testa a lógica de conversão de valores."""

    def test_converter_um_dolar(self):
        """1 USD com cotação 5.00 deve resultar em R$ 5.00."""
        assert converter(1.0, 5.0) == 5.0

    def test_converter_valor_decimal(self):
        """0.5 USD com cotação 5.00 deve resultar em R$ 2.50."""
        assert converter(0.5, 5.0) == pytest.approx(2.50)

    def test_converter_valor_grande(self):
        """1000 USD com cotação 5.20 deve resultar em R$ 5200.00."""
        assert converter(1000.0, 5.20) == pytest.approx(5200.0)

    def test_converter_zero(self):
        """0 USD deve sempre resultar em R$ 0.00."""
        assert converter(0.0, 5.0) == 0.0
