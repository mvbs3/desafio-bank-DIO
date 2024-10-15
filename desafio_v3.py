import datetime
from abc import ABC, abstractmethod

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[c] Criar um Usuario
[a] Criar uma Conta-corrente
[q] Sair

=> """
class Transacao(ABC):
    @property
    def valor(self):
        pass
    @abstractmethod
    def registrar(self,conta):
        pass
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        if(conta.sacar(self.valor)):
            conta.historico.adicionar_transacao(self)

class Depositar(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        if(conta.depositar(self.valor)):
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo" : transacao.__class__.__name__,
            "valor": transacao.valor, 
                            })


class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self,conta):
        self.contas.append(conta)
    

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    def __str__(self):
        return f"Cliente {self.nome} do CPF {self.cpf}"
class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0
        self.numero = numero
        self.agencia = 500
        self.cliente = cliente
        self.historico  = Historico()
    
    @classmethod
    def nova_conta(cls,cliente, numero):
        return cls(numero,cliente)
    def sacar(self,valor):
        saldo = self.saldo
        if (saldo<valor):
            print(f"Valor do saque de R${valor} excede o saldo atual (R${saldo})")
        elif (valor <= 0):
            print("Valor de saque inválido")
        else:
            saldo= saldo - valor
            print(f"Valor atual do saldo: R${saldo:.2f}")
            self.saldo = saldo
            return True
        return False
         
    def depositar(self,valor):
        if(valor>0):
            self.saldo += valor
            print(f"Saldo atual: R${float(self.saldo):.2f}")
            return True
        else:
            print("Valor de depósito inválido")
            return False
    def __str__(self):
        return f"Conta num: {self.numero} da agencia: {self.agencia}"
          
class ContaCorrente(Conta):
    def __init__(self,  cliente, numero, limite =500, limite_saque = 3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saque = limite_saque
    
    def sacar(self,valor):
        if (len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"] ) >= self.limite_saque):
            print(f"Número de saque diários excedido ({self.limite_saque} saques diários)")        
        elif(self.limite < valor):
            print(f"Valor excede o valor máximo de R${self.limite:2f}")
        else:
                        
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
                Agência: {self.agencia}
                Num Conta:{self.numero}
                Numero de Transacoes {len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])}

        """

def encontrar_cliente_pelo_cpf(cpf, clientes):
    cliente_encontrado = [cliente for cliente in clientes if cliente.cpf == cpf]
    return cliente_encontrado
def retornar_contas_cliente(cliente):
    i = 1
    for conta in cliente.contas:
        print(f"{i}. Conta {conta.numero} da agencia {conta.agencia} com saldo: {conta.saldo}, ")
        i+=1
    return len(cliente.contas)
def deposito(cpf, clientes, /):
    cliente_encontrado = encontrar_cliente_pelo_cpf(cpf, clientes)
    if(not cliente_encontrado):
        print("Cpf inválido, cliente não cadastrado")
        return
    else:
       
        num_contas =retornar_contas_cliente(cliente_encontrado[0])
        if not num_contas:
            print("não há contas cadastradas")
            return
        conta_selecionada = int(input(f"Escolha qual conta, digite um número de 1 a {num_contas}\n"))
        valor_deposito = float(input("Informe o valor da transacao!\n"))
        transacao = Depositar(valor_deposito)
        cliente_encontrado[0].realizar_transacao(cliente_encontrado[0].contas[conta_selecionada-1], transacao)
    

def saque(*, cpf,clientes):
    cliente_encontrado = encontrar_cliente_pelo_cpf(cpf, clientes)
    if(not cliente_encontrado):
        print("Cpf inválido, cliente não cadastrado")
        return
    else:
        
        num_contas =retornar_contas_cliente(cliente_encontrado[0])
        if not num_contas:
            print("não há contas cadastradas")
            return
        conta_selecionada = int(input(f"Escolha qual conta, digite um número de 1 a {num_contas}\n"))
        valor_saque = float(input("Informe o valor da transacao!\n"))
        transacao = Saque(valor_saque)
        cliente_encontrado[0].realizar_transacao(cliente_encontrado[0].contas[conta_selecionada-1], transacao)


def mostrar_extrato(cpf, /, *, clientes , contas):
    cliente_encontrado = encontrar_cliente_pelo_cpf(cpf, clientes)
    if(not cliente_encontrado):
        print("Cpf inválido, cliente não cadastrado")
        return
    else:
        num_contas =retornar_contas_cliente(cliente_encontrado[0])
        if not num_contas:
            print("não há contas cadastradas")
            return
        conta_selecionada = int(input(f"Escolha qual conta, digite um número de 1 a {num_contas}\n"))
        transacoes = cliente_encontrado[0].contas[conta_selecionada-1].historico.transacoes
        for transacao in transacoes:
            print(f"Evento do tipo {transacao["tipo"]} e valor: {transacao["valor"]}")


   

def criar_usuario(nome, data_de_nascimento, cpf, endereco, clientes):
    cliente_encontrado = encontrar_cliente_pelo_cpf(cpf, clientes)
    if(cliente_encontrado):
        print("Cpf inválido, Cliente ja cadastrado")
        return
    else:
        cliente = PessoaFisica(cpf,nome,data_de_nascimento,endereco)
        clientes.append(cliente)
        print("Cliente criado com sucesso")
    
    
def criar_conta_corrente(cpf, clientes, contas, numero_conta):
    cliente_encontrado = encontrar_cliente_pelo_cpf(cpf,clientes)
    if(not cliente_encontrado):
        return
    conta_criada = ContaCorrente(cliente_encontrado, numero_conta)
    contas.append(conta_criada)
    cliente_encontrado[0].contas.append(conta_criada)
    print("Conta criada com sucesso")

    
clientes = []
contas = []
while True:
    # for i in clientes:
    #     print(i)
    #     print("contas: ")
    #     for j in i.contas:
    #         print(j) 

    opcao = input(menu)
    
    if opcao == "d" or opcao=="D":
        #deposito
        #valor_deposito = float(input("Insira o valor que você quer depositar.\n"))
        cpf = input("Insira o seu CPF.\n")
        deposito(cpf, clientes)

    elif opcao == "s" or opcao=="S":
        #saque
        cpf = input("Insira o seu CPF.\n")
        saque(cpf = cpf, clientes = clientes)
    elif opcao == "e" or opcao=="E":
        #extrato
        cpf = input("Insira o seu CPF.\n")
        mostrar_extrato(cpf, clientes=clientes,contas=contas)
    elif opcao == "c" or opcao=="C":
        #cadastrar usuario
        nome = input("Insira seu nome!\n")
        data_de_nascimento = input("Insira sua data de nascimento no formato: DD-MM-YYYY!\n")
        cpf = input("Insira seu cpf! Formatos validos: xxx.xxx.xxx-xx ou xxxxxxxxxxx\n")
        endereco = input("Insira seu endereco no formato: logradouro, nro - bairro - cidade/sigla estado!\n")
        criar_usuario(nome, data_de_nascimento, cpf, endereco, clientes) 
    elif opcao == "a" or opcao=="A":
        #criar conta corrente
        cpf = input("Insira seu cpf! Formatos validos: xxx.xxx.xxx-xx ou xxxxxxxxxxx\n")
        numero_conta = len(contas) +1
        criar_conta_corrente(cpf,clientes, contas, numero_conta)
    elif opcao == "q" or opcao=="Q":
        print("Obrigado por utilizar esse banco\n")
        #sair
        break

    else:
        print("Operação inválida, por favor selecione uma operação válida.")
