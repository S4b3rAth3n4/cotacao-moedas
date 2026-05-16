import requests

API_URL = "https://economia.awesomeapi.com.br/json/last"

MOEDAS_DISPONIVEIS = {
    "1": ("USD", "Dólar Americano"),
    "2": ("EUR", "Euro"),
    "3": ("GBP", "Libra Esterlina"),
    "4": ("BTC", "Bitcoin"),
    "5": ("ARS", "Peso Argentino"),
}


def buscar_cotacao(moeda: str) -> dict:
    """Busca a cotação de uma moeda em relação ao Real (BRL) na API."""
    par = f"{moeda}-BRL"
    resposta = requests.get(f"{API_URL}/{par}", timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    chave = par.replace("-", "")
    return dados[chave]


def converter(valor: float, cotacao: float) -> float:
    """Converte um valor em moeda estrangeira para BRL."""
    return valor * cotacao


def exibir_menu():
    print("\n========================================")
    print("   💱 CONVERSOR DE MOEDAS PARA BRL")
    print("========================================")
    print("Escolha a moeda que deseja converter:\n")
    for numero, (codigo, nome) in MOEDAS_DISPONIVEIS.items():
        print(f"  [{numero}] {codigo} - {nome}")
    print("  [0] Sair")
    print("----------------------------------------")


def main():
    print("\nBem-vindo ao Conversor de Moedas!")

    while True:
        exibir_menu()

        escolha = input("Digite o número da moeda: ").strip()

        if escolha == "0":
            print("\nAté logo! 👋\n")
            break

        if escolha not in MOEDAS_DISPONIVEIS:
            print("\n❌ Opção inválida. Tente novamente.")
            continue

        codigo, nome = MOEDAS_DISPONIVEIS[escolha]

        try:
            valor_str = input(f"Digite o valor em {codigo} que deseja converter: ").strip()
            valor = float(valor_str.replace(",", "."))
        except ValueError:
            print("\n❌ Valor inválido. Digite um número.")
            continue

        try:
            print(f"\n🔄 Buscando cotação de {codigo}...")
            dados = buscar_cotacao(codigo)
            cotacao = float(dados["bid"])
            resultado = converter(valor, cotacao)

            print(f"\n✅ Cotação atual: 1 {codigo} = R$ {cotacao:.4f}")
            print(f"💰 {valor:.2f} {codigo} = R$ {resultado:.2f}")
            print(f"   (Fonte: AwesomeAPI | Atualizado: {dados['create_date']})")

        except requests.exceptions.ConnectionError:
            print("\n❌ Erro de conexão. Verifique sua internet.")
        except requests.exceptions.Timeout:
            print("\n❌ A API demorou demais para responder. Tente novamente.")
        except requests.exceptions.HTTPError as e:
            print(f"\n❌ Erro na API: {e}")
        except (KeyError, ValueError):
            print("\n❌ Erro ao processar os dados da API.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
