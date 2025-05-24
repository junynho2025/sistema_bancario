from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

@app.route("/", methods=["GET", "POST"])
def index():
    global saldo, extrato, numero_saques
    mensagem = ""
    if request.method == "POST":
        if "depositar" in request.form:
            valor = float(request.form["valor"])
            if valor > 0:
                saldo += valor
                extrato.append(f"Depósito: R$ {valor:.2f}")
                mensagem = f"Depósito de R$ {valor:.2f} realizado com sucesso!"
            else:
                mensagem = "Valor inválido para depósito."
        elif "sacar" in request.form:
            valor = float(request.form["valor"])
            if valor > 0 and valor <= saldo and valor <= limite and numero_saques < LIMITE_SAQUES:
                saldo -= valor
                numero_saques += 1
                extrato.append(f"Saque: R$ {valor:.2f}")
                mensagem = f"Saque de R$ {valor:.2f} realizado com sucesso!"
            elif numero_saques >= LIMITE_SAQUES:
                mensagem = "Limite de saques atingido"
            else:
                mensagem = "Valor inválido ou saldo insuficiente."
        elif "extrato" in request.form:
            mensagem = "Extrato solicitado."
    return render_template("index.html", saldo=saldo, extrato=extrato, mensagem=mensagem)

if __name__ == "__main__":
    app.run(debug=True)