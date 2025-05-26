from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

usuarios = []
contas = []
NUMERO_AGENCIA = "0001"

def criar_usuario(nome, cpf, data_nascimento, endereco):
    if any(u["cpf"] == cpf for u in usuarios):
        return None, "Já existe um usuário cadastrado com este CPF."
    usuario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }
    usuarios.append(usuario)
    return usuario, f"Usuário {nome} criado com sucesso!"

def criar_conta(cpf):
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if usuario:
        numero_conta = len(contas) + 1  
        conta = {
            "agencia": NUMERO_AGENCIA,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "limite": 500,
            "extrato": [],
            "numero_saques": 0,
            "LIMITE_SAQUES": 3
        }
        contas.append(conta)
        return conta
    return None

def buscar_contas_por_cpf(cpf):
    return [c for c in contas if c["usuario"]["cpf"] == cpf]

def buscar_conta_por_numero(numero_conta, cpf):
    return next((c for c in contas if c["numero_conta"] == numero_conta and c["usuario"]["cpf"] == cpf), None)

def depositar(conta, valor):
    if valor > 0:
        conta["saldo"] += valor
        datahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conta["extrato"].append(f"[{datahora}] Depósito: R$ {valor:.2f}")
        return f"Depósito de R$ {valor:.2f} realizado com sucesso!"
    else:
        return "Valor inválido para depósito."

def sacar(conta, valor):
    if valor > 0 and valor <= conta["saldo"] and valor <= conta["limite"] and conta["numero_saques"] < conta["LIMITE_SAQUES"]:
        conta["saldo"] -= valor
        conta["numero_saques"] += 1
        datahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conta["extrato"].append(f"[{datahora}] Saque: R$ {valor:.2f}")
        return f"Saque de R$ {valor:.2f} realizado com sucesso!"
    elif conta["numero_saques"] >= conta["LIMITE_SAQUES"]:
        return "Limite de saques atingido"
    else:
        return "Valor inválido ou saldo insuficiente."

def extrato(conta):
    if conta["extrato"]:
        return "\n".join(conta["extrato"])
    else:
        return "Não foram realizadas movimentações."

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""
    extrato_texto = None
    usuario_logado = None
    contas_usuario = []
    conta_selecionada = None

    # PROCESSA LOGOUT PRIMEIRO, ANTES DE QUALQUER OUTRA LÓGICA
    if request.method == "POST" and "logout" in request.form:
        session.pop("cpf_logado", None)
        session.pop("conta_ativa", None)
        return redirect(url_for("index", logout="1"))

    # SE FOI REDIRECIONADO APÓS LOGOUT, NÃO RECUPERA USUÁRIO DA SESSÃO
    if request.args.get("logout") == "1":
        mensagem = "Obrigado por utilizar nossos serviços, volte sempre!"
    elif "cpf_logado" in session:
        usuario_logado = next((u for u in usuarios if u["cpf"] == session["cpf_logado"]), None)
        if usuario_logado:
            contas_usuario = buscar_contas_por_cpf(usuario_logado["cpf"])
            if "conta_ativa" in session:
                conta_selecionada = buscar_conta_por_numero(session["conta_ativa"], usuario_logado["cpf"])
            elif contas_usuario:
                conta_selecionada = contas_usuario[0]
                session["conta_ativa"] = conta_selecionada["numero_conta"]

    # RESTANTE DO POST (exceto logout)
    if request.method == "POST":
        if "criar_usuario" in request.form:
            nome = request.form["nome"]
            cpf = request.form["cpf"]
            data_nascimento = request.form["data_nascimento"]
            endereco = request.form["endereco"]
            usuario, mensagem = criar_usuario(nome, cpf, data_nascimento, endereco)
            if usuario:
                conta_criada = criar_conta(cpf)
                if conta_criada:
                    mensagem += f" Conta {conta_criada['numero_conta']} criada automaticamente!"
        elif "login" in request.form:
            cpf = request.form["cpf_login"]
            usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
            if usuario:
                session["cpf_logado"] = cpf
                session.pop("conta_ativa", None)
                return redirect(url_for("index"))
            else:
                mensagem = "Usuário não encontrado."
        elif "criar_conta" in request.form and usuario_logado:
            cpf = usuario_logado["cpf"]
            conta_criada = criar_conta(cpf)
            if conta_criada:
                mensagem = f"Conta {conta_criada['numero_conta']} criada para o CPF {cpf}!"
                session["conta_ativa"] = conta_criada["numero_conta"]
                conta_selecionada = conta_criada
                contas_usuario = buscar_contas_por_cpf(cpf)
            else:
                mensagem = "Conta não pôde ser criada. Usuário não encontrado."
        elif "selecionar_conta" in request.form and usuario_logado:
            numero_conta = int(request.form["numero_conta"])
            conta = buscar_conta_por_numero(numero_conta, usuario_logado["cpf"])
            if conta:
                session["conta_ativa"] = numero_conta
                conta_selecionada = conta
            else:
                mensagem = "Conta não encontrada."
        elif conta_selecionada:
            if "depositar" in request.form:
                valor = float(request.form["valor"])
                mensagem = depositar(conta_selecionada, valor)
                extrato_texto = None
            elif "sacar" in request.form:
                valor = float(request.form["valor"])
                mensagem = sacar(conta_selecionada, valor)
                extrato_texto = None
            elif "extrato" in request.form:
                extrato_texto = extrato(conta_selecionada)
                mensagem = ""
        else:
            mensagem = "Nenhuma conta disponível. Crie um usuário e uma conta primeiro."

    print(session)  # Para depuração

    return render_template(
        "index.html",
        usuario_logado=usuario_logado,
        contas_usuario=contas_usuario,
        conta_selecionada=conta_selecionada,
        saldo=conta_selecionada["saldo"] if conta_selecionada else 0,
        extrato=conta_selecionada["extrato"] if conta_selecionada else [],
        mensagem=mensagem,
        extrato_texto=extrato_texto
    )

if __name__ == "__main__":
    app.run(debug=True)