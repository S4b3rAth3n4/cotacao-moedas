import pytest
import requests
from unittest.mock import patch, MagicMock
from main import buscar_cotacao, converter


class TestIntegracaoAPI:

    @pytest.mark.skipif(
        not __import__('os').getenv('RUN_INTEGRATION'),
        reason="Testes de integração real pulados no CI"
    )
    def test_busca_cotacao_usd_retorna_dados(self):
        dados = buscar_cotacao("USD")
        assert dados is not None
        assert "bid" in dados
        assert "ask" in dados
        assert "create_date" in dados

    @pytest.mark.skipif(
        not __import__('os').getenv('RUN_INTEGRATION'),
        reason="Testes de integração real pulados no CI"
    )
    def test_cotacao_usd_e_numero_valido(self):
        dados = buscar_cotacao("USD")
        cotacao = float(dados["bid"])
        assert cotacao > 0

    @pytest.mark.skipif(
        not __import__('os').getenv('RUN_INTEGRATION'),
        reason="Testes de integração real pulados no CI"
    )
    def test_busca_cotacao_eur_retorna_dados(self):
        dados = buscar_cotacao("EUR")
        assert dados is not None
        assert "bid" in dados

    def test_moeda_invalida_levanta_excecao(self):
        with pytest.raises(requests.exceptions.HTTPError):
            buscar_cotacao("XXX")


class TestMockAPI:

    @patch("main.requests.get")
    def test_buscar_cotacao_retorna_chave_correta(self, mock_get):
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

    @patch("main.requests.get")
    def test_erro_de_conexao_levanta_excecao(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Sem internet")
        with pytest.raises(requests.exceptions.ConnectionError):
            buscar_cotacao("USD")

    @patch("main.requests.get")
    def test_timeout_levanta_excecao(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")
        with pytest.raises(requests.exceptions.Timeout):
            buscar_cotacao("USD")


class TestConversor:

    def test_converter_um_dolar(self):
        assert converter(1.0, 5.0) == 5.0

    def test_converter_valor_decimal(self):
        assert converter(0.5, 5.0) == pytest.approx(2.50)

    def test_converter_valor_grande(self):
        assert converter(1000.0, 5.20) == pytest.approx(5200.0)

    def test_converter_zero(self):
        assert converter(0.0, 5.0) == 0.0