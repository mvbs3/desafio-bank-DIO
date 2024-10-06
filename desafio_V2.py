menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar um Usuario
[a] Criar uma Conta-corrente
[q] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
numero_conta = 1
LIMITE_SAQUES = 3
AGENCIA = "0001"
usuarios_cadastrados = {}
def deposito(saldo, valor, extrato, /):
    if(valor > 0):
        saldo += valor
        print(f"Saldo atual: R${float(saldo):.2f}")
        extrato.append(f"Depósito R${float(valor):.2f}")
    else:  
        print("Valor de depósito inválido")
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if(numero_saques == limite_saques):
        print(f"Número de saque diários excedido ({limite_saques} saques diários)")        
    elif (saldo<valor):
        print(f"Valor do saque de R${valor} excede o saldo atual (R${saldo})")
    elif(valor > limite):
        print("Valor excede o valor máximo de R$500,00")
    else:
        numero_saques+=1
        saldo-=valor
        print(f"Valor atual do saldo: R${saldo:.2f}")
        extrato.append(f"Saque R${float(valor):.2f}")
    return saldo, extrato

def mostrar_extrato(saldo, /, *, extrato):
    print("Extrato completo:")
    for linha_extrato in extrato:
        print(linha_extrato)
    print(f"\nSaldo atual: {saldo:.2f}")

def criar_usuario(nome, data_de_nascimento, cpf, endereco, usuarios_cadastrados):
    cpf = cpf.replace(".","").replace("-","")
    if(not (cpf in usuarios_cadastrados.keys())):
        usuarios_cadastrados[cpf] = {"nome": nome, "data_de_nascimento" : data_de_nascimento, "cpf": cpf, "endereco":endereco, "conta": []}
        print(f"\nUsuário {nome}(cpf {cpf}) cadastrado!")
    else:
        print(f"O CPF {cpf} ja está cadastrado!")
    return usuarios_cadastrados

def criar_conta_corrente(cpf,usuarios_cadastrados, agencia, numero_conta):
    cpf = cpf.replace(".","").replace("-","")

    if((cpf in usuarios_cadastrados.keys())):
        usuarios_cadastrados[cpf]["conta"].append({"conta" : numero_conta, "agencia" : agencia})
        print(f"\nUsuário {usuarios_cadastrados[cpf]["nome"]}(cpf {cpf}) cadstrou a conta {numero_conta} na agencia {agencia}!")
        return usuarios_cadastrados, (numero_conta + 1)
    else:
        print(f"O CPF {cpf} nao está cadastrado")
    return usuarios_cadastrados, numero_conta
while True:
    opcao = input(menu)

    if opcao == "d" or opcao=="D":
        #deposito
        valor_deposito = float(input("Insira o valor que você quer depositar.\n"))
        saldo, extrato = deposito(saldo, valor_deposito, extrato)

    elif opcao == "s" or opcao=="S":
        #saque
        valor_saque = float(input ("Insira o valor que você quer sacar.\n")) 
        saldo, extrato = saque(saldo = saldo, valor = valor_saque, extrato = extrato, limite=limite, numero_saques=numero_saques, limite_saques= LIMITE_SAQUES)
    elif opcao == "e" or opcao=="E":
        #extrato
        mostrar_extrato(saldo, extrato=extrato)
    elif opcao == "c" or opcao=="C":
        #cadastrar usuario
        nome = input("Insira seu nome!\n")
        data_de_nascimento = input("Insira sua data de nascimento no formato: DD-MM-YYYY!\n")
        cpf = input("Insira seu cpf! Formatos validos: xxx.xxx.xxx-xx ou xxxxxxxxxxx\n")
        endereco = input("Insira seu endereco no formato: logradouro, nro - bairro - cidade/sigla estado!\n")
        usuarios_cadastrados = criar_usuario(nome, data_de_nascimento, cpf, endereco, usuarios_cadastrados) 
    elif opcao == "a" or opcao=="A":
        cpf = input("Insira seu cpf! Formatos validos: xxx.xxx.xxx-xx ou xxxxxxxxxxx\n")
        usuarios_cadastrados, numero_conta = criar_conta_corrente(cpf, usuarios_cadastrados, AGENCIA, numero_conta)
    elif opcao == "q" or opcao=="Q":
        print("Obrigado por utilizar esse banco\n")
        #sair
        break

    else:
        print("Operação inválida, por favor selecione uma operação válida.")