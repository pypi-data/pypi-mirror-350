from abc import ABC, abstractclassmethod,abstractproperty
from datetime import datetime
import textwrap

class Cliente:      
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente, ):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0002"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod    
    def criar_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico (self):
        return self._historico
    
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print(f"\nDepósito Realizado!!!")
        else:
            print("\nSeu deposito não foi aceito!!!")
            return False
        
        return True
    
    def sacar(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print("\nVocê não tem dinheiro o suficiente para realizar este saque.")
        elif valor > 0:
            self._saldo -= valor
            print(f"\nSaque Realizado!!!")
            return True
        else:
            print("\nVocê não pode sacar valores negativos ou iguais a 0")
        
        return False
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if numero_saques >= self.limite_saques:
            print("\nVocê não pode sacar mais de 3 vezes ao dia")

        elif valor > self.limite:
            print("\nVocê não pode sacar mais que R$500")
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""
        Agência = {self.agencia}
        Numero = {self.numero}
        Titular = {self.cliente.nome}"""
        
        
        
class Historico():
    def __init__(self):
        self.transacoes = []
        
    @property
    def trasacoes(self):
        return self._trasacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
        {
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao :
            conta.historico.adicionar_transacao(self)
            
            
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))
    
    
    
def filtar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta.")
        return

    return cliente.contas[0]

def depositar(clientes):
    cpf = int(input("Informe o CPF do cliente:(somente numeros)\n"))
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta,transacao)

def sacar(clientes):
    cpf = int(input("Informe o CPF do cliente:(somente numeros)\n"))
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = int(input("Informe o CPF do cliente:(somente numeros)\n"))
    cliente = filtar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")
    
def criar_cliente(clientes):
    cpf = int(input("Informe o CPF do cliente:(somente numeros)\n"))
    cliente = filtar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta,cliente,contas):
    cpf = int(input("Informe o CPF do cliente:(somente numeros)\n"))
    cliente = filtar_cliente(cpf, cliente)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.criar_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))



def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()  

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()