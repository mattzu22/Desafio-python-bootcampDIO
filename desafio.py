import re

dados_usuario = {"saldo": 400, "limite": 500, "extrato": "", "numero_saques": 0, "LIMITE_SAQUES":3}
lista_usuarios = {
    '12377663660': {'nome': 'matheus', 'data_nascimento': '16/12/1998', 'endereco': 'parnamirin,687 - ribeira - natal/rn'},
    '12377663661': {'nome': 'paulo', 'data_nascimento': '16/12/1994', 'endereco': 'parnamirin,687 - ribeira - natal/rn'},
    '12377663662': {'nome': 'roberto', 'data_nascimento': '16/12/1993', 'endereco': 'parnamirin,687 - ribeira - natal/rn'},
    '12377663663': {'nome': 'elton', 'data_nascimento': '16/12/1999', 'endereco': 'parnamirin,687 - ribeira - natal/rn'}
    }
lista_contas = {
    '12377663660': [{"conta": 1, "agencia": "0001"}, {"conta": 2, "agencia": "0001"}],
}

def menu():
    menu = """
    ============== Menu ===============
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q] Sair
    => """

    return input(menu)

# Funções do banco
def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! O número de saques excede o limite")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        
        message = f"Saldo atualizado: R$ {saldo}"
        print(message)

    else:
       print("Operação falhou! O valor informado é inválido.")
       
    return saldo, extrato, numero_saques     
def despositar(valor, saldo, extrato, /):   
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        
        message = f"Saldo atualizado: R${saldo}"
        print(message)
    else:
        print("Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato    
def visualizar_extrato(saldo,/,*,extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função utilitaria
def formatarCPF(cpf):
    return cpf.replace(".", "").replace("-", "")
def verificarFormatoEndereco(endereco):
    padrao = r'^[a-záéíóúâêôãõç\s]+,\d+\s*-\s*[a-záéíóúâêôãõç\s]+\s*-\s*[a-záéíóúâêôãõç\s]+/[a-z]{2}$'
    return bool(re.match(padrao, endereco, re.IGNORECASE))

# Funções do usuário 
def criar_usuario(cpf, nome, data_nascimento, endereco):
    global lista_usuarios
    
    if not all([cpf, nome, data_nascimento, endereco]):
        print("Todas as informações são obrigatórias.")
        return None
    
    if not verificarFormatoEndereco(endereco):
        print("Endereço inválido.")
        return None
    
    cpf_formatado = formatarCPF(cpf)
    
    if not lista_usuarios.get(cpf_formatado):
        lista_usuarios[cpf_formatado] = {"nome": nome, "data_nascimento": data_nascimento, "endereco": endereco}
        print("Usuário cadastrado!")
        return
    else: 
        print("usuario já cadastrado.")
        return               
def criar_conta(usuario):
    global lista_contas, lista_usuarios

    AGENCIA = "0001"
    usuario_filtrado = lista_usuarios.get(usuario)
    
    if not usuario_filtrado:
        print("usuário não existe, crie um conta primeiro.")
        return
    
    if not lista_contas.get(usuario):
        lista_contas[usuario] = []

    numero_conta = len(lista_contas[usuario]) + 1
    lista_contas[usuario].append({"conta": numero_conta, "agencia": AGENCIA})
    
    print("Conta criada!")
def listar_contas(contas, usuarios):
    for conta in contas:
        for dados in contas[conta]:
            linha = f"""
            Agência: {dados["agencia"]}
            C/C: {dados["conta"]}
            Titular: {usuarios[conta]["nome"]}
            """
            print("=" * 100)
            print(linha)


def main():
    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            dados_usuario["saldo"], dados_usuario["extrato"] = despositar(valor, dados_usuario["saldo"], dados_usuario["extrato"])

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            dados_usuario["saldo"], dados_usuario["extrato"], dados_usuario["numero_saques"] = sacar(valor=valor, saldo=dados_usuario["saldo"], extrato=dados_usuario["extrato"], LIMITE_SAQUES=dados_usuario["LIMITE_SAQUES"], numero_saques=dados_usuario["numero_saques"], limite=dados_usuario["limite"])

        elif opcao == "e":
            visualizar_extrato(dados_usuario["saldo"], extrato=dados_usuario["extrato"])
        
        elif opcao == "nc":    
            cpf = input("Informe o CPF: ")
            criar_conta(cpf)
            
        elif opcao == "nu":
            cpf = input("Informe seu cpf: ")
            nome = input("Informe seu nome: ")
            data_nascimento = input("Informe sua data de nascimento: ")
            endereco = input("Informe seu endereço: (ex: parnamirin,687 - ribeira - natal/rn): ")
            criar_usuario(cpf, nome, data_nascimento, endereco)
            print(lista_usuarios)
            
        elif opcao == "lc":
            listar_contas(contas=lista_contas, usuarios=lista_usuarios)
            
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
            
main()            