menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "d" or opcao=="D":
        #deposito
        valor_deposito = float(input("Insira o valor que você quer depositar.\n"))
        if(valor_deposito > 0):
            saldo += valor_deposito
            print(f"Saldo atual: R${float(saldo):.2f}")
            extrato.append(f"Depósito R${float(valor_deposito):.2f}")
        else:  
            print("Valor de depósito inválido")

    elif opcao == "s" or opcao=="S":
        #saque
        valor_saque = float(input ("Insira o valor que você quer sacar.\n")) 
        if(numero_saques == LIMITE_SAQUES):
            print(f"Número de saque diários excedido ({LIMITE_SAQUES} saques diários)")        
        elif (saldo<valor_saque):
            print(f"Valor do saque de R${valor_saque} excede o saldo atual (R${saldo})")
        elif(valor_saque > 500):
            print("Valor excede o valor máximo de R$500,00")
        else:
            numero_saques+=1
            saldo-=valor_saque
            print(f"Valor atual do saldo: R${saldo:.2f}")
            extrato.append(f"Saque R${float(valor_saque):.2f}")


    elif opcao == "e" or opcao=="E":
        #extrato
        print("Extrato completo:")
        for linha_extrato in extrato:
            print(linha_extrato)
        print(f"\nSaldo atual: {saldo:.2f}")

    elif opcao == "q" or opcao=="Q":
        print("Obrigado por utilizar esse banco")
        #sair
        break

    else:
        print("Operação inválida, por favor selecione uma operação válida.")