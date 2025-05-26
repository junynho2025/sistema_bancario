# Banco Simples Web

Este é um projeto de um banco digital simples, desenvolvido em Python utilizando o framework Flask. A aplicação permite realizar depósitos, saques e visualizar o extrato das movimentações diretamente de uma interface web.

## Funcionalidades

- **Depositar:** Adicione valores ao saldo da conta.
- **Sacar:** Realize saques respeitando o limite diário e o saldo disponível.
- **Extrato:** Visualize todas as movimentações realizadas (depósitos e saques).

## Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)

## Como Executar

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/banco-simples-web.git
   cd banco-simples-web
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```sh
   pip install flask
   ```

4. **Execute a aplicação:**
   ```sh
   python app.py
   ```

5. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

## Estrutura do Projeto

```
banco-simples-web/
│
├── app.py
├── templates/
│   └── index.html
└── README.md
```

## Observações

- Os dados (saldo, extrato, etc.) são armazenados em variáveis globais e serão resetados ao reiniciar a aplicação.
- Este projeto é apenas para fins didáticos e não deve ser usado em produção.

## Licença

Este projeto está sob a licença MIT.
