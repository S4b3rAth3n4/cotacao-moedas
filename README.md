# 💱 Conversor de Moedas para BRL

> Aplicação CLI em Python que consulta cotações em tempo real e converte moedas estrangeiras para o Real Brasileiro (BRL).

---

## 🔗 Links

| | |
|---|---|
| 🐙 **Repositório** | [github.com/SEU-USUARIO/cotacao-moedas](https://github.com/SEU-USUARIO/cotacao-moedas) |
| 📦 **Deploy / Como executar** | Veja a seção abaixo |

---

## 📌 Sobre o Projeto

Este projeto foi desenvolvido como parte do **BootCamp - Etapa Intermediária**. A aplicação conecta-se à [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas) para buscar cotações em tempo real e permite ao usuário converter valores de moedas estrangeiras para o Real.

### Moedas suportadas

| Código | Nome |
|--------|------|
| USD | Dólar Americano |
| EUR | Euro |
| GBP | Libra Esterlina |
| BTC | Bitcoin |
| ARS | Peso Argentino |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10 ou superior instalado
- Conexão com a internet

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/cotacao-moedas.git

# 2. Entre na pasta do projeto
cd cotacao-moedas

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python main.py
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest test_integracao.py -v
```

Os testes validam:
- ✅ Comunicação real com a API (integração)
- ✅ Tratamento de erros de rede (mock)
- ✅ Lógica de conversão de valores (unitário)

---

## 🌐 API Utilizada

**AwesomeAPI - Cotação de Moedas**
- URL base: `https://economia.awesomeapi.com.br/json/last`
- Gratuita e aberta, sem necessidade de chave de acesso
- Documentação: [docs.awesomeapi.com.br](https://docs.awesomeapi.com.br/api-de-moedas)

---

## 📁 Estrutura do Projeto

```
cotacao-moedas/
├── main.py                  # Aplicação principal
├── test_integracao.py       # Testes de integração e unitários
├── requirements.txt         # Dependências do projeto
├── README.md                # Este arquivo
└── .github/
    └── workflows/
        └── ci.yml           # Pipeline de CI (GitHub Actions)
```

---

## 🛠️ Tecnologias

- **Python 3.11**
- **requests** — requisições HTTP para a API
- **pytest** — framework de testes
- **GitHub Actions** — integração contínua (CI)
