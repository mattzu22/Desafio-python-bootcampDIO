import re

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

dados_usuario = {"saldo": 400, "limite": 500, "extrato": "", "numero_saques": 0, "LIMITE_SAQUES":3}
lista_usuarios = {
    '12377663660': {'nome': 'matheus', 'data_nascimento': '16/12/1998', 'endereco': 'parnamirin,687 - ribeira - natal/rn'},
    '12377663661': {'nome': 'paulo', 'data_nascimento': '16/12/1994', 'endereco': 'parnamirin,687 - ribeira - natal/rn'},
    '12377663662': {'nome': 'roberto', 'data_nascimento': '16/12/1993', 'endereco': 'parnamirin,687 - ribeira - natal/rn'},
    '12377663663': {'nome': 'elton', 'data_nascimento': '16/12/1999', 'endereco': 'parnamirin,687 - ribeira - natal/rn'}
    }
# lista_contas = [
#     {"conta": 1, "agencia": "0001", "usuario": "12377663660"},
#     {"conta": 2, "agencia": "0001", "usuario": "12377663660"},
#     {"conta": 3, "agencia": "0001", "usuario": "12377663660"}
# ]
lista_contas = {
    "12377663660": [
        {"conta": 1, "agencia": "0001"},
        {"conta": 2, "agencia": "0001"},
        {"conta": 3, "agencia": "0001"}
    ],
}



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
    else: 
        print("usuario já cadastrado.")   
             
def criar_conta(usuario):
    global lista_contas, lista_usuarios

    AGENCIA = "0001"
    usuario_filtrado = lista_usuarios.get(usuario)
    
    if not usuario_filtrado:
        return print("usuário não existe.") 
    
    if not lista_contas.get(usuario):
        lista_contas[usuario] = {"conta": 1, "agencia": AGENCIA}
    else:
        lista_contas[usuario]["conta"] += 1
    
    print("Conta criada!")
         
# criar_usuario(cpf="123.776.636-68", nome="roberto", data_nascimento="16/12/1998",endereco='parnamirin,687 - ribeira - natal/rn')

criar_conta(usuario='12377663661') 
criar_conta(usuario='12377663662')
criar_conta(usuario='12377663662')
criar_conta(usuario='12377663663')
# criar_conta(usuario='12377663660')
# criar_conta(usuario='12377663663')

print(f"lista de contas: {lista_contas}\n")

# print(f"lista de usuários: {lista_usuarios}") 

# while True:

#     opcao = input(menu)

#     if opcao == "d":
#         valor = float(input("Informe o valor do depósito: "))

#         dados_usuario["saldo"], dados_usuario["extrato"] = despositar(valor, dados_usuario["saldo"], dados_usuario["extrato"])

#     elif opcao == "s":
#         valor = float(input("Informe o valor do saque: "))

#         dados_usuario["saldo"], dados_usuario["extrato"], dados_usuario["numero_saques"] = sacar(valor=valor, saldo=dados_usuario["saldo"], extrato=dados_usuario["extrato"], LIMITE_SAQUES=dados_usuario["LIMITE_SAQUES"], numero_saques=dados_usuario["numero_saques"], limite=dados_usuario["limite"])

#     elif opcao == "e":
#         visualizar_extrato(dados_usuario["saldo"], extrato=dados_usuario["extrato"])

#     elif opcao == "q":
#         break

#     else:
#         print("Operação inválida, por favor selecione novamente a operação desejada.")